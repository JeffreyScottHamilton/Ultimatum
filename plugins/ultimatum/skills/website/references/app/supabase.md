# Supabase: data, access rules and migrations

Read this when an app stores data. Docs: https://supabase.com/docs (check current names and commands before relying; Supabase renamed its API keys in 2025).

## Keys

| Key | Old name | Where it may go |
|---|---|---|
| Publishable key (`sb_publishable_...`) | anon key | browser code; safe only because row-level security limits it |
| Secret key (`sb_secret_...`) | service_role key | server code only; it **skips** row-level security |

If a secret key ever reaches the browser, a commit or a log, ask the owner to rotate it in the dashboard at once.

## Plan the data model

For each table write four things before any SQL: what one row is, who owns it (usually `user_id uuid references auth.users`), who may read it, who may change it. Keep roles in your own table or in `app_metadata`, never in `user_metadata`, which the user can edit.

Typical tables:
- `profiles` (one per user, created by a trigger on sign-up).
- The thing the app is about (`bookings`, `projects`, `orders`).
- `customers` linking a user to a Stripe customer id.
- `subscriptions` mirroring Stripe status, written only by the webhook.

## Row-level security

Turn it on for every table in an exposed schema (`public` by default). Tables made in the dashboard's table editor have it on; tables made with SQL do not until you say so. With it on and no policy, nobody but the secret key can see a row.

```sql
create table public.bookings (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  starts_at timestamptz not null,
  note text,
  created_at timestamptz not null default now()
);
create index bookings_user_id_idx on public.bookings (user_id);

alter table public.bookings enable row level security;

create policy "members read their bookings" on public.bookings
  for select to authenticated
  using ((select auth.uid()) = user_id);

create policy "members add their own bookings" on public.bookings
  for insert to authenticated
  with check ((select auth.uid()) = user_id);

create policy "members change their own bookings" on public.bookings
  for update to authenticated
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);
```

Rules:
- One policy per action (`select`, `insert`, `update`, `delete`). `update` needs both `using` (which rows) and `with check` (what they may become), or a user can move a row to someone else.
- Write `(select auth.uid())` rather than bare `auth.uid()` so Postgres runs it once per query; index every column a policy filters on.
- Name the role (`to authenticated`). Add `to anon` only for truly public rows.
- Views skip row-level security unless created `with (security_invoker = true)`.
- `security definer` functions run as their owner: keep them in a schema the API does not expose, set `search_path = ''`, and check the caller inside.
- Tables only the server writes (subscriptions, audit logs) get a `select` policy for the owner and no write policy; the webhook writes with the secret key.
- Storage: keep buckets private, add policies on `storage.objects` keyed to a folder per user, and hand out signed URLs for downloads.

## The second-user test

Every table gets this test before go-live, and again after each policy change:
1. Create users A and B. Sign in as A with the publishable key.
2. A inserts a row; reading it back works.
3. A reads B's rows: zero rows come back.
4. A inserts a row with `user_id` set to B: refused.
5. A updates or deletes B's row: no rows change.
6. Signed out (anon): zero rows, unless the brief says the table is public.

Automate it with pgTAP through `supabase test db`, or with a script that signs in two test users against the local stack. A test that passes with row-level security turned off is not testing anything; check that it fails when you disable it once.

## Migrations

All schema changes live in Git as migration files; nobody edits the live schema by hand.

```bash
supabase init                          # once, creates supabase/
supabase start                         # local stack in Docker
supabase migration new create_bookings # new file in supabase/migrations/
supabase db reset                      # rebuild local from all migrations and seed.sql
supabase test db                       # run pgTAP tests in supabase/tests/
supabase gen types typescript --local > src/lib/database.types.ts
supabase link --project-ref <ref>      # the owner runs this; it needs their login
supabase db push                       # apply new migrations to the linked project
```

`db push` changes the live database: run it only after the data-model approval and on the owner's yes. Back up first on a paid plan, or export the data. Destructive changes (dropping a column, changing a type) need their own plain-words warning.

## Before real users

- Every exposed table has row-level security on: `select relname from pg_class join pg_namespace n on n.oid = relnamespace where nspname = 'public' and relkind = 'r' and not relrowsecurity;` returns nothing.
- The dashboard's security and performance advisors show no open warnings.
- Point-in-time recovery or backups: check what the plan includes (check before relying).
- Email: set a custom SMTP sender; the built-in one is rate-limited and meant for testing.
