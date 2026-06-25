---
name: belong-setup-account
description: Guide a Service Provider human or buyer-side human through Belong account onboarding. Use for OAuth-style login, Belong Account creation, Organization Profile setup, account ownership, role context, notification preferences such as email/Slack/WhatsApp, required Stripe connection for payment readiness, legal/signing readiness, and required Calendly connection (plus optional Google Calendar) for scheduling Human-to-Human Meetings. The account belongs to an Organization; any Buying or Selling Agent also belongs to the Organization and is created later in training, not in setup.
---

# Belong Setup Account

**Communication:** follow the Belong Communication Standard in `voice.md` — apply its voice and use its verbatim scripts (filling the `<slots>`) for every human-facing message.

Use this for the Setup phase before any Buying Agent or Selling Agent training, and to manage an existing Belong Account.

## Prerequisites

Before setup, the human needs two external accounts ready, since both are connected
during onboarding:

- Stripe — for payment readiness (charges, holds, releases, payouts) and KYC:
  connecting Stripe verifies the organization's legal identity and runs sanctions/AML
  and baseline financial screening, so provider verification (KYC) happens here. Sign up
  at https://dashboard.stripe.com/register
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

Also explain the next milestone clearly: after account setup, the user will create and fill an Autonomous Playbook. For procurement, this becomes a Buying Playbook. For selling, this becomes one Service/Selling Playbook per Service. The playbook is the operating contract that lets Belong agents sell and/or procure autonomously inside Standing Authorization while escalating exceptions to Marketplace Inbox. This is a separate step: setup creates the account and its Organization, and any Buying or Selling Agent belongs to the Organization and is created later in training, not here.

As part of this one connection moment, require the human to connect a Calendly account
(and optionally Google Calendar). Calendly is connected here alongside payment and legal
readiness. Calendly is how Belong agents expose their human's real-time availability to the other
side and how a booking auto-creates the video join link, so the human does not have to
chase scheduling or paste links by hand. If the human has not connected Calendly, agents
cannot auto-schedule and will escalate to the Marketplace Inbox and this notification
channel before booking any meeting.

A company account can have more than one human user. Then ask whether the human wants to
add teammates to this company account: "Would you like to add more users to engage with
the agents from this account?" If yes, collect for each person their name, email, and one
role from: owner, admin, developer, finance, support, buyer, or approver. Each invited
person gets an invitation email to join the company's Belong account and help manage its
agents' playbooks.

Collect:

- Human name
- Human role for this setup: buyer, seller, or both
- Organization Profile name
- Organization kind: company or individual
- Notification channels: email, Slack, WhatsApp, or similar
- Calendly connection (required), plus Google Calendar if used
- Optional teammates to invite: name, email, and role (owner, admin, developer, finance, support, buyer, approver)

Then run:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py setup-account --human-name "<name>" --role buyer|seller|both --org-name "<org>" --org-kind company --notifications "email,Slack" --invite "Ana Gomez|ana@acme.com|admin" --invite "Luis Paz|luis@acme.com|finance"
```

## Output

Summarize:

- OAuth status
- Belong Account owner
- Organization Profile
- Notification channels and the "return to your agentic application and open the inbox" pattern
- Payment/legal readiness
- Calendar readiness: Calendly (required) and Google Calendar if connected
- Invited teammates and that invitation emails were sent
- Which training skill comes next: `$belong-train-buying-agent`, `$belong-train-selling-agent`, or both

Once the account and its Organization exist, the separate next step is to create an agent in training: route a Service Provider to `$belong-train-selling-agent`, a buyer-side human to `$belong-train-buying-agent`. If both, tell them to train both agents but keep one Selling Agent per Service. The agent is created in training, not in setup.

Use the Marketplace Inbox as the canonical next-work list.

Do not route the human into internal buying, selling, Active Service, or Dispute capabilities from setup. Those are autonomous agent capabilities after training.
