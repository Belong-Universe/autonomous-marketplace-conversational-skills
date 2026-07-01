# Runtime Mapping

[Back to index](index.md)

Status: Done

Per-purchase numbers (`--need`, `--needed-services`, `--timeline`, `--budget`, `--max-spend`, `--constraints`) are supplied on each `start-buying-request`, not at training. The defaults below are the durable posture; the binding values for a given purchase always come from its Buying Request.

## `train-buying` Arguments

- `--human-name`: Daniela
- `--org-name`: Pagora
- `--org-kind`: company
- `--notifications`: Slack
- `--goals`: Recurring and ad-hoc security assurance — external penetration tests, API security audits, and SOC 2 readiness reviews — with severity-ranked reports, evidence, and a re-test of criticals.
- `--needed-services`: penetration-testing; api-security; security-audit; soc2-readiness (specific scope per Buying Request)
- `--timeline`: per Buying Request (this category is often tied to a SOC 2 audit window)
- `--budget`: per Buying Request (example purchase: 1500)
- `--max-spend`: per Buying Request; default rule = up to 120% of expected budget (example purchase: 1800)
- `--payment-rules`: net-30 on accepted delivery; no deposits; any upfront payment needs Finance approval
- `--provider-preferences`: ISO 27001 + SOC 2 Type II required; OSCP/CREST-certified testers; min 3 years pentest delivery; reputation >= 4.2; prefer fintech experience, free re-test, and existing relationships
- `--blocked-providers`: unresolved data-handling incident in last 24 months; outside approved jurisdictions
- `--selection-rules`: competitive by default, 3 qualified providers; direct only when Daniela names a provider
- `--rfp-rules`: require scope coverage, tester certs, methodology, sample redacted report, timeline, re-test policy, price
- `--proposal-comparison-rules`: weighted rubric 60/40 quality/price; minimum acceptable score 70/100; disqualify on no sample report, narrowed scope, no re-test, or failed hard requirements
- `--negotiation-limits`: open 10–20% below expected budget; concede ~10% steps, max 3 rounds; never exceed max_spend; trade timeline/payment before price; no-ZOPA escalates
- `--contract-authority`: sign autonomously up to 5,000; above that, VP Finance approval
- `--acceptance-criteria`: severity-ranked report + exec summary + evidence + re-test of agreed criticals
- `--escalation-rules`: >5,000 spend, any upfront payment, no-ZOPA, protected/never-accept terms, no proposal >=70, hard requirement met by exception; Slack routing to VP Finance and Daniela
- `--dispute-posture`: rework-first via re-test obligation; formal dispute only on refusal or failed quality; Belong Judge on contested rejection
- `--rating-rules`: rate on report quality, finding accuracy, professionalism, re-test responsiveness; do not penalize many criticals
- `--optimization-goals`: quality 60 / price 40; tie-break to reputation then relationship; build a 2–3 provider trusted roster
- Human-To-Human Meetings: no dedicated buyer flag; meeting rules kept in playbook, scheduling escalations reflected through `--escalation-rules`
- `--activate`: done 2026-06-16
