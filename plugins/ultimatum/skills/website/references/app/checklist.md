# App go-live checklist

Run after `../launch-checklist.md`, for sites with accounts, data or payments. Tick each with evidence.

## Data
- [ ] Data model approved: `ult gate check data-model` passes (the migration hasn't changed since).
- [ ] Row-level security on for every exposed table; the SQL check in `supabase.md` returns nothing.
- [ ] The second-user test passes for every table, and fails once with row-level security turned off.
- [ ] Migrations in Git; live schema matches them (`supabase db diff` shows nothing unexpected).
- [ ] Backups or export plan confirmed for the plan the owner pays for.

## Sign-in
- [ ] Every flow in `auth.md` tested on the preview URL, on a phone and a desktop.
- [ ] Each protected page and API route refuses a signed-out user and a lower role.
- [ ] Redirect allowlist holds only the live and preview URLs; `next=` accepts paths only.
- [ ] Custom SMTP sender set; confirm and reset emails land in the inbox, not spam.

## Payments
- [ ] Test-mode walkthrough from `stripe.md` done, including a failed renewal and a refund.
- [ ] Webhook signature check refuses a forged event (send one with a wrong signature: 400).
- [ ] Prices come from server config; changing the amount in the browser changes nothing.
- [ ] Refund, cancellation and contact details on the site.
- [ ] Live payments approved (`ult gate check live-payments`), switch done, one real purchase refunded, gate closed.

## Secrets and privacy
- [ ] `git log -p | grep -E "sk_live|sk_test|sb_secret|whsec_|service_role"` finds nothing.
- [ ] Browser bundle contains no secret key (search the built JS for the same patterns).
- [ ] Privacy page lists what is stored, why, how long, and how to delete an account; account deletion works.
- [ ] Security review on the sign-in, data and payment code with the Work skill's security guides; no open high findings.
