---
name: belong-internal-active-service-actions
description: Internal Buying Agent and Selling Agent capability for mocked Active Service operation after buyer signature. Use when agents autonomously coordinate delivery plans, provider Fulfillment Tasks, messages, Human-to-Human Meetings with prep/follow-up, Deliverable Evidence Packages, Delivery Acceptance, payment authorization/charge/hold/release/refund/collection events, Change Orders, role permissions, and transition to disputes, reputation, audit, or optimization.
---

# Belong Internal Active Service Actions

Use this after buyer signature creates an Active Service. This is an internal agent capability, not the primary human-facing surface. Buying Agents and Selling Agents continue Active Service work autonomously inside their Playbooks and Standing Authorization. Humans check Active Services through `$belong-check-active-services`, check money through `$belong-check-payments`, resolve escalations through `$belong-inbox`, steer temporarily through `$belong-steer-buying-agent` or `$belong-steer-selling-agent`, and retrain durably through the training skills.

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

## Files And Evidence

Files attached to an Active Service can be:

- Deliverables the Selling Agent submits (the output of the Service)
- Information sources the buyer provides (inputs the provider needs to deliver)
- Shared working files exchanged by both sides
- Evidence that something happened (for example a call transcript, recording, photo, or
  report)

The deliverable itself can be sufficient evidence on its own. It is at the Selling
Agent's discretion whether to attach additional evidence, and it is worth considering
when the deliverable is not a file by nature (for example a live training call, where the
agent may add a transcript, recording, or photo mapped to the acceptance criteria).

Whatever files are tied to an Active Service — deliverables, sources, or evidence — are
retained with that service so that, if a dispute opens, the marketplace and the Belong
Judge can access the complete file record for the whole Active Service.

## Escalation

Create or inspect Marketplace Inbox items whenever the agent hits spend, scope, contract, payment, legal, ambiguity, confidence, meeting, dispute, or ordinary service-fulfillment limits.

If either agent is paused, block new autonomous delivery, Change Order, negotiation, optimization, or payment actions by that agent. Continue required notices, deadlines, dispute handling, payment alerts, and human escalations.

## Output

Summarize Active Service status, contract/SOW obligations, Change Order state, open tasks, evidence, acceptance state, cumulative spend/authority result, payment/collections ledger, stale or pending inbox items, reputation impact, audit or Decision Explanation path, and next human-facing skill.
