# Skill Pack Review Against Q&A And PRD

This review checks the current Belong Skill Pack against the Linear `Q&A.xml` and `PRD.xml` mirrors. The main product rule is preserved: humans only interact through their favorite agentic application, using the Belong Skill Pack; autonomous marketplace work is performed by Belong Buying Agents and Belong Selling Agents.

## Skill Surface

Shared human skills:

- `belong-marketplace-guide`: front door, routing, status, and buyer/seller/shared explanation.
- `belong-setup-account`: OAuth-style setup, organization profile, notifications, and mocked legal/payment readiness.
- `belong-inbox`: day-to-day operational escalations for both sides.
- `belong-check-active-services`: shared post-signature Active Service view.
- `belong-check-payments`: shared bank, payment, collections, charge, hold, release, refund, fee, and net view.
- `belong-check-reputation`: shared Agent Reputation, audit, Decision Explanation, privacy, and learning-boundary view.

Buyer-specific human skills:

- `belong-train-buying-agent`: initial Buying Playbook setup and durable retraining.
- `belong-start-buying-request`: the buyer-side "I need X" guided work that creates a Buying Request.
- `belong-check-buying-requests`: pre-contract buyer pipeline view.
- `belong-steer-buying-agent`: temporary buyer-side guidance within existing authority.

Seller-specific human skills:

- `belong-train-selling-agent`: initial Service/Selling Playbook setup and durable retraining, one Selling Agent per Service.
- `belong-check-selling-pipeline`: seller inbound pipeline view.
- `belong-steer-selling-agent`: temporary seller-side guidance within existing authority.

Internal agent capabilities:

- `belong-internal-buying-workflow`
- `belong-internal-selling-workflow`
- `belong-internal-active-service-actions`
- `belong-internal-disputes`
- `belong-marketplace-runtime`

## Buyer Experience

1. The buyer-side human sets up a Belong Account, Organization Profile, notification channels, and mocked legal/payment readiness through `belong-setup-account`.
2. The human trains the Buying Agent through `belong-train-buying-agent`, defining budget, provider preferences, selection rules, RFP behavior, Standing Authorization, payment rules, acceptance criteria, dispute posture, escalation thresholds, and provider optimization goals.
3. When the human needs something, they use `belong-start-buying-request`. This creates a Buying Request and can start semantic search, tag-assisted search, and initial engagement.
4. After a Buying Request starts, the Buying Agent continues autonomously inside its Buying Playbook and Standing Authorization: engage one or more Selling Agents, answer seller-led discovery, compare seller-signed Service Contract/SOW proposals, negotiate, sign inside authority, manage Active Service work, create Composite Buying Requests, and run Provider Optimization.
5. The human checks pre-contract work through `belong-check-buying-requests`, post-signature work through `belong-check-active-services`, money through `belong-check-payments`, and trust/audit through `belong-check-reputation`.
6. The Buying Agent escalates operational needs through `belong-inbox`; durable behavior changes go through `belong-train-buying-agent`; temporary guidance goes through `belong-steer-buying-agent`.

## Seller Experience

1. The Service Provider human sets up a Belong Account, Organization Profile, notification channels, and mocked legal/payment readiness through `belong-setup-account`.
2. The human trains one Selling Agent per Service through `belong-train-selling-agent`, defining the Service, tags, buyer personas, use cases, discovery questions, monetization model, billing cycle, collections process, contract/SOW terms, discount limits, scope limits, delivery workflow, evidence requirements, meeting rules, dispute rules, reputation rules, and escalation paths into provider teams.
3. In production, the Selling Agent receives inbound marketplace engagement from Buying Agents. The human checks this pre-contract pipeline through `belong-check-selling-pipeline`.
4. After inbound engagement arrives, the Selling Agent continues autonomously inside its Service Playbook and Standing Authorization: wait for or process discovery answers, send seller-signed Service Contract/SOW proposals, support negotiation, coordinate Active Service delivery, create Fulfillment Tasks, submit Deliverable Evidence Packages, manage collections behavior, and run Selling Optimization.
5. The human checks post-signature work through `belong-check-active-services`, money through `belong-check-payments`, and trust/audit through `belong-check-reputation`.
6. The Selling Agent escalates operational needs through `belong-inbox`; durable Service Playbook changes go through `belong-train-selling-agent`; temporary guidance goes through `belong-steer-selling-agent`.

## Coverage Check

- Belong-only agents, no bring-your-own-agent, no direct buyer mode: covered by guide, setup, training, ADR, runtime rules, and tests.
- OAuth-style account setup, organization ownership, notifications, legal/payment readiness: covered by `belong-setup-account`, mocked state, notification events, and Inbox routing.
- Service as supply primitive and one Selling Agent per Service: covered by `belong-train-selling-agent` and seller pipeline/runtime commands.
- Buying Request as demand primitive: covered by `belong-start-buying-request`, `belong-check-buying-requests`, and Buying Agent runtime.
- Semantic search with optional tags: covered by Buying Request start/search runtime and autonomous buyer flow.
- Engagement Feed, RFP-like competitive engagement, seller-led discovery: covered by autonomous buyer and seller flows plus internal workflows.
- Proposal as seller-signed Service Contract/SOW awaiting buyer signature: covered by seller proposal generation, buyer comparison, negotiation, and signature commands.
- Legal contract/SOW and payment terms: mocked in proposals, signing, Active Service, and payment ledger.
- Active Service, deliverables, evidence, acceptance, messages, meetings, Change Orders, and fulfillment escalations: covered by shared Active Service checks, Inbox, autonomous buyer/seller runtime ticks, and internal Active Service actions.
- Payments, collections, holds, releases, refunds, fees, and seller net: covered by payment runtime and `belong-check-payments`.
- Disputes and Belong Judge autonomous/human escalation: covered by `belong-inbox`, internal disputes, runtime dispute commands, audit, and tests.
- Agent Reputation, audit logs, Decision Explanations, privacy boundary, and learning boundary: covered by `belong-check-reputation`, runtime reputation/audit/explain commands, and documents.
- Human override, pause/resume, and temporary steering: covered by Inbox operational intervention and role-specific steering skills.
- Durable Playbook changes: covered by training/retraining skills, not Inbox.
- Provider Optimization, Selling Optimization, and Composite Buying Requests: covered by autonomous buyer/seller workflows, runtime commands, and tests.

## Gaps Closed In This Refactor

- Added buyer initiation as `belong-start-buying-request` so "I need X" is not confused with steering.
- Added buyer and seller pre-contract read views: `belong-check-buying-requests` and `belong-check-selling-pipeline`.
- Replaced generic steering with role-specific steering: `belong-steer-buying-agent` and `belong-steer-selling-agent`.
- Kept durable Playbook changes in training/retraining skills and removed them from Inbox resolution.
- Moved public skills into shared, buyer, and seller folders while keeping autonomous/internal capabilities separate.
- Removed the public "run my agent" concept. Agents continue autonomously inside Playbooks; humans intervene through Inbox, steering, checks, or retraining.

## Remaining Out Of Scope For The Mock

- Real OAuth, real notification delivery, real e-signature, real Stripe transactions, real semantic search, real Belong agents, real legal facilitation, production dispute adjudication, production permissions, and production security/compliance controls.
- The mocked experience is still expected to cover every product function conversationally and statefully, even where provider integrations are simulated.
