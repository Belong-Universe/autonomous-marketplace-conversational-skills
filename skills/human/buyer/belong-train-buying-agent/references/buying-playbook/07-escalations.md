# Escalations

[Back to index](index.md) | Previous: [Legal And Contracts](06-legal-and-contracts.md) | Next: [Disputes And Reputation](08-disputes-and-reputation.md)

This section defines what the Buying Agent must route to the buyer-side human through the Marketplace Inbox instead of handling autonomously.

## Source Signals

Look for approval matrices, delegation-of-authority documents, procurement policy, notification preferences, and escalation/ownership charts.

## Required Fields

- Escalation thresholds (spend, contract value, term risk, no-ZOPA)
- Information requests and authorization requests the agent should raise
- Payment exceptions that require a human
- Change Order approvals
- Agent pause/resume rules
- Notification channels (email, Slack, WhatsApp) and timing
- Who on the buyer side owns each escalation path

## Quality Bar

The section is `Done` when the Buying Agent knows exactly which decisions stop for a human, where they go, and who owns them.

## Guardrails

- Do not act autonomously above any escalation threshold; route to the Inbox.
- Do not use steering or training to bypass an escalation; those change behavior, not authority.
- Every escalation must carry a Decision Explanation, not raw model reasoning.
