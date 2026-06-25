---
name: belong-internal-disputes
description: Internal Belong admin/arbiter capability for mocked Belong marketplace disputes. Use when the Belong admin reviews a contested Active Service and issues the binary, full-only verdict (refund the buyer or release escrow to the provider). No party negotiation and no autonomous AI judge in this phase.
---

# Belong Internal Disputes

Use this when delivery, payment, contract/SOW compliance, acceptance, or conduct on an Active Service is contested and a Belong admin/arbiter must resolve it. This is the internal admin capability. The buyer-side and seller-side humans only file or withdraw a Dispute through `$belong-manage-dispute`, and see dispute work through `$belong-inbox`, `$belong-check-active-services`, and `$belong-check-reputation`.

In this phase there is no party back-and-forth and no autonomous AI judge. Belong assembles the evidence from the audit trail, and a Belong admin issues a single binary verdict.

## Start

Run runtime `status` and inspect open dispute inbox items. Identify:

- Active Service
- Contract/SOW obligation at issue (`kind`: deliverable_rejection, sla_determination, charge_disagreement, other)
- The opening statement and the claimant's side
- Evidence assembled from the audit trail (executed contract/SOW, acceptance criteria, evidence packages, payment ledger, messages)

## Guided Actions

A Dispute moves through a fixed lifecycle: `opened` → `under_review` → `resolved` | `withdrawn`. Use:

- `dispute-review --dispute-id <id>` for the admin to take an opened Dispute under review.
- `dispute-resolve --dispute-id <id> --resolution <refund_buyer|release_provider> [--notes "<rationale>"]` for the admin's binary, full-only verdict. `refund_buyer` refunds the full escrow to the buyer; `release_provider` releases the full escrow (minus the platform fee) to the provider. Partial or split outcomes are not supported.

Resolution is admin-only. The parties cannot resolve a Dispute, and the claimant can only withdraw it (`dispute-withdraw`) before it is resolved.

## Output

Summarize Dispute status, the `kind` and opening statement, the evidence considered, the binary verdict (`refund_buyer` or `release_provider`) and its full refund/release effect on the payment ledger, the reputation impact on both sides, pending inbox items, and the audit path.
