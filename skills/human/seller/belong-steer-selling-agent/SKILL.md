---
name: belong-steer-selling-agent
description: Seller-specific human-facing temporary steering for a Belong Selling Agent. Use when a Service Provider human wants to influence one Selling Agent inside the current Service Playbook and Standing Authorization without durably retraining it.
---

# Belong Steer Selling Agent

**Communication:** follow the Belong Communication Standard in `voice.md` — apply its voice and use its verbatim scripts (filling the `<slots>`) for every human-facing message.

Use this when a Service Provider human wants a temporary, auditable nudge such as:

- Push harder on Deliverable Evidence Package quality in this Active Service.
- Be more conservative about discounts for this Proposal.
- Prioritize faster seller-led discovery for this Engagement Feed.
- Avoid expanding scope beyond the signed Service Contract/SOW.
- Escalate human workshops sooner for this Service this week.

## Boundaries

Steering is non-durable. It does not change the Service Playbook, Standing Authorization, contract/SOW authority, payment rules, legal terms, pricing, scope limits, collections rules, escalation thresholds, or reputation rules.

Do not use steering to move money, sign contracts, approve Change Orders, bypass Agent Pause, expand authority, or permanently alter a Playbook.

Route instead:

- Operational approval, fulfillment exception, payment exception, or meeting response: `$belong-inbox`
- Durable Service Playbook change: `$belong-train-selling-agent`
- Read/check seller inbound pipeline: `$belong-check-selling-pipeline`
- Read/check Active Service state: `$belong-check-active-services`

## Guided Flow

Run runtime `status`, identify the target Selling Agent, and confirm the intended scope:

- `general`
- `service`
- `engagement_feed`
- `proposal`
- `active_service`

When scope is `general` and no expiration is given, clarify intent before recording: propose a temporary window if the nudge is short-lived, or route to `$belong-train-selling-agent` if the human means a permanent, from-now-on change. An open-ended general steer that never expires should become durable training instead.

Then run `steer-selling-agent` with the instruction, scope, linked object when needed, expiration when provided, and actor.

## Output

Summarize the Steering Instruction, scope, expiration, Service Playbook version it applies under, why it is non-durable, and what would require Inbox approval or Service Playbook retraining instead.
