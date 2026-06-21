---
name: belong-check-active-services
description: Human-facing read/check Active Service view for the mocked Belong marketplace. Use for Active Services, obligations, delivery state, Fulfillment Tasks, Human-to-Human Meetings, Deliverable Evidence Packages, Delivery Acceptance, Change Orders, Disputes, risks, payment ledger summaries, and linked Marketplace Inbox items.
---

# Belong Check Active Services

**Communication:** follow the Belong Communication Standard in `voice.md` — apply its voice and use its verbatim scripts (filling the `<slots>`) for every human-facing message.

Use this when a Service Provider human or buyer-side human asks what is happening with Active Services.

This is a read/check skill. It must not directly accept delivery, reject delivery, request revisions, open disputes, move money, create Change Orders, sign contracts, submit evidence, or complete Fulfillment Tasks.

## Guided Flow

Run runtime `active-services` with the relevant owner role and status filter.

Show:

- Active Service status and `control_state` (agent_controlled, human_controlled, or paused)
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

- Operational escalation or approval, or to take/release/pause/resume control of a flow: `$belong-inbox`
- Let the relevant Buying Agent or Selling Agent continue autonomously when the next step is inside its Playbook and Standing Authorization.
- Take manual control of an Active Service, or operate one already `human_controlled`: `$belong-operate-buying-flow` (buyer side) or `$belong-operate-selling-flow` (seller side)
- Temporary guidance to a Buying Agent or Selling Agent: `$belong-steer-buying-agent` or `$belong-steer-selling-agent`
- Durable Buying Playbook or Service Playbook change: `$belong-train-buying-agent` or `$belong-train-selling-agent`
- Money details: `$belong-check-payments`
- Trust and Decision Explanation details: `$belong-check-reputation`

## Output

This is a read-only view, so nothing changes. Summarize:

- Which Active Service(s) the human is looking at, by owner role and status
- Current lifecycle phase: delivery, evidence, acceptance, payment, Change Order, meeting, or dispute
- The most relevant state: what is done, what is in progress, and what is blocked or waiting
- Any linked Marketplace Inbox items that need the human, and the Audit Log path for detail
- Anything notable the structured view does not capture: risks, anomalies, or approaching deadlines
- Recommended next skill or action, without taking it here

Always remind the human that this skill only reads state. To act, route to `$belong-inbox` for approvals, the training or steering skills for behavior, or `$belong-check-payments` and `$belong-check-reputation` for deeper detail.
