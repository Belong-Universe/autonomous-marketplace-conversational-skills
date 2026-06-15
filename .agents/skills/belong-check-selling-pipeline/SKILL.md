---
name: belong-check-selling-pipeline
description: Seller-specific human-facing read/check view for inbound Selling Agent pipeline before Active Service. Use for Services, buyer engagements, seller-led Discovery Questionnaires, seller-signed Service Contract/SOW proposals, negotiations, billing readiness, linked Marketplace Inbox items, and seller pipeline visibility.
---

# Belong Check Selling Pipeline

Use this when a Service Provider human asks what is happening before a buyer signs: Service listing state, inbound buyer engagements, discovery, proposals, negotiation, billing readiness, or seller approvals.

This is a read/check skill. It must not create proposals, negotiate, approve discounts, sign Change Orders, submit evidence, move money, or change the Service Playbook.

## Guided Flow

Run runtime `selling-pipeline` with the relevant Selling Agent, optional Service ID, and status filter.

Show:

- Service status and Service Playbook version
- Buyer Engagement Feed state
- Seller-led Discovery Questionnaire state
- Seller-signed Service Contract/SOW proposals
- Negotiation and discount-authority signals when present
- Billing, collections, platform fee, seller net, and merchant-of-record readiness
- Linked Marketplace Inbox items
- Audit Log or Decision Explanation path when relevant

## Route Actions

- Operational escalation, approval, fulfillment, meeting, payment, or discount exception: `$belong-inbox`
- Let the Selling Agent continue autonomously when the next step is inside the Service Playbook and Standing Authorization.
- Temporary Selling Agent guidance: `$belong-steer-selling-agent`
- Durable Service Playbook or Service positioning change: `$belong-train-selling-agent`
- Signed/active delivery state: `$belong-check-active-services`
- Payment ledger details: `$belong-check-payments`
- Trust and Decision Explanation details: `$belong-check-reputation`
