---
name: belong-manage-dispute
description: Shared human-facing cockpit for participating in a Belong Dispute on an Active Service. Use when a buyer-side or seller-side human wants to open a Dispute with evidence, withdraw a Dispute they opened, or understand the binary admin verdict and its payment and reputation outcome. Role-aware; the human files, a Belong admin resolves.
---

# Belong Manage Dispute

**Communication:** follow the Belong Communication Standard in `voice.md` — apply its voice and use its verbatim scripts (filling the `<slots>`) for every human-facing message.

Use this when contested delivery, payment, contract/SOW compliance, acceptance, or conduct needs a human to file a Dispute: "this delivery is wrong", "they never paid", "I want to dispute this", or "withdraw my dispute."

This is the human's cockpit to **file and follow** a Dispute. It does not adjudicate. A Belong admin/arbiter is the only one who resolves a Dispute, with a binary, full-only verdict: refund the buyer or release escrow to the provider. There is no party back-and-forth and no autonomous AI judge in this phase — Belong assembles the evidence from the audit trail and the admin decides. The admin verdict logic lives in `$belong-internal-disputes` (internal). Payment refund/release and reputation effects are runtime-driven outcomes, not chosen here.

It is role-aware: detect whether this human is buyer-side or seller-side and use that side for `--opened-by`. A buyer-side human cannot file as the seller, and vice versa. Only the side that opened a Dispute can withdraw it.

## Preconditions (run first, every time)

1. Run runtime `status`. A Dispute only exists on an **Active Service** (post-contract). If there is no Active Service, there is nothing to dispute yet — route to `$belong-check-active-services` or `$belong-inbox`.
2. Identify the Active Service, the contested obligation, the relevant Deliverable Evidence Package, and the payment state. `$belong-check-active-services` and `$belong-check-payments` give this detail.
3. Confirm the human's side (buyer or seller). Use it consistently below.

## Guided Flow

Run from the runtime root:
`python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py <command>`

1. **Open the Dispute** (if not already open):
   ```bash
   dispute-open --active-service-id <id> --opened-by <buyer|seller> --kind <deliverable_rejection|sla_determination|charge_disagreement|other> --reason "<what is contested>" --evidence "<links or description>"
   ```
   Pick the `--kind` that fits the grievance and capture a clear, specific reason with the strongest evidence the human has. Disputes are decided on the executed contract/SOW, acceptance criteria, evidence packages, payment ledger, and messages that Belong assembles from the audit trail — so help the human point at those, not at sentiment. There is no response step: once filed, the dispute waits for the Belong admin verdict.

2. **Withdraw the Dispute** (only the side that opened it, only before it is resolved):
   ```bash
   dispute-withdraw --dispute-id <id> --reason "<why you are withdrawing>"
   ```
   On withdrawal the Active Service returns to its prior delivery state and no escrow moves.

3. **Read the outcome.** Once a Belong admin resolves the Dispute (`refund_buyer` or `release_provider`), summarize the verdict and route the human to `$belong-check-active-services` (delivery/payment effect), `$belong-check-payments` (the refund or release), and `$belong-check-reputation` (Reputation Events). A "Review dispute resolution" item appears in `$belong-inbox` for both sides.

## Boundaries

- Active Services only: there is no Dispute pre-contract. An unsigned proposal you do not want is not a Dispute — simply decline it or take the flow over with `$belong-steer-*`, `$belong-operate-*`, or review it through `$belong-check-buying-requests`/`$belong-check-selling-pipeline`.
- The human files; the admin resolves: the human opens or withdraws a Dispute but never issues the verdict. Resolution is admin-only and binary (refund the buyer or release to the provider), full amount only — no partial or split outcomes, and no party negotiation (`$belong-internal-disputes`).
- Role-locked: file only as the human's own side, and only the opener can withdraw.
- Outcomes are runtime-driven: the full refund or release and the Reputation Events follow the admin verdict; this skill does not set them.
- Not training or steering: durable policy (dispute posture, escalation thresholds) belongs in `$belong-train-buying-agent` / `$belong-train-selling-agent`; temporary nudges in `$belong-steer-*`.
- Opening a Dispute is also available as a shortcut inside `$belong-operate-buying-flow` / `$belong-operate-selling-flow`; this skill owns filing, withdrawing, and reading the outcome.

## Output

Summarize: the Active Service and contested obligation, the Dispute id, kind, and status (`opened`/`under_review`/`resolved`/`withdrawn`), each human action taken (open/withdraw) and its result, the admin verdict when present (`refund_buyer` or `release_provider`) with its payment and reputation implications, pending Marketplace Inbox items, the Audit Log path, and the next skill — usually `$belong-check-active-services`, `$belong-check-payments`, `$belong-check-reputation`, or `$belong-inbox`.
