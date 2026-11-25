import os


def root() -> str:
    return os.environ.get("UPLOAD_ROOT", os.path.join(os.getcwd(), "data"))


def user_dir(user: str) -> str:
    path = os.path.join(root(), user)
    os.makedirs(path, exist_ok=True)
    return path


def valid_name(name) -> bool:
    return isinstance(name, str) and 0 < len(name) <= 100 and "/" not in name and "\\" not in name and not name.startswith(".")


def save(user: str, name: str, content: str) -> None:
    with open(os.path.join(user_dir(user), name), "w", encoding="utf-8") as fh:
        fh.write(content)


def list_names(user: str) -> list:
    return sorted(os.listdir(user_dir(user)))
