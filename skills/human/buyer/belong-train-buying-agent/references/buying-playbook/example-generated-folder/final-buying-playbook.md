# Final Buying Playbook

[Back to index](index.md)

Status: Done

Organization: Pagora · Owner: Daniela · Phase: Production · Activated 2026-06-16

Consolidated after all ten sections were approved. This is the durable policy; per-purchase numbers (need, budget, ceiling, deadline) arrive on each Buying Request.

## 1. Buying Goals And Needs

Standing category: security assurance — external pentests, API security audits, SOC 2 readiness. Each purchase must state assets in scope, test type, report/re-test needs, and compliance driver. Default success criteria: severity-ranked report + exec summary + evidence + one re-test of criticals within 30 days. Out of scope without explicit approval: production data exfiltration, social engineering, testing non-owned assets.

## 2. Budget And Payment

USD, net-30 on accepted delivery, no deposits. Upfront payment needs Finance approval. Default ceiling rule: `max_spend` <= 120% of expected budget unless set otherwise on the Buying Request. `max_spend` is internal. Spend above 5,000 needs VP Finance approval.

## 3. Provider Preferences

Hard requirements: ISO 27001, SOC 2 Type II, OSCP/CREST testers, >= 3 years pentest delivery, approved jurisdiction, reputation >= 4.2. Preferences: fintech experience, free re-test, existing relationship (moderate edge). Blocked: recent unresolved data incident or unapproved jurisdiction.

## 4. Selection And RFP Rules

Competitive by default (3 qualified providers); direct only when Daniela names one. RFP requires scope, certs, methodology, sample report, timeline, re-test, price. Weighted rubric 60/40 quality/price; minimum acceptable score 70/100; disqualify on missing sample, narrowed scope, no re-test, or failed hard requirements.

## 5. Negotiations

Open 10–20% below expected budget; concede ~10% steps, max 3 rounds; never exceed `max_spend`. Trade timeline and payment before price; scope fixed. Use perceived signals (competition, eagerness, deadline, scarcity, reputation). Walk away on quality red lines or unreachable price. Disclosure: never reveal ceiling, weighting, or scores. No-ZOPA: when seller floor > `max_spend`, escalate to the Inbox; never raise the ceiling autonomously.

## 6. Legal And Contracts

Sign autonomously up to 5,000; above that, VP Finance approval. Required: NDA, DPA, liability cap >= contract value, defined deliverables, acceptance/re-test terms, authorization-to-test scope, secure report delivery. Acceptance ties to payment release. Change Orders for added scope/re-test/extension. Never accept (without approval): unlimited liability, IP assignment of Pagora data, auto-renewal, or removal of the re-test obligation.

## 7. Escalations

Escalate on: spend > 5,000, any upfront payment, no-ZOPA, protected/never-accept terms, no proposal >= 70, or a hard requirement met by exception. Routing: VP Finance for spend/authority, Daniela for security/legal/scheduling. Slack notifications. Pause/resume via `override`. Every escalation carries a Decision Explanation.

## 8. Disputes And Reputation

Rework-first via the re-test obligation; formal dispute only on refusal or failed quality, with evidence against the acceptance criteria. Prefer rework over refund for security work. Belong Judge on contested rejection; human review when material or data exposed. Rate on report quality, finding accuracy, professionalism, re-test responsiveness; never penalize many criticals. Feed outcomes into Provider Optimization.

## 9. Optimization Objective

Maximize quality and trust, then minimize cost (60/40). Tie-break: reputation, then existing relationship. Inherited by selection and negotiation. Build a 2–3 provider trusted roster. Speed outranks quality only against a real deadline.

## 10. Human-To-Human Meetings

Pre-contract scoping calls when scope is ambiguous or assets sensitive. Daniela attends security scoping calls. Preferred window Tue–Thu 9:00–12:00 America/Bogota. Agent confirms inside the window autonomously; outside it, or for exec/travel, escalates. Calendly handshake; max two counter-proposal rounds; high urgency for deadline-bound calls.
