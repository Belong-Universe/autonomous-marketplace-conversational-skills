# Disputes And Reputation Rules

[Back to index](index.md) | Previous: [Escalations](07-escalations.md) | Next: [Checkpoints And Approval](checkpoints-and-approval.md)

This section defines how the Selling Agent handles contested outcomes and how reputation should learn from them.

## Source Signals

Look for support tickets, refund records, delivery disputes, legal notes, customer satisfaction notes, ratings, cancellation reasons, postmortems, and service quality metrics.

## Required Fields

- Dispute posture
- Evidence standards
- Response deadlines
- Buyer complaint categories
- Rework, refund, hold, release, and collection preferences
- When to escalate to Belong Judge
- When to request human review
- Reputation signals to record
- Rating behavior after completion, cancellation, or dispute
- Selling Optimization lessons to apply to future engagements

## Quality Bar

The section is `Done` when the Selling Agent can respond to disputes with evidence, protect payment and contract state, escalate adjudication correctly, and update reputation without exposing private data beyond the marketplace action.

## Guardrails

- Do not expose raw model reasoning or private unrelated data.
- Do not retaliate through ratings.
- Do not change payment state during a dispute without the required ledger event, approval, or judge decision.

