# Provider Preferences

[Back to index](index.md)

Status: Done
Approval: Approved

## Playbook Rules

- Hard requirements (a provider that misses any of these is disqualified, never engaged or ranked):
  - ISO 27001 certification.
  - SOC 2 Type II report available under NDA.
  - At least one OSCP- or CREST-certified tester on the engagement.
  - Minimum 3 years of penetration-testing delivery.
  - Based in an approved jurisdiction (US, EU, UK, Canada, or LATAM-approved list).
  - Marketplace reputation at or above 4.2 / 5.
- Preferences (weight the ranking, but are not pass/fail):
  - Prior experience with payments/fintech APIs.
  - Provides a free re-test of remediated criticals.
  - Existing relationship with Pagora (give a moderate edge, not an automatic win).
- Blocked: any provider with an unresolved data-handling incident in the last 24 months, or outside approved jurisdictions.
- The agent may engage a brand-new provider that meets all hard requirements on its own; it flags for Daniela only when a hard requirement is met by exception (for example a SOC 2 in progress but not yet issued).

## Worked Example (this purchase)

- Search returned 5 candidates; 2 were dropped automatically (one lacked SOC 2, one had a 4.0 reputation).
- 3 qualified; the existing-relationship vendor got a moderate edge in ranking.

## Still Missing

- `-`

## Source Notes

- Pagora Security vendor requirements (Confluence) for ISO 27001 / SOC 2 / tester certs.
- Preferred & blocked vendor list. Daniela set the 4.2 reputation floor and the 3-year minimum.
