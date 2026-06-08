---
name: belong-check-active-services
description: Human-facing read/check Active Service view for the mocked Belong marketplace. Use for Active Services, obligations, delivery state, Fulfillment Tasks, Human-to-Human Meetings, Deliverable Evidence Packages, Delivery Acceptance, Change Orders, Disputes, risks, payment ledger summaries, and linked Marketplace Inbox items.
---

# Belong Check Active Services

Use this when a Service Provider human or buyer-side human asks what is happening with Active Services.

This is a read/check skill. It must not directly accept delivery, reject delivery, request revisions, open disputes, move money, create Change Orders, sign contracts, submit evidence, or complete Fulfillment Tasks.

## Guided Flow

Run runtime `active-services` with the relevant owner role and status filter.

Show:

- Active Service status
- Service Contract/SOW obligations
- Fulfillment Task state
- Deliverable Evidence Package state
- Delivery Acceptance state
- Human-to-Human Meeting prep and follow-up state
- Change Order state
- Dispute and Belong Judge state
- Payment ledger summary
- Linked Marketplace Inbox items
- Agent Reputation and Audit Log path when relevant

## Route Actions

- Operational escalation or approval: `$belong-inbox`
- Let the relevant Buying Agent or Selling Agent continue autonomously when the next step is inside its Playbook and Standing Authorization.
- Temporary guidance to a Buying Agent or Selling Agent: `$belong-steer-buying-agent` or `$belong-steer-selling-agent`
- Durable Buying Playbook or Service Playbook change: `$belong-train-buying-agent` or `$belong-train-selling-agent`
- Money details: `$belong-check-payments`
- Trust and Decision Explanation details: `$belong-check-reputation`
