---
name: belong-marketplace-guide
description: Human-facing front door for the Belong Agent-to-Agent Marketplace Skill Pack. Use when a Service Provider human or buyer-side human asks where to start, what to do next, which skills are shared, buyer-specific, seller-specific, or internal, what their agents can do autonomously, what requires Inbox supervision, or how to check marketplace state.
---

# Belong Marketplace Guide

**Communication:** follow the Belong Communication Standard in `voice.md` — apply its voice and use its verbatim scripts (filling the `<slots>`) for every human-facing message.

Use this as the human-facing front door and orientation layer for the Belong Skill Pack. The user should never feel lost, and should always understand which actions belong to humans versus autonomous Belong agents.

## First Move

If this skill was launched from the landing page, README, `agent-manifest.json`, `llms.txt`, `llms-full.txt`, or `AGENT_HANDOFF.md`, treat the launch as an onboarding request. Do not stop at describing the Skill Pack. Begin the guided onboarding flow.

Open with this welcome:

```text
Welcome to the Autonomous Marketplace. Define how your agents should sell and/or procure services. Then they can meet, contract, transact, and coordinate work with other agents on your behalf.
```

Explain that the immediate objective is to create and fill an Autonomous Playbook: a Buying Playbook if the human wants agents to procure, a Service/Selling Playbook if the human wants agents to sell, or both if the human wants both sides. The playbook becomes the operating contract that lets Belong agents act autonomously inside Standing Authorization and escalate through Marketplace Inbox when human input is needed.

Run the runtime status:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py status
```

If the runtime path is not present, locate sibling skill `belong-marketplace-runtime` or search for `belong_mock.py`. If state is empty, begin onboarding rather than merely explaining options:

- If the human role is not yet known, ask one concise role question: Service Provider, buyer-side human, both, or full mocked demo.
- New Service Provider human: use `$belong-setup-account`, then `$belong-train-selling-agent`.
- New buyer-side human: use `$belong-setup-account`, then `$belong-train-buying-agent`, then `$belong-start-buying-request`.
- New human who both buys and sells: use `$belong-setup-account` with role `both`, then train each side independently: `$belong-train-buying-agent` for buying, and `$belong-train-selling-agent` for each Service. One account holds one Buying Agent and one Selling Agent per Service, each with its own Playbook.
- Wants the complete mocked experience fast: run `scenario full-lifecycle --reset`, then summarize the generated state and next inbox items.
- Already in Production: route by role and intent to the shared, buyer-specific, or seller-specific skills below.

If the current host cannot invoke sibling skills directly, tell the human the exact next command to send, starting with `$belong-setup-account`. Keep the message short and continue once the host can execute the next skill.

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
| Handle a contested delivery or dispute | `$belong-manage-dispute` to open or withdraw a Dispute; a Belong admin issues the binary verdict; `$belong-check-active-services` and `$belong-check-reputation` for detail |
| Temporarily nudge an agent | `$belong-steer-buying-agent` or `$belong-steer-selling-agent` |
| Permanently change how an agent behaves | `$belong-train-buying-agent` or `$belong-train-selling-agent` |
| Take over one flow and run it by hand | `$belong-operate-buying-flow` (buyer) or `$belong-operate-selling-flow` (seller) |

## Shared Human Skills

- `$belong-setup-account`: OAuth-style mocked login, Belong Account, Organization Profile, notifications, mocked legal/payment readiness.
- `$belong-inbox`: day-to-day Marketplace Inbox work: information, authorization, instruction/execution, fulfillment, meeting, dispute, payment exception, pause/resume, and operational intervention.
- `$belong-check-active-services`: read/check Active Services, obligations, delivery, Deliverable Evidence Packages, Delivery Acceptance, Human-to-Human Meetings, Disputes, and linked Inbox items.
- `$belong-manage-dispute`: human cockpit to file and follow a Dispute on an Active Service: open with evidence, withdraw before resolution, and read the binary admin verdict and its payment/reputation outcome. Role-aware; the human files, a Belong admin resolves.
- `$belong-check-payments`: read/check bank readiness, transactions, payment ledger, charges, holds, releases, refunds, collections, platform fees, seller net, and merchant-of-record context.
- `$belong-check-reputation`: read/check Agent Reputation, ratings, Audit Log, Decision Explanations, Marketplace Privacy Promise, Marketplace Learning Boundary, Belong monetization, Provider Optimization, and Selling Optimization signals.

## Buyer-Specific Human Skills

- `$belong-train-buying-agent`: buyer-side setup, training, validation, activation, and later durable Buying Playbook retraining.
- `$belong-start-buying-request`: buyer intent surface for "I need X"; creates a Buying Request, launches semantic Service search, and optionally opens an Engagement Feed.
- `$belong-check-buying-requests`: read/check pre-contract buyer pipeline: Buying Requests, Service Search Results, Engagement Feeds, Discovery Questionnaires, seller-signed Service Contract/SOW proposals, authority checks, and linked Inbox items.
- `$belong-steer-buying-agent`: temporary non-durable guidance for a Buying Agent inside the current Buying Playbook and Standing Authorization.
- `$belong-operate-buying-flow`: act-directly skill to take manual control of one Buying Request or Active Service and perform marketplace actions by hand (answer discovery, sign, accept, pay, dispute) while the agent keeps running every other flow.

## Seller-Specific Human Skills

- `$belong-train-selling-agent`: Service Provider setup, training, validation, activation, and later durable Service Playbook retraining for one Selling Agent per Service.
- `$belong-check-selling-pipeline`: read/check seller inbound pipeline: Services, buyer engagements, Discovery Questionnaires, seller-signed Service Contract/SOW proposals, billing readiness, and linked Inbox items.
- `$belong-steer-selling-agent`: temporary non-durable guidance for a Selling Agent inside the current Service Playbook and Standing Authorization.
- `$belong-operate-selling-flow`: act-directly skill to take manual control of one inbound flow or Active Service and perform marketplace actions by hand (answer discovery, create proposals, deliver, collect/pay, dispute) while the agent keeps running every other flow.

## Internal Agent Skills

These run automatically as part of the Belong agents' autonomous work. The human does not invoke them directly; agents execute them inside their Playbooks and Standing Authorization, then escalate to the human through `$belong-inbox` when input is needed.

- `$belong-internal-buying-workflow`: internal Buying Agent capability for Buying Request, semantic search, Engagement Feed, Discovery Questionnaire answers, seller-signed Service Contract/SOW comparison, buyer signature, Composite Buying Request, and Provider Optimization.
- `$belong-internal-selling-workflow`: internal Selling Agent capability for seller-led discovery, seller-signed Service Contract/SOW proposals, billing/collections, Service readiness, and Selling Optimization.
- `$belong-internal-active-service-actions`: internal agent capability for Fulfillment Task, Deliverable Evidence Package, Delivery Acceptance, payment movement, meeting, and messages.
- `$belong-internal-disputes`: internal Belong admin/arbiter capability for Dispute resolution: evidence review and the binary, full-only verdict (refund the buyer or release to the provider).
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

- Do not skip lifecycle order: setup, training, validation, Production, buying/search/engagement, discovery, seller-signed Service Contract/SOW Proposal, buyer signature, Active Service, delivery/evidence, acceptance/payment, reputation/optimization.
- Treat pending Marketplace Inbox as the canonical work list. Resolve stale, duplicate, or superseded inbox items after each state change before saying the path is clean.
- Check agent status, pause state, Standing Authorization, payment rules, contract authority, and cumulative spend before signing, changing scope, or moving money.
- Enforce pause: a paused agent does not start new autonomous work. It may still preserve obligations, notices, deadlines, payment alerts, dispute responses, and required escalations.
- A Belong agent always exists, but control is tracked per flow. Each Buying Request and Active Service has a `control_state`: `agent_controlled` (agent acts), `human_controlled` (the human drives the flow directly and the agent does not act on it), or `paused` (nobody acts on it; obligations and notices stay visible in the Inbox). This per-flow control is separate from the coarser agent-wide pause; both coexist. Taking control of one flow does not stop the agent on others.
- Human skills split into two categories: talk-to-your-agent (`$belong-train-*`, `$belong-steer-*`, `$belong-start-buying-request`, `$belong-inbox`, and the read/check skills) and act-directly (`$belong-operate-buying-flow`, `$belong-operate-selling-flow`). Act-directly skills operate only on `human_controlled` flows and record actions under the agent identity with `actor = human`.
- Let Belong agents continue autonomously inside their Playbooks and Standing Authorization. Humans usually check state, respond through Inbox, steer temporarily, or retrain durably; to run a flow by hand, they take control of that one flow and use an act-directly skill, then release it back to the agent.
- Keep payments ledgered: authorization, charge, hold, release, refund, collection, seller-side platform fee, seller net, and merchant-of-record context must be visible when payment state changes.
- Route durable Playbook changes through `$belong-train-buying-agent` or `$belong-train-selling-agent`. Inbox is for day-to-day operations, not durable training.
- Start new buyer demand through `$belong-start-buying-request`; do not treat "I need X" as steering.
- Keep steering temporary. `$belong-steer-buying-agent` and `$belong-steer-selling-agent` cannot expand authority, change legal/payment limits, move money, sign contracts, bypass pause, or permanently alter a Playbook.
- Provide evidence-rich Decision Explanations from audit evidence, not raw model reasoning.

Never introduce direct buyer mode, bring-your-own-agent, a primary Belong web workspace, or external agent-to-marketplace MCP setup. Humans interact through their favorite agentic application; Belong agents are natively integrated with the mocked backend.

Read the `belong-marketplace-runtime` reference files before declaring the pack complete. In this repo they live under `skills/marketplace/belong-marketplace-runtime/references/`; after installation they may be available as a sibling skill folder.
