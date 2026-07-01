# Pagora Buying Playbook

Organization: Pagora
Human owner: Daniela
Organization kind: company
Notification channels: Slack
Runtime account: acct_0002
Runtime organization: org_0002
Current phase: Production
Progress: 100%

This is a complete, activated example of a buyer-side Buying Playbook. It is the durable counterpart to the seller-side `example-generated-folder` (which shows a playbook mid-training). Use it to see what a finished buyer playbook looks like end to end, and how the two layers stay separate: the playbook holds durable rules, while the per-purchase numbers (need, budget, ceiling, deadline) arrive on each Buying Request.

The running story is a real purchase Pagora ran through this playbook: an external penetration test and API security audit, expected budget 1,500, ceiling 1,800. It is used throughout to show how the rules behave, and it ends in a no-ZOPA escalation when the chosen seller's floor lands at 2,000.

## Files

- [Source Prefill](source-prefill.md)
- [01 Buying Goals And Needs](01-buying-goals-and-needs.md)
- [02 Budget And Payment](02-budget-and-payment.md)
- [03 Provider Preferences](03-provider-preferences.md)
- [04 Selection And RFP Rules](04-selection-and-rfp-rules.md)
- [05 Negotiations](05-negotiations.md)
- [06 Legal And Contracts](06-legal-and-contracts.md)
- [07 Escalations](07-escalations.md)
- [08 Disputes And Reputation](08-disputes-and-reputation.md)
- [09 Optimization Objective](09-optimization-objective.md)
- [10 Human-To-Human Meetings](10-human-to-human-meetings.md)
- [Checkpoints And Approval](checkpoints-and-approval.md)
- [Runtime Mapping](runtime-mapping.md)
- [Approval Log](approval-log.md)
- [Final Buying Playbook](final-buying-playbook.md)

## Current State

- Mock Belong OAuth/account setup is complete for Daniela at Pagora.
- Payment (Stripe) and legal/signing readiness are mocked as ready by the runtime.
- Buying Agent training is activated; the agent is in Production.
- All ten sections are approved and mapped to the runtime.
- One Buying Request has run end to end on this playbook (the pentest/security audit), which produced the no-ZOPA escalation documented in [05 Negotiations](05-negotiations.md).
