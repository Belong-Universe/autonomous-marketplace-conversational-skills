---
name: belong-internal-disputes
description: Internal agent and Belong Judge capability for mocked Belong marketplace disputes. Use when Buying Agents, Selling Agents, the autonomous Belong Judge, or a Belong human judge escalation handles contested delivery, payment, contract/SOW compliance, acceptance, evidence, conduct issues, payment/reputation impact, and dispute outcomes.
---

# Belong Internal Disputes

Use this when delivery, payment, contract/SOW compliance, acceptance, evidence, or conduct is contested. This is an internal agent/Judge capability. Humans participate in a Dispute through `$belong-manage-dispute` (open, respond, ask the Belong Judge, escalate to a Belong human judge) and see dispute work through `$belong-inbox`, `$belong-check-active-services`, and `$belong-check-reputation`.

## Start

Run runtime `status` and inspect pending dispute inbox items. Identify:

- Active Service
- Contract/SOW obligation at issue
- Evidence package
- Buyer-side and seller-side positions
- Whether agents can handle it inside their Playbooks or must escalate

## Guided Actions

Use:

- `dispute-open` to open a structured Dispute
- `dispute-respond` for buyer or seller responses
- `judge` for the autonomous Belong Judge decision
- `judge --escalate-human` when a human wants Belong human judge review

The Belong Judge is first-layer autonomous adjudication. It reviews mocked evidence, contract/SOW terms, messages, acceptance criteria, payment state, and reputation history. Humans may escalate further to a Belong human judge.

## Output

Summarize Dispute status, evidence considered, payment hold/release/refund implications when present, reputation impact, pending inbox items, whether the decision came from agents, Belong Judge, or a Belong human judge escalation, and the audit path.
