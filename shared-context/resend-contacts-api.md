---
created: 2026-05-18 20:05
tags:
aliases:
---

# Resend Contacts & Audiences API

Researched 2026-05-18 against Resend SDK v6.x. Updated same day after production testing.

---

## Architecture shift: Audiences → Global Contacts

Resend has migrated from audience-scoped contacts to a **global contacts model**. Contacts are now first-class entities; audiences have been rebranded as "Segments." The `audienceId` parameter in `contacts.create()` is backward-compatible but no longer required.

References:
- https://resend.com/docs/api-reference/contacts/create-contact
- https://resend.com/blog/new-contacts-experience

---

## contacts.create() — current signature

```ts
const { data, error } = await resend.contacts.create({
  email: "user@example.com",      // required
  firstName: "Steve",             // optional
  lastName: "Wozniak",            // optional
  unsubscribed: false,            // optional, global subscription status
  properties: { key: "value" },  // optional custom key-value pairs
  segments: [{ id: "uuid" }],    // optional — replaces audienceId in new model
  // audienceId: "uuid"           // backward-compat only, not needed in new model
});
```

**Minimal working call (no audience/segment needed):**

```ts
await resend.contacts.create({ email, unsubscribed: false });
```

**Always destructure the return value** — the SDK never throws on API errors; it returns them in the `error` field. Awaiting without destructuring silently swallows failures.

```ts
// ❌ silent failure — looks like 200, nothing happened
await resend.contacts.create({ email, unsubscribed: false });

// ✅ check the error
const { data, error } = await resend.contacts.create({ email, unsubscribed: false });
if (error) {
  console.error(error); // e.g. 401 restricted_api_key
  return NextResponse.json({ error: "Failed to subscribe" }, { status: 500 });
}
```

---

## API key permissions (gotcha)

Resend has two API key types:

| Type | contacts.create() | emails.send() |
|---|---|---|
| **Sending access** | ❌ 401 `restricted_api_key` | ✅ |
| **Full access** | ✅ | ✅ |

If contacts are being silently skipped (200 returned but nothing in dashboard), the key is likely "Sending access" only. Create a **Full access** key at resend.com/api-keys.

---

## `onboarding@resend.dev` sender restriction

The default test sender can **only deliver to the Resend account owner's email**. Emails to any other recipient are silently dropped — no error, no bounce.

To send to real subscribers, a verified domain is required.

---

## Domain verification for sending

- Each Resend account verifies its own domain at resend.com/domains
- Subdomains work and are independent — `learner1.yourdomain.com` and `learner2.yourdomain.com` can each be verified on separate Resend accounts without conflict
- Each subdomain gets its own DKIM keys and DNS records
- Useful pattern for workshops: instructor owns the root domain, adds DNS records per learner subdomain on request

---

## Finding an Audience/Segment ID

The Resend dashboard at `https://resend.com/audience` does not show the UUID in the URL on the list page. Two ways to get it:

**Option A — API:**
```ts
const { data } = await resend.audiences.list();
// data.data[0].id → "78261eea-8f8b-4381-83c6-79fa7120f1cf"
```

**Option B — Dashboard:** Click into a specific audience; the UUID appears in the URL once inside the detail view.

---

## Lazy client instantiation (important for Next.js)

Do NOT instantiate `new Resend(...)` at module level in a Next.js App Router route. It will throw during `next build` when the env var is absent.

```ts
// ❌ module level — breaks build
const resend = new Resend(process.env.RESEND_API_KEY);

// ✅ inside the handler — lazy init
export async function POST(req: NextRequest) {
  const resend = new Resend(process.env.RESEND_API_KEY);
  // ...
}
```

Also add `export const dynamic = "force-dynamic"` to prevent static optimization of the route.

---

## Required env vars for the subscribe route

| Var | Required | Notes |
|---|---|---|
| `RESEND_API_KEY` | yes | must be **Full access**, not "Sending access" |
| `RESEND_FROM_EMAIL` | yes (production) | must be a verified domain address; `onboarding@resend.dev` only works for the account owner |
| `RESEND_AUDIENCE_ID` | no | only needed if using segments/audienceId param |
