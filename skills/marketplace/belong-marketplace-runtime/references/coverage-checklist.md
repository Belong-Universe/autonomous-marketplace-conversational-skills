# Coverage Checklist

The mocked Skill Pack must cover all resolved PRD/Q&A functionality.

## Human Surface

- OAuth-style login is mocked once, then all work stays in the agentic application.
- Only two human user types exist: Service Provider human and buyer-side human.
- Humans operate, approve, override, pause, supervise, and handle escalations through their own agents.
- Notification channels point humans back to the agentic app and Marketplace Inbox.
- Seller-side orientation always names the Service Provider human, Service, Selling Agent, buyer-side object, billing/collections state, fulfillment state, and seller inbox work.
- Marketplace Inbox is the canonical next-work list; stale, duplicate, superseded, or already-satisfied items must be resolved or called out before declaring work complete.
- Shared human skills cover setup, inbox, Active Service checks, payment checks, reputation/audit/explanation checks.
- Buyer-specific human skills cover Buying Agent training/retraining, starting a Buying Request from buyer intent, continuing Buying Agent autonomous work, checking the pre-contract buyer pipeline, and temporary Buying Agent steering.
- Seller-specific human skills cover Selling Agent training/retraining, continuing Selling Agent autonomous work, checking the seller inbound pipeline, and temporary Selling Agent steering.

## Agents And Training

- Belong agents only; no bring-your-own-agent.
- Buying Agent training creates a Buying Playbook with buying goals, provider preferences, budget, RFP/selection rules, proposal comparison, contract authority, payment rules, acceptance criteria, escalation rules, dispute posture, rating rules, and optimization goals.
- Selling Agent training creates a Service Playbook for one Service with description, tags, discovery, pricing, monetization, billing, collections, contract/SOW behavior, negotiation limits, delivery, evidence, meetings, escalations, disputes, reputation, and Standing Authorization.
- Setup, Training, Validation, and Production phases are explicit.

## Marketplace Lifecycle

- Lifecycle order is enforced; downstream objects are not created before required predecessors.
- Buying Request
- Buyer-side human intent starts through a Buying Request, not a Steering Instruction.
- Semantic-first Service search with optional tags
- Ranked Service Search Results with Service, provider identity, Selling Agent reputation, price/timeline signals, availability, and supported terms
- Direct or competitive Engagement Feed
- Seller-led Discovery Questionnaire
- Proposal as seller-signed Service Contract/SOW, not a separate document
- Negotiation/iteration
- Buyer signature within Standing Authorization or human approval
- Active Service
- Stripe Payment Stack mock with authorizations, charges, holds, releases, refunds, collections, seller-side platform fee, and merchant-of-record distinction
- Payment ledger summaries show event type, gross amount, platform fee, seller net, hold/release/refund/collection state, linked contract/SOW or Change Order, and audit path.
- Budget and authority checks include cumulative spend across proposals, active services, holds, charges, releases, refunds, collections, composite requests, and pending Change Orders.
- Legal Layer mock with signing provider, contract/SOW versions, approvals, obligations, evidence, and audit

## Production Operation

- Marketplace Inbox with information, authorization, instruction/execution, fulfillment, meeting, dispute, payment exception, Change Order approval, pause/resume, and operational intervention requests
- Fulfillment Tasks for provider-side delivery work
- Human-to-Human Meetings with prep and follow-up
- Deliverable Evidence Packages
- Delivery Acceptance: accept, reject, request revision, or dispute
- Change Orders as signed contract/SOW amendments that state scope, price, timeline, deliverable, approval/signature, payment ledger impact, and acceptance evidence changes
- Human Override and Agent Pause
- Agent Pause blocks new autonomous search engagement, proposals, negotiations, signatures, Change Orders, payment movement, optimization, and steering while preserving obligations, required notices, deadlines, payment alerts, disputes, and escalations
- Disputes managed by agents
- Belong Judge autonomous decision
- Belong human judge escalation
- Agent Reputation outcome and conduct events
- Buyer ratings and search/trust impact
- Complete Audit Log
- Decision Explanations from audit evidence without raw model reasoning; include object IDs, timestamps, Playbook rule/version, authority result, cumulative spend when relevant, inbox approvals, contract/payment/evidence links, and outcome
- Composite Buying Request
- Provider Optimization
- Selling Optimization
- Durable Playbook changes through training/retraining skills; direct instructions, Inbox approvals, steering, and one-off overrides are not durable Playbook changes
- Steering Instructions as temporary, auditable guidance inside existing Playbook and Standing Authorization
- Training Recommendations from Provider Optimization and Selling Optimization that are reviewed through training/retraining, not Inbox
- Marketplace Privacy Promise
- Marketplace Learning Boundary and network-effect explanation
