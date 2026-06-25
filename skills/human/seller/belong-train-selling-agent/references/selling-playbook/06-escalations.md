# Escalations

[Back to index](index.md) | Previous: [Human-To-Human Meetings](05-human-to-human-meetings.md) | Next: [Disputes And Reputation Rules](07-disputes-and-reputation.md)

This section defines what the Selling Agent must bring to the Service Provider human/team instead of handling autonomously.

## Source Signals

Look for escalation policies, support queues, fulfillment ownership charts, approval matrices, incident notes, Slack/email routing, account ownership, and payment exception history.

## Required Fields

- Escalation categories
- Trigger thresholds
- Required approver or owner for each category
- Notification channels
- Response time expectations
- Information the agent must include in the escalation
- Agent pause and resume rules
- Human override process
- Stale, duplicate, and superseded inbox cleanup rules
- Escalation closure criteria

## Human-Performed Actions (standing manual control)

Beyond "agent executes" and "agent escalates for approval", the Selling Playbook can mark specific high-criticality action types as **always performed by the human** (Scenario B): a third authority outcome. When the agent reaches one, it does not execute and does not ask for approval — it hands the action to the Service Provider human, who performs it directly with `$belong-operate-selling-flow`.

Only this fixed set of seller action types is eligible: `sign` (seller-signed proposal), `deliver`, `accept-change-order`, `payment` (collection), `dispute`. Operational actions (discovery, meeting, message, fulfillment-task) are not eligible and stay with the agent; the human can still take any single flow over ad-hoc with `$belong-operate-selling-flow`.

This is a standing rule per action type, not per flow, and never arbitrary sub-flow slicing. Treat it as authority-critical and confirm it live before activation. Map the confirmed set to `--human-controlled-actions` (comma-separated).

## Quality Bar

The section is `Done` when the Selling Agent can identify exceptions early, route them to the right human, include enough context for action, and avoid continuing autonomous work past its authority.

## Guardrails

- Do not bury exceptions in ordinary status updates.
- Do not continue delivery, Change Orders, or payment movement when a required approval is pending.
- Do not let stale inbox items remain unresolved when newer decisions supersede them.

