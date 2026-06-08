---
name: belong-check-buying-requests
description: Buyer-specific human-facing read/check view for pre-contract Buying Requests. Use for Buying Requests, semantic search results, Engagement Feeds, seller-led Discovery Questionnaires, seller-signed Service Contract/SOW proposals, negotiation state, authority checks, linked Marketplace Inbox items, and buyer pipeline visibility before Active Service.
---

# Belong Check Buying Requests

Use this when a buyer-side human asks what is happening before a contract is signed: open needs, search results, RFPs, competitive feeds, discovery, proposals, negotiation, or pending buyer approvals.

This is a read/check skill. It must not create a new request, answer discovery, negotiate, sign, move money, approve exceptions, or change the Buying Playbook.

## Guided Flow

Run runtime `buying-requests` with the relevant Buying Agent and status filter.

Show:

- Buying Request status and need
- Semantic Service Search Results and tags
- Direct or competitive Engagement Feed state
- Seller-led Discovery Questionnaire state
- Seller-signed Service Contract/SOW proposals
- Proposal comparison and negotiation state when present
- Authority, budget, cumulative spend, and payment readiness signals when present
- Linked Marketplace Inbox items
- Audit Log or Decision Explanation path when relevant

## Route Actions

- New buyer intent: `$belong-start-buying-request`
- Let the Buying Agent continue autonomously when the next step is inside the Buying Playbook and Standing Authorization.
- Operational escalation or approval: `$belong-inbox`
- Temporary Buying Agent guidance: `$belong-steer-buying-agent`
- Durable Buying Playbook change: `$belong-train-buying-agent`
- Signed/active delivery state: `$belong-check-active-services`
- Trust and Decision Explanation details: `$belong-check-reputation`
