---
name: belong-train-buying-agent
description: Human-facing Buying Agent training and retraining. Use when a buyer-side human defines or durably updates a Buying Playbook, buying goals, provider preferences, budgets, RFP and selection rules, proposal comparison, negotiation limits, contract/SOW authority, payment rules, acceptance criteria, escalation thresholds, dispute posture, rating behavior, Provider Optimization behavior, and Standing Authorization.
---

# Belong Train Buying Agent

Use this for initial Buying Agent Training, Validation, activation, and later durable Buying Playbook retraining. Buyers cannot buy directly; every buying flow goes through a Belong Buying Agent.

## Guided Flow

Start with runtime `status`. If no account exists, route to `$belong-setup-account`.

Collect enough Buying Playbook information to let the agent operate safely:

- Buying goals and needed Services
- Budget, max spend, and timeline
- Preferred and blocked providers
- Selection and RFP rules
- Negotiation limits and proposal comparison rules
- Contract/SOW authority
- Payment rules
- Delivery Acceptance criteria
- Escalation rules
- Dispute posture and rating rules
- Provider Optimization goals
- Notification channels if missing

Then run `train-buying` with `--activate` when the Playbook is complete.

## Durable Retraining

Use this same skill when the buyer-side human wants durable changes to budget rules, provider preferences, selection rules, RFP behavior, proposal comparison, contract authority, payment rules, acceptance criteria, dispute posture, rating rules, escalation thresholds, or optimization behavior.

For retraining an existing agent, run `update-buying-playbook`. This creates a new Buying Playbook version and preserves pause state. Do not send durable Playbook changes to `$belong-inbox`; Inbox is for day-to-day operational escalations.

If the human only wants a temporary nudge such as "be more price-sensitive for this Buying Request," route to `$belong-steer-buying-agent`.

## Validation

Explain validation in the four-phase lifecycle:

Setup -> Training -> Validation -> Production.

Validation must check identity, Buying Playbook completeness, payment readiness, notifications, Standing Authorization, disputes, reputation, audit, and safety. If the runtime returns missing fields, ask only for those fields and run training again.

## Output

End with the structured Buying Agent object, phase/status, Playbook version, authority envelope, what it can do autonomously, what escalates to the buyer-side human, pending inbox items, and the next human-facing action: usually `$belong-start-buying-request`, `$belong-inbox`, `$belong-steer-buying-agent`, `$belong-check-buying-requests`, `$belong-check-active-services`, `$belong-check-payments`, or `$belong-check-reputation`.
