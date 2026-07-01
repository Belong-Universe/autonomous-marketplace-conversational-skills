# Budget And Payment

[Back to index](index.md)

Status: Done
Approval: Approved

## Playbook Rules

- The binding `expected_budget` and `max_spend` (ceiling) for a purchase are set on the Buying Request, not here. The playbook holds the posture and the default rule for choosing a ceiling.
- Default ceiling rule: for standard security-assurance work, set `max_spend` no higher than 120% of the expected budget unless Daniela sets a different ceiling on the Buying Request.
- `max_spend` is internal and is never disclosed to a seller.
- Currency: USD.
- Payment posture: net-30, on accepted delivery. Deposits and any pre-delivery (upfront) payment require Finance approval through the Inbox, regardless of amount.
- Spend above 5,000 requires VP Finance approval before signing (see [06 Legal And Contracts](06-legal-and-contracts.md) and [07 Escalations](07-escalations.md)).
- Disclosure rule: the agent may state budget posture ("that is above our budget for this scope") without revealing the ceiling, the 60/40 weighting, or approval thresholds.

## Worked Example (this purchase)

- On the Buying Request: `--budget 1500 --max-spend 1800`.
- 1,800 is within the default rule (120% of 1,500 = 1,800).
- Payment posture applied: net-30 on accepted delivery, no deposit.

## Still Missing

- `-`

## Source Notes

- Pagora Procurement Policy v3: 5,000 approval threshold, upfront-payment rule, net-30 standard.
- Daniela set the 120% default ceiling rule and confirmed deposits are discouraged.
