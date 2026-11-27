"""`ult appstore check` - offline review of an Expo app's App Store setup.

Reads app.json or app.config.json, eas.json, package.json and, when present,
store.config.json (EAS Metadata). Reports missing or risky items before a
store build: bundle ID, version and build number, permission usage strings,
privacy manifest, icon, encryption flag, build profiles, privacy and support
URLs, and secrets or signing files that should never be in the project.

Standard library only, no network. Exit 0 when clean, 1 when there are
findings at warn or fail level, 2 when the project cannot be read.
"""
from __future__ import annotations

import json
import os
import re
import struct
import subprocess
import sys
from pathlib import Path

LEVELS = ("fail", "warn", "note")

# Package -> usage strings it needs, with the config plugin option that can set each one.
# (key, plugin option, required): required False means "only if the app uses that feature".
PERMISSIONS: dict[str, list[tuple[str, str, bool]]] = {
    "expo-camera": [("NSCameraUsageDescription", "cameraPermission", True),
                    ("NSMicrophoneUsageDescription", "microphonePermission", False)],
    "react-native-vision-camera": [("NSCameraUsageDescription", "cameraPermissionText", True),
                                   ("NSMicrophoneUsageDescription", "microphonePermissionText", False)],
    "expo-image-picker": [("NSPhotoLibraryUsageDescription", "photosPermission", True),
                          ("NSCameraUsageDescription", "cameraPermission", False)],
    "expo-media-library": [("NSPhotoLibraryUsageDescription", "photosPermission", True),
                           ("NSPhotoLibraryAddUsageDescription", "savePhotosPermission", True)],
    "expo-location": [("NSLocationWhenInUseUsageDescription", "locationWhenInUsePermission", True),
                      ("NSLocationAlwaysAndWhenInUseUsageDescription", "locationAlwaysAndWhenInUsePermission", False)],
    "expo-contacts": [("NSContactsUsageDescription", "contactsPermission", True)],
    "expo-calendar": [("NSCalendarsFullAccessUsageDescription", "calendarPermission", True),
                      ("NSRemindersFullAccessUsageDescription", "remindersPermission", False)],
    "expo-audio": [("NSMicrophoneUsageDescription", "microphonePermission", False)],
    "expo-av": [("NSMicrophoneUsageDescription", "microphonePermission", False)],
    "expo-tracking-transparency": [("NSUserTrackingUsageDescription", "userTrackingPermission", True)],
    "expo-local-authentication": [("NSFaceIDUsageDescription", "faceIDPermission", True)],
    "expo-sensors": [("NSMotionUsageDescription", "motionPermission", False)],
    "expo-speech-recognition": [("NSSpeechRecognitionUsageDescription", "speechRecognitionPermission", True),
                                ("NSMicrophoneUsageDescription", "microphonePermission", True)],
}

API_CATEGORIES = {
    "NSPrivacyAccessedAPICategoryUserDefaults", "NSPrivacyAccessedAPICategoryFileTimestamp",
    "NSPrivacyAccessedAPICategorySystemBootTime", "NSPrivacyAccessedAPICategoryDiskSpace",
    "NSPrivacyAccessedAPICategoryActiveKeyboards",
}
REASON_CODE = re.compile(r"^[0-9A-F]{4}\.[0-9]$")
BUNDLE_ID = re.compile(r"^[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")
PLACEHOLDER_ID = re.compile(r"^(com|org|io)\.(example|yourcompany|your-company|mycompany|company|test)\b", re.I)
MARKETING_VERSION = re.compile(r"^\d+(\.\d+){0,2}$")
VAGUE_PURPOSE = re.compile(r"^\s*(allow\s+\$\(PRODUCT_NAME\)\s+to\s+access\s+your\s+\w+\.?|needed\.?|required\.?|for the app\.?)\s*$", re.I)

THIRD_PARTY_LOGIN = {"@react-native-google-signin/google-signin", "react-native-fbsdk-next",
                     "@invertase/react-native-apple-authentication", "react-native-app-auth"}
APPLE_LOGIN = {"expo-apple-authentication", "@invertase/react-native-apple-authentication"}
IAP_LIBS = {"react-native-iap", "expo-iap", "react-native-purchases", "expo-in-app-purchases"}
WEB_PAYMENT_LIBS = {"@stripe/stripe-react-native", "react-native-paypal", "@paypal/react-native-paypal"}

SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN (?:EC |RSA )?PRIVATE KEY-----"), "a private key block"),
    (re.compile(r"\bsk_live_[0-9A-Za-z]{10,}"), "a Stripe live secret key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "an AWS access key ID"),
    (re.compile(r"\bgh[pousr]_[0-9A-Za-z]{30,}"), "a GitHub token"),
    (re.compile(r"\b[a-z]{4}-[a-z]{4}-[a-z]{4}-[a-z]{4}\b"), "something shaped like an Apple app-specific password"),
]
SECRET_NAME = re.compile(r"(SECRET|TOKEN|PASSWORD|PRIVATE|API_?KEY)", re.I)
SIGNING_SUFFIXES = (".p8", ".p12", ".mobileprovision", ".keystore", ".jks")
SKIP_DIRS = {"node_modules", ".git", "Pods", ".expo", "build", "dist", ".ultimatum", "DerivedData"}


class BadInput(Exception):
    pass


def _finding(level: str, code: str, where: str, msg: str, fix: str = "") -> dict:
    return {"level": level, "code": code, "where": where, "message": msg, "fix": fix}


def _load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as e:
        raise BadInput(f"cannot read {path.name}: {e}") from e
    except json.JSONDecodeError as e:
        raise BadInput(f"{path.name} is not valid JSON (line {e.lineno}): {e.msg}") from e
    if not isinstance(data, dict):
        raise BadInput(f"{path.name} must hold a JSON object")
    return data


def load_app_config(root: Path, config: str | None = None) -> tuple[dict, str, list[dict]]:
    """Return (expo config, file name, notes). Raises BadInput when there is none to read."""
    notes: list[dict] = []
    if config:
        path = (root / config) if not os.path.isabs(config) else Path(config)
        if not path.is_file():
            raise BadInput(f"config file not found: {config}")
        candidates = [path]
    else:
        candidates = [root / n for n in ("app.json", "app.config.json") if (root / n).is_file()]
    dynamic = [n for n in ("app.config.js", "app.config.ts", "app.config.mjs", "app.config.cjs") if (root / n).is_file()]
    if not candidates:
        if dynamic:
            raise BadInput(f"only {dynamic[0]} found; this checker does not run JavaScript. Write the resolved "
                           "config with `npx expo config --json > app.config.resolved.json` and pass "
                           "--config app.config.resolved.json")
        raise BadInput(f"no app.json or app.config.json in {root}")
    path = candidates[0]
    data = _load_json(path)
    expo = data.get("expo", data)
    if not isinstance(expo, dict):
        raise BadInput(f"{path.name}: `expo` must be an object")
    if dynamic and not config:
        notes.append(_finding("note", "AS002", dynamic[0],
                              f"{dynamic[0]} can change what {path.name} says; this check read {path.name} only",
                              "check the resolved config: `npx expo config --json`, then --config"))
    return expo, path.name, notes


def _deps(root: Path) -> set[str]:
    pkg = root / "package.json"
    if not pkg.is_file():
        return set()
    data = _load_json(pkg)
    out: set[str] = set()
    for key in ("dependencies", "devDependencies"):
        block = data.get(key) or {}
        if isinstance(block, dict):
            out.update(block)
    return out


def _plugins(expo: dict) -> dict[str, dict]:
    """Config plugins by name, with their options ({} when given without options)."""
    out: dict[str, dict] = {}
    for entry in expo.get("plugins") or []:
        if isinstance(entry, str):
            out.setdefault(entry, {})
        elif isinstance(entry, list) and entry and isinstance(entry[0], str):
            opts = entry[1] if len(entry) > 1 and isinstance(entry[1], dict) else {}
            out[entry[0]] = opts
    return out


def _png_info(path: Path) -> tuple[int, int, bool] | None:
    """(width, height, has_alpha) from a PNG header, or None when it is not a PNG."""
    try:
        with path.open("rb") as fh:
            head = fh.read(33)
    except OSError:
        return None
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", head[16:24])
    colour_type = head[25]
    return width, height, colour_type in (4, 6)


def _version_tuple(text: str) -> tuple[int, ...]:
    return tuple(int(x) for x in text.split("."))


def _git_show(root: Path, ref: str, name: str) -> dict | None:
    try:
        res = subprocess.run(["git", "-C", str(root), "show", f"{ref}:./{name}"],
                             capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    if res.returncode != 0:
        return None
    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError:
        return None
    return data.get("expo", data) if isinstance(data, dict) else None


def check_identity(expo: dict, src: str) -> list[dict]:
    out = []
    ios = expo.get("ios") or {}
    bid = ios.get("bundleIdentifier")
    if not bid:
        out.append(_finding("fail", "AS010", f"{src} ios.bundleIdentifier", "no iOS bundle ID",
                            "set ios.bundleIdentifier to a reverse-DNS ID you own, e.g. com.yourbrand.appname; "
                            "it cannot change after the first upload"))
    elif not BUNDLE_ID.match(bid):
        out.append(_finding("fail", "AS011", f"{src} ios.bundleIdentifier",
                            f"bundle ID `{bid}` is not valid (letters, digits, hyphens and dots, at least two parts)"))
    elif PLACEHOLDER_ID.match(bid):
        out.append(_finding("warn", "AS012", f"{src} ios.bundleIdentifier",
                            f"bundle ID `{bid}` looks like a placeholder", "use a domain the owner controls"))
    if not expo.get("name"):
        out.append(_finding("warn", "AS013", f"{src} name", "no app name",
                            "set `name`; it is the name under the icon (the store name is set in App Store Connect)"))
    return out


def check_versions(expo: dict, src: str, eas: dict | None, prev: dict | None) -> list[dict]:
    out = []
    ios = expo.get("ios") or {}
    version = expo.get("version")
    if not version:
        out.append(_finding("warn", "AS020", f"{src} version", "no `version`; Expo falls back to 1.0.0",
                            "set the version people see, e.g. 1.0.0"))
    elif not MARKETING_VERSION.match(str(version)):
        out.append(_finding("fail", "AS021", f"{src} version",
                            f"version `{version}` is not one to three numbers joined by dots, which Apple requires"))
    source = ((eas or {}).get("cli") or {}).get("appVersionSource", "local")
    prod = (((eas or {}).get("build") or {}).get("production") or {})
    auto = prod.get("autoIncrement") or (prod.get("ios") or {}).get("autoIncrement")
    build = ios.get("buildNumber")
    if source == "remote":
        if build is not None:
            out.append(_finding("note", "AS022", f"{src} ios.buildNumber",
                                "appVersionSource is remote, so EAS keeps the build number and ignores this one"))
    else:
        if build is None and not auto:
            out.append(_finding("warn", "AS023", f"{src} ios.buildNumber",
                                "no build number and no autoIncrement; every upload needs a new build number",
                                'set "cli": {"appVersionSource": "remote"} and "autoIncrement": true in eas.json'))
        elif build is not None and not str(build).replace(".", "").isdigit():
            out.append(_finding("fail", "AS024", f"{src} ios.buildNumber",
                                f"build number `{build}` must be numbers joined by dots"))
    if prev is not None and source != "remote":
        prev_ios = prev.get("ios") or {}
        pv, pb = str(prev.get("version", "")), str(prev_ios.get("buildNumber", ""))
        cv, cb = str(version or ""), str(build or "")
        same_version = pv == cv
        if not auto and same_version and pb and cb and pb.replace(".", "").isdigit() and cb.replace(".", "").isdigit():
            if _version_tuple(cb) <= _version_tuple(pb):
                out.append(_finding("fail", "AS025", f"{src} ios.buildNumber",
                                    f"build number {cb} is not higher than {pb} at the compared commit, "
                                    f"with the same version {cv}", "raise ios.buildNumber, or use remote autoIncrement"))
        if pv and cv and MARKETING_VERSION.match(pv) and MARKETING_VERSION.match(cv) and _version_tuple(cv) < _version_tuple(pv):
            out.append(_finding("fail", "AS026", f"{src} version", f"version went down from {pv} to {cv}"))
    return out


def check_permissions(expo: dict, src: str, deps: set[str]) -> list[dict]:
    out = []
    plist = (expo.get("ios") or {}).get("infoPlist") or {}
    plugins = _plugins(expo)
    for pkg, needs in sorted(PERMISSIONS.items()):
        if pkg not in deps:
            continue
        opts = plugins.get(pkg)
        for key, option, required in needs:
            text = plist.get(key) or (opts or {}).get(option)
            where = f"{src} ios.infoPlist.{key}"
            if isinstance(text, str) and text.strip():
                if VAGUE_PURPOSE.match(text) or len(text.strip()) < 25:
                    out.append(_finding("warn", "AS031", where, f"usage string for {pkg} does not say why: \"{text.strip()}\"",
                                        "say what the app does with it, e.g. \"Scan a receipt to add it to your expenses.\""))
                continue
            if opts is not None and required:
                out.append(_finding("warn", "AS032", where,
                                    f"{pkg} plugin is listed without `{option}`, so its generic default text ships",
                                    f"set `{option}` in the plugin options, or {key} in ios.infoPlist, to say why"))
            elif required:
                out.append(_finding("fail", "AS030", where, f"{pkg} is installed but {key} is missing",
                                    f"add {key} under ios.infoPlist (or `{option}` in the {pkg} plugin) saying why"))
            else:
                out.append(_finding("note", "AS033", where,
                                    f"{pkg} is installed; add {key} if the app uses that feature"))
    return out


def check_privacy_manifest(expo: dict, src: str, deps: set[str]) -> list[dict]:
    out = []
    pm = (expo.get("ios") or {}).get("privacyManifests")
    where = f"{src} ios.privacyManifests"
    if not pm:
        out.append(_finding("warn", "AS040", where, "no privacy manifest entries in the app config",
                            "declare NSPrivacyAccessedAPITypes for required-reason APIs your code and libraries use "
                            "(React Native itself uses UserDefaults, file timestamps and boot time)"))
        return out
    if not isinstance(pm, dict):
        return [_finding("fail", "AS041", where, "privacyManifests must be an object")]
    for i, entry in enumerate(pm.get("NSPrivacyAccessedAPITypes") or []):
        if not isinstance(entry, dict):
            out.append(_finding("fail", "AS041", f"{where}.NSPrivacyAccessedAPITypes[{i}]", "entry must be an object"))
            continue
        cat = entry.get("NSPrivacyAccessedAPIType")
        reasons = entry.get("NSPrivacyAccessedAPITypeReasons") or []
        if cat not in API_CATEGORIES:
            out.append(_finding("fail", "AS042", f"{where}.NSPrivacyAccessedAPITypes[{i}]",
                                f"unknown API category `{cat}`", "check the category name against Apple's list"))
        if not reasons or not all(isinstance(r, str) and REASON_CODE.match(r) for r in reasons):
            out.append(_finding("fail", "AS043", f"{where}.NSPrivacyAccessedAPITypes[{i}]",
                                f"reasons for `{cat}` are missing or not codes like CA92.1"))
    if "expo-tracking-transparency" in deps and pm.get("NSPrivacyTracking") is not True:
        out.append(_finding("warn", "AS044", where, "the app asks for tracking permission but NSPrivacyTracking is not true",
                            "set NSPrivacyTracking and list NSPrivacyTrackingDomains, or drop the tracking prompt"))
    return out


def check_assets(expo: dict, src: str, root: Path) -> list[dict]:
    out = []
    ios = expo.get("ios") or {}
    icon = ios.get("icon") if isinstance(ios.get("icon"), str) else expo.get("icon")
    if not icon:
        out.append(_finding("fail", "AS050", f"{src} icon", "no app icon", "set `icon` to a 1024x1024 PNG with no transparency"))
    elif not re.match(r"^https?://", icon) and not icon.endswith(".icon"):
        path = root / icon
        if not path.is_file():
            out.append(_finding("fail", "AS051", f"{src} icon", f"icon file `{icon}` not found"))
        else:
            info = _png_info(path)
            if info is None:
                out.append(_finding("warn", "AS052", f"{src} icon", f"`{icon}` is not a PNG"))
            else:
                w, h, alpha = info
                if (w, h) != (1024, 1024):
                    out.append(_finding("warn", "AS053", f"{src} icon", f"icon is {w}x{h}; use 1024x1024"))
                if alpha:
                    out.append(_finding("warn", "AS054", f"{src} icon", "icon PNG has an alpha channel",
                                        "export it without transparency; the store icon must be opaque"))
    plugins = _plugins(expo)
    if "splash" not in expo and "expo-splash-screen" not in plugins:
        out.append(_finding("warn", "AS055", f"{src} plugins", "no splash screen set",
                            "add the expo-splash-screen plugin with an image and background colour"))
    cfg = ios.get("config") or {}
    plist = ios.get("infoPlist") or {}
    if "usesNonExemptEncryption" not in cfg and "ITSAppUsesNonExemptEncryption" not in plist:
        out.append(_finding("warn", "AS056", f"{src} ios.config.usesNonExemptEncryption",
                            "encryption use is not declared, so App Store Connect asks about it on every build",
                            "set ios.config.usesNonExemptEncryption (false when the app only uses HTTPS and OS crypto)"))
    if ios.get("supportsTablet"):
        out.append(_finding("note", "AS057", f"{src} ios.supportsTablet",
                            "the app runs on iPad, so the listing needs iPad screenshots too"))
    return out


def check_eas(eas: dict | None, deps: set[str], expo: dict, src: str) -> list[dict]:
    out = []
    if eas is None:
        return [_finding("warn", "AS060", "eas.json", "no eas.json", "run `eas build:configure`, then review the profiles")]
    build = eas.get("build") or {}
    for name in ("development", "preview", "production"):
        if name not in build:
            out.append(_finding("warn" if name == "production" else "note", "AS061", f"eas.json build.{name}",
                                f"no `{name}` build profile"))
    prod = build.get("production") or {}
    if prod.get("distribution") == "internal" or prod.get("developmentClient"):
        out.append(_finding("fail", "AS062", "eas.json build.production",
                            "the production profile is set up for internal or development builds, which cannot go to the store"))
    if (prod.get("ios") or {}).get("simulator"):
        out.append(_finding("fail", "AS063", "eas.json build.production.ios.simulator", "production builds for the simulator"))
    dev = build.get("development")
    if isinstance(dev, dict) and dev and not dev.get("developmentClient"):
        out.append(_finding("note", "AS064", "eas.json build.development", "development profile has no developmentClient"))
    ios_submit = (((eas.get("submit") or {}).get("production") or {}).get("ios") or {})
    if not ios_submit.get("ascAppId"):
        out.append(_finding("note", "AS065", "eas.json submit.production.ios.ascAppId",
                            "no ascAppId; `eas submit` will ask which app to use",
                            "add the numeric Apple ID from App Store Connect > App Information"))
    if "expo-updates" in deps:
        rv = expo.get("runtimeVersion") or (expo.get("ios") or {}).get("runtimeVersion")
        if not rv:
            out.append(_finding("warn", "AS066", f"{src} runtimeVersion",
                                "expo-updates is installed but no runtimeVersion is set",
                                'use {"policy": "fingerprint"} so an update never reaches a build with different native code'))
        elif isinstance(rv, str):
            out.append(_finding("note", "AS067", f"{src} runtimeVersion",
                                f"runtimeVersion is a fixed string `{rv}`; change it by hand after every native change"))
        channels = [p for p in ("preview", "production") if isinstance(build.get(p), dict) and not build[p].get("channel")]
        if channels:
            out.append(_finding("warn", "AS068", "eas.json build", f"no update channel on: {', '.join(channels)}",
                                "give each store profile a channel so updates reach the right builds"))
    return out


def check_store_listing(root: Path, eas: dict | None) -> list[dict]:
    """Privacy and support URLs live in App Store Connect; in the repo only when EAS Metadata is used."""
    meta = ((((eas or {}).get("submit") or {}).get("production") or {}).get("ios") or {}).get("metadataPath", "store.config.json")
    path = root / meta
    if not path.is_file():
        return [_finding("warn", "AS070", meta, "no privacy policy URL found in the repo",
                         "set it in App Store Connect (App Privacy), or keep the listing in store.config.json "
                         "with EAS Metadata; the app must also link to it from inside")]
    data = _load_json(path)
    info = ((data.get("apple") or {}).get("info")) or {}
    out = []
    if not info:
        return [_finding("warn", "AS071", meta, "no apple.info block, so no privacy or support URL")]
    for locale, block in info.items():
        if not isinstance(block, dict):
            continue
        for key, code in (("privacyPolicyUrl", "AS072"), ("supportUrl", "AS073")):
            url = block.get(key)
            if not url:
                out.append(_finding("fail" if key == "privacyPolicyUrl" else "warn", code,
                                    f"{meta} apple.info.{locale}.{key}", f"no {key}"))
            elif not str(url).startswith("https://"):
                out.append(_finding("warn", code, f"{meta} apple.info.{locale}.{key}", f"{key} is not https"))
        for key, limit in (("title", 30), ("subtitle", 30), ("promoText", 170), ("description", 4000)):
            val = block.get(key)
            if isinstance(val, str) and len(val) > limit:
                out.append(_finding("fail", "AS074", f"{meta} apple.info.{locale}.{key}",
                                    f"{key} is {len(val)} characters; the limit is {limit}"))
        kw = block.get("keywords")
        if isinstance(kw, list):
            joined = ",".join(kw)
            if len(joined.encode("utf-8")) > 100:
                out.append(_finding("fail", "AS075", f"{meta} apple.info.{locale}.keywords",
                                    f"keywords take {len(joined.encode('utf-8'))} bytes; the limit is 100"))
    return out


def check_policy_risks(deps: set[str]) -> list[dict]:
    out = []
    if deps & THIRD_PARTY_LOGIN and not deps & APPLE_LOGIN:
        out.append(_finding("warn", "AS080", "package.json",
                            "third-party sign-in without an Apple sign-in package",
                            "Guideline 4.8 asks for an equivalent private sign-in option; Sign in with Apple is the usual one"))
    if deps & WEB_PAYMENT_LIBS and not deps & IAP_LIBS:
        out.append(_finding("note", "AS081", "package.json",
                            "card payments without an in-app purchase library",
                            "fine for physical goods and services; digital content and features need in-app purchase (3.1.1)"))
    return out


def _walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield Path(dirpath) / name


def check_secrets(root: Path, files: list[str], eas: dict | None) -> list[dict]:
    out = []
    for path in _walk(root):
        if path.suffix.lower() in SIGNING_SUFFIXES:
            out.append(_finding("fail", "AS090", str(path.relative_to(root)),
                                "signing key or certificate file inside the project",
                                "move it out and let EAS manage credentials; if it was ever committed, revoke it"))
    for name in files:
        path = root / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for rx, what in SECRET_PATTERNS:
            if rx.search(text):
                out.append(_finding("fail", "AS091", name, f"looks like {what}",
                                    "remove it; use EAS environment variables or secrets, and revoke the old value"))
    for pname, prof in (((eas or {}).get("build")) or {}).items():
        env = (prof or {}).get("env") if isinstance(prof, dict) else None
        for key, val in (env or {}).items():
            if SECRET_NAME.search(key) and isinstance(val, str) and val and not val.startswith("$"):
                level = "fail" if not key.startswith("EXPO_PUBLIC_") else "warn"
                out.append(_finding(level, "AS092", f"eas.json build.{pname}.env.{key}",
                                    f"`{key}` has a literal value in eas.json"
                                    + (" and EXPO_PUBLIC_ values ship inside the app" if level == "warn" else ""),
                                    "store it as an EAS environment variable with secret visibility"))
    for pname, prof in (((eas or {}).get("submit")) or {}).items():
        ios = (prof or {}).get("ios") if isinstance(prof, dict) else None
        key_path = (ios or {}).get("ascApiKeyPath")
        if key_path and not os.path.isabs(key_path) and (root / key_path).exists():
            out.append(_finding("fail", "AS093", f"eas.json submit.{pname}.ios.ascApiKeyPath",
                                "the App Store Connect API key file is inside the project",
                                "keep the .p8 outside the repo or let `eas credentials` store it"))
    return out


def check(root: Path, config: str | None = None, since: str | None = None) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise BadInput(f"not a folder: {root}")
    expo, src, findings = load_app_config(root, config)
    eas_path = root / "eas.json"
    eas = _load_json(eas_path) if eas_path.is_file() else None
    deps = _deps(root)
    if not (deps & {"expo", "react-native"}) and (root / "package.json").is_file():
        findings.append(_finding("note", "AS003", "package.json", "neither expo nor react-native is a dependency"))
    prev = _git_show(root, since, src) if since else None
    if since and prev is None:
        findings.append(_finding("note", "AS027", src, f"could not read {src} at `{since}`; build number not compared"))
    findings += check_identity(expo, src)
    findings += check_versions(expo, src, eas, prev)
    findings += check_permissions(expo, src, deps)
    findings += check_privacy_manifest(expo, src, deps)
    findings += check_assets(expo, src, root)
    findings += check_eas(eas, deps, expo, src)
    findings += check_store_listing(root, eas)
    findings += check_policy_risks(deps)
    findings += check_secrets(root, [src, "eas.json", "store.config.json", "app.config.resolved.json"], eas)
    findings.sort(key=lambda f: (LEVELS.index(f["level"]), f["code"]))
    counts = {lvl: sum(1 for f in findings if f["level"] == lvl) for lvl in LEVELS}
    return {"root": str(root), "config": src, "counts": counts, "findings": findings}


def format_text(report: dict) -> str:
    lines = []
    for f in report["findings"]:
        lines.append(f"{f['level']:<4} {f['code']} {f['where']}: {f['message']}")
        if f["fix"]:
            lines.append(f"     fix: {f['fix']}")
    c = report["counts"]
    lines.append(f"appstore check: {c['fail']} fail, {c['warn']} warn, {c['note']} note ({report['config']})")
    return "\n".join(lines)


def cmd_appstore(args, out=sys.stdout) -> int:
    try:
        report = check(Path(args.root), args.config, args.since)
    except BadInput as e:
        print(f"appstore check: {e}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2) if args.json else format_text(report), file=out)
    return 1 if report["counts"]["fail"] or report["counts"]["warn"] else 0


def register(sub):
    p = sub.add_parser("appstore", help="App Store readiness checks for an Expo app (offline)")
    s = p.add_subparsers(dest="what", required=True)
    c = s.add_parser("check", help="read app.json, eas.json, package.json and report missing or risky items")
    c.add_argument("--root", default=".")
    c.add_argument("--config", help="app config JSON to read instead of app.json (e.g. output of `npx expo config --json`)")
    c.add_argument("--since", help="git ref to compare version and build number against, e.g. the last released tag")
    c.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_appstore)
