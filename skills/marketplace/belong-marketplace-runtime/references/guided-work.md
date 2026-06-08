# Guided Work Standard

Use this standard in every Belong Skill Pack flow.

## Start

1. Run runtime `status` unless the current state was just inspected.
2. Name the user's current phase: Setup, Training, Validation, or Production.
3. Identify the human role in this moment: Service Provider human, buyer-side human, or both.
4. Identify the object being created or changed: Belong Account, Organization Profile, Buying Agent, Selling Agent, Service, Buying Request, Engagement Feed, Proposal/Service Contract/SOW, Active Service, Marketplace Inbox item, Dispute, Reputation Event, Audit Log event, Steering Instruction, Training Recommendation, Training Update, or Composite Buying Request.
5. Inspect pending Marketplace Inbox items for the relevant role before starting new Production work.

## Guide

Ask only for missing information needed to safely produce the next structured object. Prefer short groups of questions over a long interview. If the user gives enough information, proceed and create or update the object.

Keep the user oriented with:

- Phase
- Current object
- Lifecycle position and required predecessor
- What the agent can do autonomously
- What will escalate to the human
- Pause state and authority envelope
- Cumulative spend and payment ledger when money can move
- What is mocked
- What happens next

Do not present the experience as command-line usage unless the user asks for raw commands. The runtime commands are backend mechanics for Codex, not the product surface.

## Output

Every flow must end with:

- Structured object created or updated
- Human-readable summary of what changed
- Explicit next steps
- Any Marketplace Inbox items that now need attention, plus stale items resolved or still requiring cleanup
- Audit or Decision Explanation path if the action involved authority, contract terms, payments, disputes, reputation, or human override

## Invariants

Before signing, negotiating, changing scope, moving money, optimizing, or continuing autonomous work, check Production status, pause state, Standing Authorization, Playbook authority, contract/SOW authority, payment rules, cumulative spend, and pending inbox approvals.

Paused agents do not start new autonomous work. They may preserve obligations, required notices, deadlines, payment alerts, disputes, and human escalations.

Durable Playbook changes require the relevant training/retraining skill. Do not treat Inbox approval, steering, direct instruction, override, or one-off approval as a permanent Playbook change.

Marketplace Inbox is for day-to-day operational work: information, authorization, instruction/execution, fulfillment, meeting, dispute, payment exception, Change Order approval, pause/resume, and Active Service intervention.

Buyer-side "I need X" intent creates a Buying Request and starts semantic search. Steering is only temporary, non-durable guidance for an existing agent/object and must stay inside the current Playbook and Standing Authorization.

Continuing autonomous work should go through the role-specific human wrapper skills: `$belong-run-buying-agent` for buyer-side continuation and `$belong-run-selling-agent` for seller-side continuation. Internal workflow skills describe agent capabilities; they are not the normal human product surface.

Payments must stay ledgered. Show authorization, charge, hold, release, refund, collection, gross amount, seller-side platform fee, seller net, merchant-of-record context, linked contract/SOW or Change Order, and audit path whenever payment state changes.

Decision Explanations must cite audit evidence, object IDs, timestamps, Playbook rule/version, authority result, inbox approval, contract/payment evidence, and outcome. Do not reveal raw model reasoning.

## Mock Fidelity

Maintain coherent local JSON state. Use the runtime rather than inventing one-off objects in prose. Enforce basic lifecycle order:

Account -> Agent training -> Validation -> Production -> Buying Request/Search/Engagement -> Discovery -> seller-signed Service Contract/SOW Proposal -> Negotiation -> buyer signature -> Active Service -> Delivery/Evidence -> Acceptance/Payment -> Reputation/Optimization.

Disputes, meetings, fulfillment tasks, change orders, inbox items, overrides, pauses, audit events, and explanations can happen throughout Production.

Change Orders are signed contract/SOW amendments. They must state scope, price, timeline, deliverable, approval/signature, payment ledger impact, and acceptance evidence changes. Unsigned amendments stay pending and visible in the Marketplace Inbox.
