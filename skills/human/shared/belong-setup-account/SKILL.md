---
name: belong-setup-account
description: Guide a Service Provider human or buyer-side human through Belong account onboarding. Use for OAuth-style login, Belong Account creation, Organization Profile setup, account ownership, role context, notification preferences such as email/Slack/WhatsApp, required Stripe connection for payment readiness, legal/signing readiness, required Calendly connection (plus optional Google Calendar) for scheduling Human-to-Human Meetings, and routing into Buying Agent or Selling Agent training.
---

# Belong Setup Account

Use this for the Setup phase before any Buying Agent or Selling Agent training, and to manage an existing Belong Account.

## Prerequisites

Before setup, the human needs two external accounts ready, since both are connected
during onboarding:

- Stripe — for payment readiness (charges, holds, releases, payouts). Sign up at
  https://dashboard.stripe.com/register
- Calendly — required for scheduling Human-to-Human Meetings, so agents can expose
  real-time availability and auto-create the video join link. Sign up at
  https://calendly.com/signup

If the human does not have one of these yet, share the matching link first: "To set up
your Belong account, you need a Stripe account and a Calendly account. If you don't have
one yet, here is where you can register: <link>." Confirm both are ready before running
`setup-account`.

## Returning Human

If an account already exists for this human, do not treat setup as new. Re-running setup is additive: it adds a role (for example, a buyer who now also sells), adds an organization, and unions notification channels onto the existing account. Confirm whether the human is adding a role, organization, or channel rather than starting over.

To change rather than add, use `update-account`:

- Replace the notification channel(s) with `--set-notifications`. An account must keep at least one channel; it cannot be left without any.
- Rename an organization with `--rename-org` (and `--org-id` when the account has more than one organization).
- Remove a role with `--remove-role buyer|seller`. A role cannot be removed while agents still back it: the seller role is blocked while a Selling Agent exists, and the buyer role is blocked while a Buying Agent exists. Retire those agents first.

## Guided Flow

Start with runtime `status`, then explain that this flow represents the one web/OAuth moment. After it completes, all work returns to the user's favorite agentic application.

Also explain the next milestone clearly: after account setup, the user will create and fill an Autonomous Playbook. For procurement, this becomes a Buying Playbook. For selling, this becomes one Service/Selling Playbook per Service. The playbook is the operating contract that lets Belong agents sell and/or procure autonomously inside Standing Authorization while escalating exceptions to Marketplace Inbox.

As part of this one connection moment, require the human to connect a Calendly account
(and optionally Google Calendar). This is mocked as ready, like payment and legal.
Calendly is how Belong agents expose their human's real-time availability to the other
side and how a booking auto-creates the video join link, so the human does not have to
chase scheduling or paste links by hand. If the human has not connected Calendly, agents
cannot auto-schedule and will escalate to the Marketplace Inbox and this notification
channel before booking any meeting.

Collect:

- Human name
- Human role for this setup: buyer, seller, or both
- Organization Profile name
- Organization kind: company or individual
- Notification channels: email, Slack, WhatsApp, or similar
- Calendly connection (required), plus Google Calendar if used

Then run:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py setup-account --human-name "<name>" --role buyer|seller|both --org-name "<org>" --org-kind company --notifications "email,Slack"
```

## Output

Summarize:

- OAuth status
- Belong Account owner
- Organization Profile
- Notification channels and the "return to your agentic application and open the inbox" pattern
- Payment/legal readiness
- Calendar readiness: Calendly (required) and Google Calendar if connected
- Which training skill comes next: `$belong-train-buying-agent`, `$belong-train-selling-agent`, or both

If the human is a Service Provider, route to `$belong-train-selling-agent`. If the human is a buyer-side human, route to `$belong-train-buying-agent`. If both, tell them to train both agents but keep one Selling Agent per Service.

Use the Marketplace Inbox as the canonical next-work list.

Do not route the human into internal buying, selling, Active Service, or Dispute capabilities from setup. Those are autonomous agent capabilities after training.
