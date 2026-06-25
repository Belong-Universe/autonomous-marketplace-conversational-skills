---
name: belong-check-buying-requests
description: Buyer-specific human-facing read/check view for pre-contract Buying Requests. Use for Buying Requests, semantic search results, Engagement Feeds, seller-led Discovery Questionnaires, seller-signed Service Contract/SOW proposals, negotiation state, authority checks, linked Marketplace Inbox items, and buyer pipeline visibility before Active Service.
---

# Belong Check Buying Requests

**Communication:** follow the Belong Communication Standard in `voice.md` — apply its voice and use its verbatim scripts (filling the `<slots>`) for every human-facing message.

Use this when a buyer-side human asks what is happening before a contract is signed: open needs, search results, RFPs, competitive feeds, discovery, proposals, negotiation, or pending buyer approvals.

This is a read/check skill. It must not create a new request, answer discovery, negotiate, sign, move money, approve exceptions, or change the Buying Playbook.

## Guided Flow

Run runtime `buying-requests` with the relevant Buying Agent and status filter.

Show:

- Buying Request status, need, and `control_state` (agent_controlled, human_controlled, or paused)
- Semantic Service Search Results and category
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
- Take manual control of a request, or operate one already `human_controlled`: `$belong-operate-buying-flow`
- Operational escalation or approval, or to take/release/pause/resume control of a flow: `$belong-inbox`
- Temporary Buying Agent guidance: `$belong-steer-buying-agent`
- Durable Buying Playbook change: `$belong-train-buying-agent`
- Signed/active delivery state: `$belong-check-active-services`
- Trust and Decision Explanation details: `$belong-check-reputation`

## Output

This is a read-only view, so nothing changes. Summarize:

- Which Buying Request(s) the human is looking at, by status and need
- Current pre-contract phase: search, engagement, discovery, proposals, or negotiation
- The most relevant state: results found, feeds open, proposals received, and how they compare
- Authority signals when present: budget, cumulative spend, and whether signature is within Standing Authorization
- Any linked Marketplace Inbox items that need the human, and the Audit Log path for detail
- Anything notable the structured view does not capture: risks, anomalies, or approaching deadlines
- Recommended next skill or action, without taking it here

Always remind the human that this skill only reads state. To act, route to `$belong-start-buying-request` for a new need, `$belong-inbox` for approvals, the steering or training skills for behavior, or `$belong-check-active-services` once a proposal is signed.
