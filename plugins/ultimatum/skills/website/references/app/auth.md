# Sign-in and accounts

Read this when an app has accounts. Examples use Supabase Auth with Next.js and `@supabase/ssr`; check the current guide at https://supabase.com/docs/guides/auth/server-side before relying. The flows are the same with other providers.

## Flows to build, each tested end to end

| Flow | Done when |
|---|---|
| Sign up | confirmation email arrives, the link signs the user in, a `profiles` row exists |
| Sign in with password | wrong password and unknown email show the same message |
| Magic link or one-time code | the link works once and expires |
| Google or Apple | redirect returns to the page the user started from |
| Forgot password | the reset link opens a set-password page; the old password stops working |
| Sign out | server session ends; back button shows no private page |
| Change email | confirmation goes to the new address |
| Delete account | data removed or anonymised as the privacy page says; Stripe customer handled |
| Roles | a member cannot open staff or admin pages or call their endpoints |

## Clients

One client for the browser (publishable key) and one for the server that reads and writes the session cookies. Middleware refreshes the session on each request so server components see a current user.

```ts
// src/lib/supabase/server.ts
import { cookies } from "next/headers";
import { createServerClient } from "@supabase/ssr";

export async function serverClient() {
  const store = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    {
      cookies: {
        getAll: () => store.getAll(),
        setAll: (list) => {
          try {
            list.forEach(({ name, value, options }) => store.set(name, value, options));
          } catch {
            // called from a server component; middleware refreshes the cookies instead
          }
        },
      },
    },
  );
}
```

## Trust on the server

- Protect pages and API routes on the server. Hiding a link in the browser is not a guard.
- On the server, get the user with `supabase.auth.getUser()` (or `getClaims()`), which verifies the token. `getSession()` reads the cookie without checking it, so never base access on it.
- Row-level security is the last line: even if a route forgets a check, the database refuses other users' rows.

```ts
// src/app/account/page.tsx
import { redirect } from "next/navigation";
import { serverClient } from "@/lib/supabase/server";

export default async function AccountPage() {
  const supabase = await serverClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/sign-in?next=/account");
  const { data: bookings } = await supabase.from("bookings").select("id, starts_at").order("starts_at");
  return <BookingList items={bookings ?? []} />;
}
```

## Five checks before an AI-written login ships

Generated sign-in code usually works on the happy path and fails these. Run each one, against the preview URL, before the flows table counts as done.

1. **No secret key in the code.** Only the publishable key belongs in the browser. The secret key (`sb_secret_...`, the old `service_role`), Stripe's `sk_` keys and AI provider keys live in server environment variables, never behind a `NEXT_PUBLIC_` or `VITE_` prefix, never in a commit. Test: run the two secret searches in `checklist.md` on the history and the built JS. A hit means the owner rotates the key now; deleting the line is not enough.
2. **The server decides.** Who the user is comes from the server (`supabase.auth.getUser()` in server code), not from a user id, role, plan or price sent by the browser or kept in `localStorage`. Hiding a button protects nothing. Every API route and server action checks the user and their right to this record. Test: as user A, call the endpoint directly (curl or the browser console) with user B's record id and with `role: "admin"` in the body; expect 401, 403 or 404 and no change.
3. **Every table locked.** Row-level security on for every exposed table, with a policy per action. Test: the second-user test and the SQL check in `supabase.md`; also try the publishable key from the console against each table while signed out.
4. **Sign-out that really signs out.** Sign-out runs on the server and clears the session cookies; client caches of private data (query caches, service-worker caches) are cleared too; private pages send `Cache-Control: no-store`. Offer "sign out everywhere" (Supabase: `signOut({ scope: "global" })`) and use it after a password change. Access tokens stay valid until they expire, so keep the expiry short; confirm the provider's default. Test: copy the session cookie, sign out, replay a request with the old cookie, and press Back; neither shows private data.
5. **One error message.** Wrong password and unknown email give the same text; so do sign-up with a taken email ("Check your email to continue") and password reset ("If that address has an account, we've sent a link"). Never show the provider's raw error. Test: compare the responses for a real and a made-up email; status, body and rough timing match.

## Redirects and OAuth

- Add the live and preview URLs to the allowed redirect list in the auth settings; never accept an arbitrary `next=` URL. Only allow paths that start with a single `/`.
- OAuth and magic links return a `code`; a callback route exchanges it with `exchangeCodeForSession(code)` and then redirects.
- Google and Apple need their own developer-console setup, done by the owner in their accounts.

## Abuse and privacy

- The same message for "no such email" and "wrong password", and for password-reset requests.
- Turn on CAPTCHA for sign-up and reset if bots appear; keep the provider's rate limits.
- Minimum password length and leaked-password checks where the provider offers them.
- Roles come from your table or `app_metadata`, checked on the server and in row-level security.
- Account deletion runs on the server with the secret key (`auth.admin.deleteUser`), after deleting or anonymising the user's rows and cancelling any subscription.

## Tests

For each role, a test that a lower role gets 401, 403 or 404 on every protected route and gets zero rows from the database. Add one test per bug found.
