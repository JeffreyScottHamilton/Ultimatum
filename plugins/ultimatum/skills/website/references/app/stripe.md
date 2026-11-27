# Stripe payments

Read this when an app takes money. Docs: https://docs.stripe.com (check current API versions, fees and rules before relying). Everything runs in test mode until `ult gate approve live-payments`.

## Pick the integration

| Need | Use |
|---|---|
| A fixed price, no code | Payment Link |
| Pay on our site with Stripe's hosted page | Checkout Session (`mode: "payment"`) |
| Subscriptions | Checkout Session (`mode: "subscription"`) plus the customer portal |
| Card form inside our own page | Payment Element with a PaymentIntent or Checkout in embedded mode |

Hosted Checkout is the default: it handles cards, wallets, 3D Secure, tax collection and receipts with the least code.

## Products and prices

Create products and prices in the Stripe dashboard (or a seed script) and keep their price ids in config. The browser sends which plan the user picked; the server maps it to a price id. **Never take an amount or a price id straight from the browser.**

## Start a checkout (server only)

```ts
// src/app/api/checkout/route.ts
import Stripe from "stripe";
import { serverClient } from "@/lib/supabase/server";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const PLANS: Record<string, string> = {
  monthly: process.env.STRIPE_PRICE_MONTHLY!,
  yearly: process.env.STRIPE_PRICE_YEARLY!,
};

export async function POST(req: Request) {
  const supabase = await serverClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return new Response("Sign in first", { status: 401 });

  const { plan } = await req.json();
  const price = PLANS[plan];
  if (!price) return new Response("Unknown plan", { status: 400 });

  const site = process.env.SITE_URL!;
  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    line_items: [{ price, quantity: 1 }],
    client_reference_id: user.id,
    customer_email: user.email,
    success_url: `${site}/account?checkout={CHECKOUT_SESSION_ID}`,
    cancel_url: `${site}/pricing`,
  });
  return Response.json({ url: session.url });
}
```

Reuse the user's Stripe customer id (`customer:`) once one exists, so they get a single billing history.

## Webhooks: the source of truth

The success page only says "thanks, we're confirming". Access changes when a verified webhook arrives.

```ts
// src/app/api/stripe/webhook/route.ts
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const body = await req.text(); // raw body: parsing JSON first breaks the signature
  const signature = req.headers.get("stripe-signature") ?? "";
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch {
    return new Response("Bad signature", { status: 400 });
  }
  if (await alreadyHandled(event.id)) return new Response("ok");

  switch (event.type) {
    case "checkout.session.completed":
    case "customer.subscription.created":
    case "customer.subscription.updated":
    case "customer.subscription.deleted":
    case "invoice.paid":
    case "invoice.payment_failed":
      await syncFromStripe(event); // re-read the object from Stripe, then upsert our row
      break;
  }
  await markHandled(event.id);
  return new Response("ok");
}
```

Rules:
- Verify every event's signature; reject the rest with 400.
- Events can come twice and out of order: store handled event ids, and on each event fetch the current subscription from Stripe instead of trusting the order.
- Reply 2xx quickly; do slow work after recording the event.
- Write with the Supabase secret key on the server; members only read their own `subscriptions` row.
- Grant access while the status is `active` or `trialing`; decide in the brief what `past_due` gets.
- Payment methods that settle later (bank debits) send `checkout.session.async_payment_succeeded` or `..._failed`: fulfil on success, not on `completed`.

## Customer portal

Let subscribers change plan, update the card, see invoices and cancel through the portal: configure it in the dashboard, then create a session on the server with `stripe.billingPortal.sessions.create({ customer, return_url })` and redirect.

## Test before going live

```bash
stripe login                                        # the owner's own login
stripe listen --forward-to localhost:3000/api/stripe/webhook   # prints a test signing secret
stripe trigger checkout.session.completed
stripe trigger invoice.payment_failed
```

Test cards (check the current list in Stripe's testing docs): `4242 4242 4242 4242` succeeds, `4000 0025 0000 3155` asks for 3D Secure, `4000 0000 0000 0002` is declined. Any future date and any CVC.

Walk through: subscribe, see access, cancel in the portal, lose access at period end, fail a renewal, refund one payment.

## Going live (only after the live-payments approval)

1. The owner finishes Stripe's account activation (business details, bank account).
2. Recreate products, prices, the portal settings and the webhook endpoint in live mode; the live webhook has its own signing secret.
3. The owner pastes the live keys and secret into the host's production environment variables. Test keys stay in preview.
4. One real small purchase by the owner, then a refund (`stripe.refunds.create({ payment_intent })` or the dashboard).
5. Turn on email receipts, set the statement descriptor and support email, and add refund and cancellation terms to the site.
6. `ult gate done live-payments`.

Sales tax and VAT: Stripe Tax, a merchant of record, or the owner's accountant. Rules depend on the country; never guess, ask the owner who handles it.
