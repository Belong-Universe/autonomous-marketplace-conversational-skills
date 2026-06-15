---
name: belong-check-reputation
description: Human-facing read/check trust layer for the mocked Belong marketplace. Use for Agent Reputation, buyer ratings, Selling Agent search/trust impact, Reputation Events, complete Audit Log, Decision Explanations, Marketplace Privacy Promise, Marketplace Learning Boundary, network-effect explanations, Provider Optimization and Selling Optimization signals, and Belong seller-side transaction/platform fee visibility.
---

# Belong Check Reputation

Use this when a human asks what happened, why an agent acted, how trust changed, how reputation affects search, or how Belong learns without exposing private data.

This is a read/check skill. If the human wants to act, route to `$belong-inbox` for operational work, `$belong-steer-buying-agent` or `$belong-steer-selling-agent` for temporary guidance, or `$belong-train-buying-agent`/`$belong-train-selling-agent` for durable retraining.

## Reputation

Run `reputation` to inspect Buying Agent and Selling Agent scores. Reputation is agent-level because every marketplace interaction happens through Belong agents.

Use `rate` after delivery, dispute, or cancellation outcomes. Reputation events should reflect outcome and conduct: accepted delivery, missed obligations, payment or collection behavior, disputes, response time, escalation quality, contract compliance, evidence quality, cancellations, and ratings.

## Audit

Run `audit` for a complete log of identities, timestamps, instructions, Playbook versions, authority checks, decisions, messages, proposals, contracts, signatures, payments, evidence, acceptance, escalations, disputes, Judge decisions, and reputation changes.

Run `explain --audit-id ...` for a Decision Explanation. Explain from audit evidence:

- Relevant instruction or event
- Playbook rule and version
- Authority check, including pause state and cumulative spend when relevant
- Contract/SOW version, Change Order, or payment ledger entry when relevant
- Marketplace evidence with object IDs, timestamps, inbox approvals, messages, deliverables, acceptance mapping, disputes, or ratings
- Outcome

Make Decision Explanations evidence-rich enough for a human to approve, override, pause, dispute, steer, or retrain through the correct skill. Do not expose raw model reasoning or private data outside the marketplace action being explained.

## Privacy, Learning, And Monetization

Explain the Marketplace Privacy Promise: private by default; private Playbooks, contracts, messages, evidence, and organization data are shared only through explicit marketplace actions.

Explain the Marketplace Learning Boundary: aggregated/anonymized outcomes, reputation, benchmarks, search/conversion patterns, and dispute statistics can improve ranking and recommendations without exposing private transaction data.

Explain Belong Monetization when payment terms appear: for now, Belong earns a seller-side transaction/platform fee because the marketplace is the Service Provider's automated revenue channel. The Service Provider remains merchant of record. Payment explanations must show ledger event type, gross amount, platform fee, seller net, hold/release/refund/collection state, and linked contract/SOW or Change Order.

## Output

Summarize scores, events, audit evidence, explanation, lifecycle position, authority/payment result, privacy boundary, and next human-facing action: Inbox, temporary steering, durable retraining, payment check, Active Service check, or no action.
