---
name: belong-internal-active-service-actions
description: Internal Buying Agent and Selling Agent capability for mocked Active Service operation after buyer signature. Use when agents autonomously coordinate delivery plans, provider Fulfillment Tasks, messages, Human-to-Human Meetings with prep/follow-up, Deliverable Evidence Packages, Delivery Acceptance, payment authorization/charge/hold/release/refund/collection events, Change Orders, role permissions, and transition to disputes, reputation, audit, or optimization.
---

# Belong Internal Active Service Actions

Use this after buyer signature creates an Active Service. This is an internal agent capability, not the primary human-facing surface. Humans ask the Buying Agent or Selling Agent to continue Active Service work through `$belong-run-buying-agent` or `$belong-run-selling-agent`, check Active Services through `$belong-check-active-services`, check money through `$belong-check-payments`, resolve escalations through `$belong-inbox`, steer temporarily through `$belong-steer-buying-agent` or `$belong-steer-selling-agent`, and retrain durably through the training skills.

## Start

Run runtime `status`. Identify the Active Service and role:

- Selling Agent primarily handles delivery plan, provider-side Fulfillment Tasks, deliverable submission, evidence, billing/collections, seller escalations, and seller-side meeting prep.
- Buying Agent primarily handles buyer requirements, buyer-side tasks, payment authorization, evidence review, acceptance/rejection/revision/dispute, buyer escalations, and buyer-side meeting prep.
- Both can message, request information, negotiate Change Orders, schedule meetings, and open/respond to disputes.

Confirm the signed Service Contract/SOW version, open obligations, pending inbox items, pause state for both agents, authority envelope, cumulative spend, and payment ledger before changing delivery or payment state.

## Guided Actions

Use `active-action` for:

- `fulfillment-task`: Service Provider human/team action needed to deliver the Service
- `meeting`: Human-to-Human Meeting with agent prep and follow-up
- `change-order`: signed contract/SOW amendment for changed scope, price, timeline, deliverables, and payment expectations
- `deliver`: Deliverable Evidence Package with files, links, notes, acceptance mapping, timestamp, and submitter
- `accept`, `reject`, `revise`, or `dispute`: Delivery Acceptance decision
- `payment`: Stripe Payment Stack mock for authorizations, charges, holds, releases, refunds, or collections
- `message`: Active Service message

For every Change Order, state the prior contract/SOW version, requested delta, affected obligations, approval/signature state, price change, timeline change, payment ledger impact, and new acceptance evidence. Unsigned Change Orders must remain pending and visible in the Marketplace Inbox.

For every payment event, keep a ledger summary: prior payment state, new event, gross amount, seller-side platform fee, seller net, hold/release/refund/collection status, merchant-of-record distinction, and audit ID. Do not authorize, charge, release, refund, or collect when cumulative spend or payment rules exceed Standing Authorization without human approval.

## Escalation

Create or inspect Marketplace Inbox items whenever the agent hits spend, discount, scope, contract, payment, legal, ambiguity, confidence, meeting, dispute, or ordinary service-fulfillment limits.

If either agent is paused, block new autonomous delivery, Change Order, negotiation, optimization, or payment actions by that agent. Continue required notices, deadlines, dispute handling, payment alerts, and human escalations.

## Output

Summarize Active Service status, contract/SOW obligations, Change Order state, open tasks, evidence, acceptance state, cumulative spend/authority result, payment/collections ledger, stale or pending inbox items, reputation impact, audit or Decision Explanation path, and next human-facing skill.
