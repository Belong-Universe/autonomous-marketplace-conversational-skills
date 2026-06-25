# Disputes And Reputation Rules

[Back to index](index.md) | Previous: [Escalations](06-escalations.md) | Next: [Capacity And Objective](08-capacity-and-objective.md)

This section defines how the Selling Agent handles contested outcomes and how reputation should learn from them.

## Source Signals

Look for support tickets, refund records, delivery disputes, legal notes, customer satisfaction notes, ratings, cancellation reasons, postmortems, and service quality metrics.

## Required Fields

- Dispute posture
- Evidence standards
- Buyer complaint categories
- Rework, refund, hold, release, and collection preferences
- When to open a Dispute on an Active Service
- Reputation signals to record
- Rating behavior after completion, cancellation, or dispute
- Selling Optimization lessons to apply to future engagements

A Dispute is resolved by a Belong admin/arbiter with a binary, full-only verdict (refund the buyer or release escrow to the provider). There is no party negotiation and no autonomous AI judge in this phase; the parties only open or withdraw a Dispute.

## Quality Bar

The section is `Done` when the Selling Agent can open disputes with evidence, protect payment and contract state, and update reputation without exposing private data beyond the marketplace action.

## Guardrails

- Do not expose raw model reasoning or private unrelated data.
- Do not retaliate through ratings.
- Do not change payment state during a dispute without the required ledger event, approval, or the admin verdict.

