# Buying Goals And Needs

[Back to index](index.md)

Status: Done
Approval: Approved

## Playbook Rules

- Pagora buys recurring and ad-hoc security assurance work. The standing category covers external penetration tests, API security audits, and SOC 2 readiness reviews.
- For each purchase, the binding need, scope, success criteria, and deadline arrive on the Buying Request (`--need`, `--needed-services`, `--timeline`). The playbook only defines how to scope and qualify, not the specific purchase.
- A well-formed security purchase must state: the assets in scope (apps, APIs, environments), the test type, whether a report and a re-test are required, and any compliance driver (SOC 2, customer due diligence, regulator).
- Default success criteria for a pentest purchase: a written report with severity-ranked findings, evidence/repro steps, an executive summary, and one free re-test of remediated criticals within 30 days.
- Treat any purchase as out of scope if it requires production data exfiltration, social engineering of named employees, or testing assets Pagora does not own, unless Daniela explicitly approves it.
- Useful search tags: `penetration-testing`, `api-security`, `application-security`, `soc2-readiness`, `security-audit`.

## Worked Example (this purchase)

- Need: external penetration test + API security audit of the Pagora public API and merchant dashboard.
- Scope: 2 web apps, 1 REST API (~40 endpoints), staging environment.
- Success criteria: severity-ranked report + exec summary + one re-test of criticals.
- Deadline: report due before the September SOC 2 audit window.
- Recurrence: annual, plus ad-hoc after major releases.

## Still Missing

- `-` (section complete for the standing category; per-purchase scope always arrives on the Buying Request).

## Source Notes

- Pagora past pentest RFPs (2024, 2025) for default scope and success criteria.
- Daniela confirmed the standing security-assurance category and the out-of-scope guardrails.
