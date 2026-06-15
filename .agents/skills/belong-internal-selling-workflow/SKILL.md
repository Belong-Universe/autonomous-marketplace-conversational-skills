---
name: belong-internal-selling-workflow
description: Internal Selling Agent capability for Production selling workflows in the mocked Belong marketplace. Use when the Belong Selling Agent autonomously handles Service readiness, buyer engagement, seller-led discovery, seller-signed Service Contract/SOW proposals, negotiation limits, billing and collections, platform fees, delivery handoff, fulfillment escalations, Human-to-Human Meeting preparation, and Selling Optimization.
---

# Belong Internal Selling Workflow

Use this once a Selling Agent is in Production for one Service. This is an internal agent capability, not the primary human-facing surface. The Selling Agent continues autonomously inside the Service Playbook and Standing Authorization after inbound engagement arrives. Humans check inbound seller work through `$belong-check-selling-pipeline`, supervise escalations through `$belong-inbox`, give temporary guidance through `$belong-steer-selling-agent`, and make durable Service Playbook changes through `$belong-train-selling-agent`.

## Start

Run runtime `status`. If no Selling Agent is in Production, route the human to `$belong-train-selling-agent`.

Identify the Service Provider human, Selling Agent, Service, buyer-side object, seller inbox state, billing/collections state, and whether the Selling Agent is paused before guiding seller work.

## Production Responsibilities

Keep the Service Provider human oriented around what the Selling Agent does:

- Represents one Service 24/7
- Answers buyer questions through Engagement Feeds
- Leads discovery with questionnaires
- Sends the seller-signed Service Contract/SOW as the Proposal
- Negotiates inside discount, scope, and contract limits
- Escalates exceptions and ordinary fulfillment needs to the Service Provider human/team
- Coordinates billing, collections, delivery, evidence, meetings, disputes, and reputation
- Keeps the Service Provider visible as merchant of record while Belong facilitates workflow, legal, payment orchestration, inbox, reputation, audit, and disputes

## Guided Actions

Use the runtime through buyer-created feeds when available:

- Inspect and clean seller inbox items that are stale, duplicate, superseded, or linked to completed fulfillment before starting new seller actions
- Inspect Engagement Feeds and pending discovery
- Create seller-signed Service Contract/SOW proposals after discovery
- Negotiate terms only after checking Standing Authorization, pause state, discount limit, scope limit, contract authority, cumulative buyer spend signal, and payment rules
- Explain seller-side platform fee and merchant-of-record distinction
- Move executed deals to internal Active Service actions and human read/check views
- Create Selling Optimization recommendations with `optimization`

If a buyer needs a human workshop, service-specific human action, unusual scope, legal term, payment exception, collections exception, or sensitive dispute, create or resolve Marketplace Inbox items through `$belong-inbox`.

Do not let a paused Selling Agent create new proposals, negotiate, initiate Change Orders, optimize, or trigger new payment activity. It may still preserve active obligations, required notices, disputes, payment alerts, deadlines, and human escalations.

For post-signature changes, use internal Active Service actions. Change Orders must amend the signed contract/SOW and state scope, price, timeline, deliverable, approval, and payment ledger impact. Human review happens through `$belong-inbox`.

## Output

End with Service status, Selling Agent reputation, proposal/contract status, authority/pause result, billing/collections and payment ledger summary, platform-fee visibility, stale or pending provider tasks/escalations, and next action.
