---
name: belong-setup-account
description: Guide a Service Provider human or buyer-side human through mocked Belong account onboarding. Use for OAuth-style login, Belong Account creation, Organization Profile setup, account ownership, role context, notification preferences such as email/Slack/WhatsApp, mocked payment readiness, mocked legal/signing readiness, and routing into Buying Agent or Selling Agent training.
---

# Belong Setup Account

Use this for the Setup phase before any Buying Agent or Selling Agent training, and to manage an existing Belong Account.

## Returning Human

If an account already exists for this human, do not treat setup as new. Re-running setup is additive: it adds a role (for example, a buyer who now also sells), adds an organization, and unions notification channels onto the existing account. Confirm whether the human is adding a role, organization, or channel rather than starting over.

To change rather than add, use `update-account`:

- Replace the notification channel(s) with `--set-notifications`. An account must keep at least one channel; it cannot be left without any.
- Rename an organization with `--rename-org` (and `--org-id` when the account has more than one organization).
- Remove a role with `--remove-role buyer|seller`. A role cannot be removed while agents still back it: the seller role is blocked while a Selling Agent exists, and the buyer role is blocked while a Buying Agent exists. Retire those agents first.

## Guided Flow

Start with runtime `status`, then explain that this mocked flow represents the one web/OAuth moment. After it completes, all work returns to the user's favorite agentic application.

Collect:

- Human name
- Human role for this setup: buyer, seller, or both
- Organization Profile name
- Organization kind: company or individual
- Notification channels: email, Slack, WhatsApp, or similar

Then run:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py setup-account --human-name "<name>" --role buyer|seller|both --org-name "<org>" --org-kind company --notifications "email,Slack"
```

## Output

Summarize:

- Mock OAuth status
- Belong Account owner
- Organization Profile
- Notification channels and the "return to your agentic application and open the inbox" pattern
- Mocked payment/legal readiness
- Which training skill comes next: `$belong-train-buying-agent`, `$belong-train-selling-agent`, or both

If the human is a Service Provider, route to `$belong-train-selling-agent`. If the human is a buyer-side human, route to `$belong-train-buying-agent`. If both, tell them to train both agents but keep one Selling Agent per Service.

Use the Marketplace Inbox as the canonical next-work list.

Do not route the human into internal buying, selling, Active Service, or Dispute capabilities from setup. Those are autonomous agent capabilities after training.
