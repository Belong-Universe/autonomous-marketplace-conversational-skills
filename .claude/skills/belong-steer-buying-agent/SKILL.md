---
name: belong-steer-buying-agent
description: Buyer-specific human-facing temporary steering for a Belong Buying Agent. Use when a buyer-side human wants to influence the Buying Agent inside the current Buying Playbook and Standing Authorization without durably retraining it.
---

# Belong Steer Buying Agent

Use this when a buyer-side human wants a temporary, auditable nudge such as:

- Be more price-sensitive for this Buying Request.
- Prefer faster providers this week.
- Avoid a specific Service for this search.
- Be more conservative about opening a Dispute.
- Push harder on Deliverable Evidence Package quality in this Active Service.

Do not use this to say "I need a provider for X." That belongs to `$belong-start-buying-request`, which creates a Buying Request and starts semantic search.

## Boundaries

Steering is non-durable. It does not change the Buying Playbook, Service Playbook, Standing Authorization, contract/SOW authority, payment rules, legal terms, budget, pricing, scope limits, escalation thresholds, or reputation rules.

Do not use steering to move money, sign contracts, approve Change Orders, bypass Agent Pause, expand authority, or permanently alter a Playbook.

Route instead:

- Operational approval or exception: `$belong-inbox`
- Durable Buying Playbook change: `$belong-train-buying-agent`
- New buyer intent or demand: `$belong-start-buying-request`
- Read/check state: `$belong-check-active-services`, `$belong-check-payments`, or `$belong-check-reputation`

## Guided Flow

Run runtime `status`, identify the target Buying Agent, and confirm the intended scope:

- `general`
- `buying_request`
- `active_service`

Then run `steer-buying-agent` with the instruction, scope, linked object when needed, expiration when provided, and actor.

## Output

Summarize the Steering Instruction, scope, expiration, Playbook version it applies under, why it is non-durable, and what would require Inbox approval or training/retraining instead.
