# Source Prefill

[Back to index](index.md)

Status: Done

## Sources Reviewed

| Source | Access status | Sections informed | Confidence | Gaps |
| --- | --- | --- | --- | --- |
| Pagora Procurement Policy v3 (PDF) | Accessed | Budget And Payment, Legal And Contracts, Escalations | High | per-category ceilings |
| Delegation-of-Authority matrix (sheet) | Accessed | Legal And Contracts, Escalations | High | none |
| Preferred & blocked vendor list (sheet) | Accessed | Provider Preferences | High | reputation thresholds |
| Security vendor requirements (Confluence) | Accessed | Provider Preferences, Selection And RFP Rules | High | none |
| Two past pentest RFPs + scoring sheets | Accessed | Selection And RFP Rules, Optimization Objective | High | none |
| MSA / DPA templates | Accessed | Legal And Contracts | Medium | pentest-specific liability caps |
| 2025 vendor scorecards | Accessed | Disputes And Reputation, Optimization Objective | Medium | rating weights |
| Daniela's working-hours and calendar norms | Provided | Human-To-Human Meetings | High | none |

## Extracted Facts

- Organization: Pagora (payments fintech, ~80 people).
- Buyer-side human owner: Daniela (Head of Security & Compliance).
- Notification channel: Slack.
- Procurement policy: any spend above 5,000 needs VP Finance approval; any upfront (pre-delivery) payment needs Finance approval regardless of amount.
- Standard payment terms are net-30; deposits are discouraged.
- Security vendors must hold ISO 27001 and provide SOC 2 Type II; pentest vendors must have OSCP/CREST-certified testers and at least 3 years of pentest delivery.
- Blocked vendors: any with an unresolved data-handling incident in the last 24 months, or based outside approved jurisdictions.
- Buying priority for security work: quality and trust over price (roughly 60/40).
- Daniela prefers meetings Tue–Thu, 9:00–12:00 America/Bogota.

## Conflicts

- None unresolved. (One: procurement policy implied net-45 in an appendix; Daniela confirmed net-30 is the current standard.)

## Gaps

- Reputation/rating thresholds were not written down; captured from Daniela in section drafting.
- Pentest-specific liability cap added during Legal And Contracts review.

## Initial Prefill Map

| Section | Prefill strength | Source-backed draft available | Still required from Daniela |
| --- | --- | --- | --- |
| Buying Goals And Needs | Medium | Past RFP scope | this purchase's exact scope and deadline |
| Budget And Payment | Strong | Procurement policy | default ceiling rule, disclosure rule |
| Provider Preferences | Strong | Vendor requirements + lists | reputation threshold |
| Selection And RFP Rules | Strong | Past RFPs + scoring sheets | minimum acceptable score |
| Negotiations | Weak | None reliable | opening, concession ladder, walk-away, no-ZOPA |
| Legal And Contracts | Medium | MSA/DoA | pentest liability cap, never-accept list |
| Escalations | Strong | DoA matrix | Slack routing, owners |
| Disputes And Reputation | Medium | Scorecards | dispute posture, rating weights |
| Optimization Objective | Medium | RFP weighting | tie-break rule |
| Human-To-Human Meetings | Medium | Calendar norms | scheduling authority |
