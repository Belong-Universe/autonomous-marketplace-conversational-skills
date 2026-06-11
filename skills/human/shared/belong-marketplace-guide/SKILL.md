---
name: belong-marketplace-guide
description: Human-facing front door for the Belong Agent-to-Agent Marketplace Skill Pack. Use when a Service Provider human or buyer-side human asks where to start, what to do next, which skills are shared, buyer-specific, seller-specific, or internal, what their agents can do autonomously, what requires Inbox supervision, or how to check marketplace state.
---

# Belong Marketplace Guide

Use this as the human-facing front door and orientation layer for the Belong Skill Pack. The user should never feel lost, and should always understand which actions belong to humans versus autonomous Belong agents.

## First Move

Run the runtime status:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py status
```

If the runtime path is not present, locate sibling skill `belong-marketplace-runtime` or search for `belong_mock.py`. If state is empty, offer the best next path:

- New Service Provider human: use `$belong-setup-account`, then `$belong-train-selling-agent`.
- New buyer-side human: use `$belong-setup-account`, then `$belong-train-buying-agent`, then `$belong-start-buying-request`.
- New human who both buys and sells: use `$belong-setup-account` with role `both`, then train each side independently: `$belong-train-buying-agent` for buying, and `$belong-train-selling-agent` for each Service. One account holds one Buying Agent and one Selling Agent per Service, each with its own Playbook.
- Wants the complete mocked experience fast: run `scenario full-lifecycle --reset`, then summarize the generated state and next inbox items.
- Already in Production: route by role and intent to the shared, buyer-specific, or seller-specific skills below.

Always orient the human by role. Seller-side humans should hear which Service, Selling Agent, buyer feed, contract, billing state, fulfillment task, and seller inbox item they are acting on.

Whenever a Belong agent needs the human, it adds an item to the Marketplace Inbox and sends a notification on the human's preferred channel. The human returns to their agentic application and opens `$belong-inbox`. The notification is mocked; the Inbox is the canonical work list.

## Find Your Next Step By Intent

Map what the human wants to the right skill. Route by intent first, then confirm role.

| The human wants to... | Use |
| --- | --- |
| Get started or is unsure where to begin | `$belong-setup-account` |
| Buy something ("I need X") | `$belong-start-buying-request` |
| See what needs their approval or input | `$belong-inbox` |
| Check how a purchase is progressing (pre-contract) | `$belong-check-buying-requests` |
| Check inbound buyer pipeline (seller side) | `$belong-check-selling-pipeline` |
| See delivery and active work after signature | `$belong-check-active-services` |
| See money, charges, holds, refunds, or payouts | `$belong-check-payments` |
| Understand why an agent acted, or review audit/reputation | `$belong-check-reputation` |
| Handle a contested delivery or dispute | `$belong-inbox` to respond; `$belong-check-active-services` and `$belong-check-reputation` for detail |
| Temporarily nudge an agent | `$belong-steer-buying-agent` or `$belong-steer-selling-agent` |
| Permanently change how an agent behaves | `$belong-train-buying-agent` or `$belong-train-selling-agent` |

## Shared Human Skills

- `$belong-setup-account`: OAuth-style mocked login, Belong Account, Organization Profile, notifications, mocked legal/payment readiness.
- `$belong-inbox`: day-to-day Marketplace Inbox work: information, authorization, instruction/execution, fulfillment, meeting, dispute, payment exception, Change Order approval, pause/resume, and operational intervention.
- `$belong-check-active-services`: read/check Active Services, obligations, delivery, Deliverable Evidence Packages, Delivery Acceptance, Change Orders, Human-to-Human Meetings, Disputes, and linked Inbox items.
- `$belong-check-payments`: read/check bank readiness, transactions, payment ledger, charges, holds, releases, refunds, collections, platform fees, seller net, and merchant-of-record context.
- `$belong-check-reputation`: read/check Agent Reputation, ratings, Audit Log, Decision Explanations, Marketplace Privacy Promise, Marketplace Learning Boundary, Belong monetization, Provider Optimization, and Selling Optimization signals.

## Buyer-Specific Human Skills

- `$belong-train-buying-agent`: buyer-side setup, training, validation, activation, and later durable Buying Playbook retraining.
- `$belong-start-buying-request`: buyer intent surface for "I need X"; creates a Buying Request, launches semantic Service search, and optionally opens an Engagement Feed.
- `$belong-check-buying-requests`: read/check pre-contract buyer pipeline: Buying Requests, Service Search Results, Engagement Feeds, Discovery Questionnaires, seller-signed Service Contract/SOW proposals, negotiations, authority checks, and linked Inbox items.
- `$belong-steer-buying-agent`: temporary non-durable guidance for a Buying Agent inside the current Buying Playbook and Standing Authorization.

## Seller-Specific Human Skills

- `$belong-train-selling-agent`: Service Provider setup, training, validation, activation, and later durable Service Playbook retraining for one Selling Agent per Service.
- `$belong-check-selling-pipeline`: read/check seller inbound pipeline: Services, buyer engagements, Discovery Questionnaires, seller-signed Service Contract/SOW proposals, negotiation, billing readiness, and linked Inbox items.
- `$belong-steer-selling-agent`: temporary non-durable guidance for a Selling Agent inside the current Service Playbook and Standing Authorization.

## Internal Agent Skills

These run automatically as part of the Belong agents' autonomous work. The human does not invoke them directly; agents execute them inside their Playbooks and Standing Authorization, then escalate to the human through `$belong-inbox` when input is needed.

- `$belong-internal-buying-workflow`: internal Buying Agent capability for Buying Request, semantic search, Engagement Feed, Discovery Questionnaire answers, seller-signed Service Contract/SOW comparison, negotiation, buyer signature, Composite Buying Request, and Provider Optimization.
- `$belong-internal-selling-workflow`: internal Selling Agent capability for seller-led discovery, seller-signed Service Contract/SOW proposals, negotiation, billing/collections, Service readiness, and Selling Optimization.
- `$belong-internal-active-service-actions`: internal agent capability for Fulfillment Task, Deliverable Evidence Package, Delivery Acceptance, payment movement, Change Order, meeting, and messages.
- `$belong-internal-disputes`: internal agent and Belong Judge capability for Dispute handling, evidence review, autonomous decisions, and Belong human judge escalation.
- `$belong-marketplace-runtime`: shared mock backend and command reference.

## Guided Navigation

After every state change, say:

1. Current phase
2. Current object
3. What changed
4. What is pending in the Marketplace Inbox
5. Recommended next skill/action

## Lifecycle Invariants

Enforce these across every skill:

- Do not skip lifecycle order: setup, training, validation, Production, buying/search/engagement, discovery, seller-signed Service Contract/SOW Proposal, negotiation, buyer signature, Active Service, delivery/evidence, acceptance/payment, reputation/optimization.
- Treat pending Marketplace Inbox as the canonical work list. Resolve stale, duplicate, or superseded inbox items after each state change before saying the path is clean.
- Check agent status, pause state, Standing Authorization, payment rules, contract authority, and cumulative spend before signing, negotiating, changing scope, or moving money.
- Enforce pause: a paused agent does not start new autonomous work. It may still preserve obligations, notices, deadlines, payment alerts, dispute responses, and required escalations.
- Let Belong agents continue autonomously inside their Playbooks and Standing Authorization. Humans do not run agent workflows manually; they check state, respond through Inbox, steer temporarily, or retrain durably.
- Keep payments ledgered: authorization, charge, hold, release, refund, collection, seller-side platform fee, seller net, and merchant-of-record context must be visible when payment state changes.
- Treat Change Orders as signed contract/SOW amendments. Scope, price, timeline, deliverables, and payment changes must update the contract trail and payment expectations.
- Route durable Playbook changes through `$belong-train-buying-agent` or `$belong-train-selling-agent`. Inbox is for day-to-day operations, not durable training.
- Start new buyer demand through `$belong-start-buying-request`; do not treat "I need X" as steering.
- Keep steering temporary. `$belong-steer-buying-agent` and `$belong-steer-selling-agent` cannot expand authority, change legal/payment limits, move money, sign contracts, bypass pause, or permanently alter a Playbook.
- Provide evidence-rich Decision Explanations from audit evidence, not raw model reasoning.

Never introduce direct buyer mode, bring-your-own-agent, a primary Belong web workspace, or external agent-to-marketplace MCP setup. Humans interact through their favorite agentic application; Belong agents are natively integrated with the mocked backend.

Read the `belong-marketplace-runtime` reference files before declaring the pack complete. In this repo they live under `skills/marketplace/belong-marketplace-runtime/references/`; after installation they may be available as a sibling skill folder.
