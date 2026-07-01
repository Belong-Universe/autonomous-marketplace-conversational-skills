# Escalations

[Back to index](index.md)

Status: Done
Approval: Approved

## Playbook Rules

- Escalate to the Marketplace Inbox (do not act autonomously) when any of these is true:
  - Contract value would exceed 5,000 (VP Finance approval).
  - Any upfront / pre-delivery payment or deposit is requested (Finance approval).
  - A no-ZOPA situation: the seller's floor exceeds the Buying Request `max_spend` (see [05 Negotiations](05-negotiations.md)).
  - A required protection or never-accept term is at stake (see [06 Legal And Contracts](06-legal-and-contracts.md)).
  - No qualified provider scores at or above the 70 minimum.
  - A hard provider requirement is met only by exception.
- Routing and owners:
  - Spend/authority approvals → VP Finance (Slack: #pagora-finance-approvals).
  - Security/legal exceptions → Daniela (Head of Security & Compliance).
  - Scheduling beyond authority → Daniela.
- Notification channel: Slack. Normal escalations within business hours; high-urgency escalations ping immediately.
- Agent pause/resume: Daniela or VP Finance may pause the agent at any time through `override`; the agent must not run autonomous create/negotiate/sign/payment actions while paused.
- Every escalation carries a Decision Explanation built from audit evidence, not raw model reasoning.

## Worked Example (this purchase)

- The no-ZOPA situation triggered an escalation to Daniela (security owner) and VP Finance (ceiling change). Daniela approved raising the ceiling to 2,000 in the Inbox.

## Still Missing

- `-`

## Source Notes

- Pagora Delegation-of-Authority matrix and Procurement Policy v3.
- Daniela confirmed Slack routing and the named owners.
