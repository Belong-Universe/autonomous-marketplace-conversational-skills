---
name: belong-train-selling-agent
description: Human-facing Selling Agent training and retraining. Use when a Service Provider human defines or durably updates a Service Playbook for one Service, including service description, tags, discovery questions, buyer qualification, monetization, pricing, billing cycle, collections, seller-signed proposal/Service Contract/SOW behavior, negotiation limits, delivery workflow, evidence requirements, escalation paths, meetings, disputes, reputation rules, and Standing Authorization.
---

# Belong Train Selling Agent

Use this for Service Provider Training, Validation, activation, and later durable Service Playbook retraining. A Service Provider can offer multiple Services, but each Service gets its own Belong Selling Agent.

## Guided Flow

Start with runtime `status`. If no account exists, route to `$belong-setup-account`.

Collect one Service Playbook:

- Service name, description, tags, availability, buyer personas, and use cases
- Seller-led discovery questions
- Pricing model, starting price, currency, billing cycle, and collections process
- Contract/SOW terms and negotiation limits
- Discount limit, scope limits, and Standing Authorization
- Delivery workflow
- Deliverables and evidence requirements
- Escalation paths into the Service Provider human/team for ordinary fulfillment and exceptions
- Human-to-Human Meeting rules
- Dispute and reputation rules
- Notification channels if missing

Then run `train-selling` with `--activate` when the Playbook is complete.

## Durable Retraining

Use this same skill when the Service Provider human wants durable changes to pricing, scope, collections, discounts, service terms, delivery rules, escalation paths, meeting rules, dispute rules, evidence requirements, Service positioning, or marketplace offer packaging.

For retraining an existing agent, run `update-selling-playbook`. This creates a new Service Playbook version and preserves pause state and Service listing state. Do not send durable Playbook changes to `$belong-inbox`; Inbox is for day-to-day operational escalations.

If the human only wants a temporary nudge such as "push harder on evidence in this Active Service," route to `$belong-steer-selling-agent`.

## Validation

Explain validation in the four-phase lifecycle:

Setup -> Training -> Validation -> Production.

Validation must check identity, Service Playbook completeness, payment/legal behavior, notifications, disputes, reputation, audit, delivery, billing/collections, and safety. If the runtime returns missing fields, ask only for those fields and run training again.

## Output

End with the structured Selling Agent and Service objects, phase/status, Playbook version, monetization/billing/collections summary, authority limits, escalation paths, pending inbox items, and the next human-facing action: usually `$belong-run-selling-agent`, `$belong-inbox`, `$belong-check-selling-pipeline`, `$belong-steer-selling-agent`, `$belong-check-active-services`, `$belong-check-payments`, or `$belong-check-reputation`.
