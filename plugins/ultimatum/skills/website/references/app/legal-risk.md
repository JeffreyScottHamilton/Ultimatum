# Legal-risk pass before launch

Read before the go-live gate for any site that collects data, takes money, runs ads or tracking, or uses an AI provider. Pair it with `checklist.md`; this file covers the claims people most often get into trouble over.

This is a risk check, not legal advice. Rules differ by country and state; where a row names a law, it is an example of the kind of rule to look up for the places the owner's users live. When the stakes are real (children, health, money, ID documents), tell the owner to have a lawyer read the privacy page and terms.

Each step ends in evidence: a command and its result, a screenshot, or a file and line. Unchecked steps go in the launch report as open, never as done.

## 1. Know what data you hold (do this first; the rest depends on it)

1. Build a data map from the code, not from memory. Search the schema, migrations, form fields, API handlers, analytics calls and third-party SDKs:
   ```bash
   grep -rnE "insert|upsert|FormData|<input[^>]+name=|gtag|fbq|posthog|segment|sentry|stripe|resend|openai|anthropic" --include=*.{ts,tsx,js,jsx,py,sql,svelte,vue} .
   ```
   For each field record: what it is, why it is kept, where it is stored, which outside services receive it, and how long it stays.
2. Delete what you collect but never read. A field with no reader is risk with no benefit; ID photos, selfies, exact location, date of birth and contact lists first. Remove the form field, the column (migration), and any copy already stored.
3. Write the privacy page from the map: every outside service by name, what each receives, how long data is kept, how to get a copy, and how to delete the account. A privacy page that names fewer services than the code calls is the usual gap. Re-run step 1 after every new integration.

## 2. Users can leave, and their data goes with them

- A delete-account control the user can reach while signed in. It removes or anonymises their rows in every table from the map, their files in storage, and their records at outside services that offer a delete call (payments keep what tax law requires; say so on the privacy page).
- Test it: create a user with data in every table, delete the account, then query each table and bucket for that user's id. Nothing may come back except the rows the privacy page says are kept.

## 3. Strangers can't read other people's data

The public key in the browser is public. Assume anyone has it.

- Signed out, with only the public key, try to read and write each table and bucket (`supabase.md` has the second-user test; add an anonymous run). Every request for another user's rows must return nothing or an error.
- Signed in as user A, request user B's rows by id through the API and through storage URLs. Expect a refusal.
- Record each request and its result. If one succeeds, launch waits.

## 4. Children

If a child could plausibly use the product (games, school, homework, family, youth sport), treat users as possibly under 13 (in the US, COPPA; other places set other ages):
- no ad tracking or behavioural ads, no third-party analytics that profile, no public profiles or open chat;
- an age question that does not hint at the "right" answer; under-age users get a parent-consent step that a child cannot click through alone, or are kept out;
- the privacy page has a section for parents.
If the owner can't do this, say the product must be marked and enforced as 13+ (or 16+ where that is the rule) and launch only with their yes.

## 5. Subscriptions: leaving is as easy as joining

- Cancelling takes no more steps than signing up, online, without a call or chat (several places require this, for example California's automatic renewal law).
- Billing stops at the moment the plan says (end of period or immediately); a cancel webhook or Stripe's customer portal sets it, and a test cancel in test mode shows no further invoice.
- Before checkout, show the price, the renewal period, when the trial converts, and how to cancel. Send a receipt that repeats them.

## 6. No tracking before a yes

Where users are in the EU, UK or similar places, ad pixels and non-essential analytics may run only after the visitor agrees.
- Load the Meta pixel, Google Analytics/Ads, TikTok and similar scripts only after consent; "reject" is as easy to find as "accept".
- Check it: open the site in a fresh private window, decline or ignore the banner, and look at the Network tab (or a Playwright run filtering requests). No request may reach `facebook.com/tr`, `google-analytics.com`, `googletagmanager.com` or the like. Record the request list.
- In the US, honour the opt-out a state requires (for example a "Do not sell or share" link and the Global Privacy Control signal in California).

## 7. The name is free to use

Before the owner buys the domain or prints anything:
- search the trademark registers for the name and close variants in the classes that fit the business (USPTO search in the US, EUIPO TMview for the EU and many national offices, UK IPO, and the owner's own country);
- search the app stores and the web for the same name in the same trade.
A clash in the same trade means pick another name; say so plainly. Report what was searched and when; a search is not legal clearance.

## 8. Keys stay on the server, and spending has a ceiling

- Find keys in the frontend and its history:
  ```bash
  git log -p | grep -nE "sk-[A-Za-z0-9]|sk_live|sk_test|sb_secret|service_role|AIza[0-9A-Za-z_-]{20,}|whsec_"
  ```
  and search the built JS bundle for the same patterns. Anything found moves to a server route or edge function, and the key is rotated (a key that was ever public is burned).
- Every AI and paid API call goes through the server with a per-user rate limit and a size limit on input.
- Set a hard monthly budget or usage limit in each AI provider's console and a billing alert below it. Record the limit set.

## 9. Uploads and user text can't attack other users

- File uploads: allowlist extensions and check the content, cap the size, store under a generated name in object storage (not the app's web root), never execute uploads (no `.php`, `.jsp`, `.html`, `.svg` served as pages), and serve them with `Content-Disposition` and `X-Content-Type-Options: nosniff`. Upload a renamed script as a test; it must be refused or served as a download.
- User text: rely on the framework's escaping; any raw HTML (`dangerouslySetInnerHTML`, `v-html`, `{@html}`, `innerHTML`) goes through a sanitiser and has a test with `<img src=x onerror=alert(1)>`. Add a Content-Security-Policy without `unsafe-inline` scripts where the stack allows.
- Payment webhooks verify the signature and are idempotent (see `stripe.md`).
The deeper rules are in the Work skill's `security/secure-implementation.md`.

## 10. Everything you didn't make has a licence you follow

List fonts, images, icons, music, video, code snippets and packages that ship with the site, each with its licence and source. Check `../shared/licenses.md` for what each common licence asks (attribution, notice files, no resale). Drop anything with no licence or one that forbids the use; AI-generated assets follow the generator's terms.

## Report

Add a "Legal risk" block to the launch report: the ten steps, each marked done (with its evidence), not applicable (with why), or open. Open items in steps 2, 3, 6 or 8 block the publish gate until the owner decides in their own words.
