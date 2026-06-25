---
name: belong-internal-buying-workflow
description: Internal Buying Agent capability for Production buying workflows in the mocked Belong marketplace. Use when the Belong Buying Agent autonomously runs Buying Requests, semantic Service search with an optional category filter, ranked Service Search Results, direct or competitive Engagement Feeds, seller-led Discovery Questionnaire answers, seller-signed Service Contract/SOW proposal comparison, buyer signature, Active Service creation, Composite Buying Requests, and Provider Optimization.
---

# Belong Internal Buying Workflow

Use this once the Buying Agent is in Production. This is an internal agent capability, not the primary human-facing surface. Humans start buyer intent through `$belong-start-buying-request`, then the Buying Agent continues autonomously inside the Buying Playbook and Standing Authorization. Humans check the pre-contract pipeline through `$belong-check-buying-requests`, supervise escalations through `$belong-inbox`, give temporary guidance through `$belong-steer-buying-agent`, and make durable Buying Playbook changes through `$belong-train-buying-agent`.

## Start

Run runtime `status` to confirm preconditions. This workflow only runs when a Buying Agent is already in Production; surfacing training to the human is owned by the human-facing `$belong-start-buying-request`. If the precondition is not met, stop instead of proceeding. If no Services exist, the runtime can seed a mocked catalog during search.

Inspect pending buyer inbox items before creating new work. Clear stale authorizations, duplicate information requests, and old payment approvals before reporting that nothing is blocked.

## Buying Request

For a new need, collect:

- Need/outcome
- Budget and timeline
- Cumulative spend cap, existing committed spend, and payment rules
- Constraints
- Direct engagement or competitive feed
- Whether the request may become composite

Run `buying-request`, then `search`.

## Search And Engagement

Explain that search is semantic-first with an optional Service Category filter. Results represent Services, not companies as the primitive. Each result must show Service fit, provider identity, Selling Agent reputation, price/timeline signals, availability, and supported contract/SOW terms.

Engage one result directly or several competitively:

1. `engage`
2. `answer-discovery`
3. `create-proposals`

Discovery is seller-led through questionnaires. The `create-proposals` step does not author a buyer document; it elicits the seller-signed Service Contract/SOW from each engaged Selling Agent, already signed by the seller and awaiting buyer signature.

## Proposals And Signature

Treat each Proposal as the seller-signed Service Contract/SOW awaiting buyer signature. Never create an intermediate proposal document.

Guide:

- `compare-proposals`
- `sign` only after checking Standing Authorization, contract authority, payment rules, paused state, and cumulative spend across this request, related composite requests, active services, holds, charges, and pending Change Orders

Escalate through `$belong-inbox` when the best action exceeds budget, creates unclear cumulative spend, changes legal terms, requires a payment exception, or needs buyer judgment. Buyer signature creates the Active Service. Any scope, price, timeline, or deliverable change after signature belongs to internal Active Service actions as a Change Order.

When payment state changes at signature, summarize the ledger expectation: authorization or charge, gross amount, seller-side platform fee, seller net, payer, merchant-of-record distinction, and audit path.

## Composite And Optimization

Use `composite-request` when one buyer goal coordinates multiple Selling Agents or Active Services. Use `optimization` for continuous Provider Optimization: better providers, better deals, complementary Services, or value improvements. Optimization can create training recommendations, but durable behavior changes are applied through `$belong-train-buying-agent`, not Inbox.

## Output

After every step, summarize the current Buying Request, Engagement Feed, Proposal/contract status, cumulative spend/authority result, payment ledger state, stale or pending inbox items, escalation state, and next human-facing skill only when human attention is needed: usually `$belong-check-buying-requests`, `$belong-inbox`, `$belong-check-active-services`, `$belong-check-payments`, `$belong-check-reputation`, `$belong-steer-buying-agent`, or `$belong-train-buying-agent`.
