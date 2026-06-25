---
name: belong-manage-dispute
description: Shared human-facing cockpit for participating in a Belong Dispute on an Active Service. Use when a buyer-side or seller-side human wants to open a Dispute, state their position with evidence, respond to the other side, ask the Belong Judge to decide, escalate to a Belong human judge, or understand the payment and reputation outcome. Role-aware; not the Judge.
---

# Belong Manage Dispute

**Communication:** follow the Belong Communication Standard in `voice.md` — apply its voice and use its verbatim scripts (filling the `<slots>`) for every human-facing message.

Use this when contested delivery, payment, contract/SOW compliance, acceptance, evidence, or conduct needs a human to drive the Dispute: "this delivery is wrong", "they never paid", "I want to dispute this", "respond to their claim", or "escalate to a human judge."

This is the human's cockpit to **participate** in a Dispute. It does not adjudicate. The autonomous Belong Judge decides first; the human can escalate further to a Belong human judge. The Judge's logic lives in `$belong-internal-disputes` (internal). Payment hold/release/refund and reputation effects are runtime-driven outcomes, not chosen here.

It is role-aware: detect whether this human is buyer-side or seller-side and use that side for every command (`--opened-by`, `--actor`). A buyer-side human cannot file or respond as the seller, and vice versa.

## Preconditions (run first, every time)

1. Run runtime `status`. A Dispute only exists on an **Active Service** (post-contract). If there is no Active Service, there is nothing to dispute yet — route to `$belong-check-active-services` or `$belong-inbox`.
2. Identify the Active Service, the contested obligation, the relevant Deliverable Evidence Package, and the payment state. `$belong-check-active-services` and `$belong-check-payments` give this detail.
3. Confirm the human's side (buyer or seller). Use it consistently below.

## Guided Flow

Run from the runtime root:
`python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py <command>`

1. **Open the Dispute** (if not already open):
   ```bash
   dispute-open --active-service-id <id> --opened-by <buyer|seller> --reason "<what is contested>" --evidence "<links or description>"
   ```
   Capture a clear, specific reason and the strongest evidence the human has. Disputes are decided on the executed contract/SOW, acceptance criteria, evidence packages, payment ledger, messages, and reputation history — so help the human point at those, not at sentiment.

2. **Respond to the other side's position:**
   ```bash
   dispute-respond --dispute-id <id> --actor <buyer|seller> --response "<the human's position>"
   ```
   Show the other side's latest response, then record the human's. Keep it factual and tied to the contract/SOW and evidence.

3. **Ask the Belong Judge to decide** (first-layer autonomous adjudication, once positions are in and agents cannot resolve it):
   ```bash
   judge --dispute-id <id>
   ```
   Explain that the Judge reviews the executed contract/SOW, evidence packages, acceptance criteria, payment ledger, messages, dispute responses, and reputation history, and that the decision carries payment and reputation consequences for both sides.

4. **Escalate to a Belong human judge** (only if the autonomous decision is unsatisfactory):
   ```bash
   judge --dispute-id <id> --escalate-human --reason "<why human review is needed>"
   ```
   This requests human review; evidence and payment holds stay visible in the Inbox until the human-judge outcome is mocked.

5. **Read the outcome.** After a decision, summarize it and route the human to `$belong-check-active-services` (delivery/payment effect) and `$belong-check-reputation` (Reputation Events). A "Review Belong Judge decision" item appears in `$belong-inbox` for both sides.

## Boundaries

- Active Services only: there is no Dispute pre-contract. A contested proposal is a negotiation, not a Dispute — use `$belong-steer-*`, `$belong-operate-*`, or `$belong-check-buying-requests`/`$belong-check-selling-pipeline`.
- Not the Judge: the human states a position and may escalate, but does not issue the decision. The autonomous Belong Judge and any Belong human judge own adjudication (`$belong-internal-disputes`).
- Role-locked: act only as the human's own side. Never file or respond as the other party.
- Outcomes are runtime-driven: payment hold/release/refund and Reputation Events follow the decision; this skill does not set them.
- Not training or steering: durable policy (dispute posture, escalation thresholds) belongs in `$belong-train-buying-agent` / `$belong-train-selling-agent`; temporary nudges in `$belong-steer-*`.
- Opening a Dispute is also available as a shortcut inside `$belong-operate-buying-flow` / `$belong-operate-selling-flow`; this skill owns the full multi-step participation (open, respond, judge, escalate, read outcome).

## Output

Summarize: the Active Service and contested obligation, the Dispute id and status, each human action taken (open/respond/judge/escalate) and its result, the decision when present with its payment and reputation implications, whether it came from agents, the Belong Judge, or a Belong human judge escalation, pending Marketplace Inbox items, the Audit Log path, and the next skill — usually `$belong-check-active-services`, `$belong-check-payments`, `$belong-check-reputation`, or `$belong-inbox`.
