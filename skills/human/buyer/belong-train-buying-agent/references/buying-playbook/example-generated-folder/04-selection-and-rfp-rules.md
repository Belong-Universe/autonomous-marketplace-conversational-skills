# Selection And RFP Rules

[Back to index](index.md)

Status: Done
Approval: Approved

## Playbook Rules

- Sourcing mode: competitive by default for security work; engage 3 qualified providers. Go direct only when Daniela names a provider on the Buying Request.
- RFP must require each seller to answer: scope coverage, tester certifications, methodology (OWASP/PTES), sample redacted report, timeline, re-test policy, and price.
- Comparison rubric (scores feed `compare-proposals`), weighted by the [Optimization Objective](09-optimization-objective.md) 60/40 quality/price split:
  - Methodology & scope coverage — 25%
  - Team certifications & relevant fintech experience — 20%
  - Report & evidence quality (from sample) — 15%
  - Reputation & references — 10% (this is the quality 60%)
  - Price vs expected budget — 30% (this is the price 40%)
- Red flags that disqualify a proposal regardless of score: no sample report, scope narrower than requested, no re-test, or a tester team that fails the hard requirements in [03 Provider Preferences](03-provider-preferences.md).
- Minimum acceptable score to be worth negotiating: 70 / 100. Below that, do not negotiate; widen the search or escalate.

## Worked Example (this purchase)

- 3 qualified proposals scored 82, 78, and 64.
- The 64 was dropped (below 70). The agent advanced the 82 and 78 to negotiation, leading with the 82 (best quality fit), price 2,300.

## Still Missing

- `-`

## Source Notes

- Pagora 2024 and 2025 pentest RFPs and their scoring sheets.
- Daniela set the 70/100 minimum and the disqualifying red flags.
