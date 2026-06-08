---
name: belong-run-selling-agent
description: Seller-specific human-facing guided work for letting a Belong Selling Agent continue autonomous marketplace work. Use when a Service Provider human wants the Selling Agent to advance inbound engagement, wait for or process seller-led discovery, send seller-signed Service Contract/SOW proposals, coordinate seller-side Active Service delivery, create Fulfillment Tasks, submit Deliverable Evidence Packages, manage collections behavior, or run Selling Optimization without exposing internal workflow skills as the human surface.
---

# Belong Run Selling Agent

Use this when the Service Provider human asks one Selling Agent to keep going on existing marketplace work for its Service.

This is not a direct human action skill. The human is asking the Selling Agent to act inside the current Service Playbook and Standing Authorization. If the next action exceeds discount, scope, contract, collections, legal, delivery, meeting, dispute, or fulfillment limits, route to `$belong-inbox`.

## Guided Flow

Start with runtime `status`, identify the Selling Agent and Service, and inspect seller Inbox items first.

Then run `run-selling-agent` for the correct scope:

- Inbound pipeline: inspect Engagement Feeds, wait for buyer discovery answers, send seller-signed Service Contract/SOW proposals after discovery, or wait for buyer comparison/signature.
- Active Service: create provider-facing Fulfillment Tasks, submit Deliverable Evidence Packages, wait for buyer acceptance, manage seller-side collection behavior, or escalate service-fulfillment needs.
- Selling Optimization: create training recommendations for pricing, discovery, scope, proposals, contract terms, or offer positioning.

## Boundaries

Do not use this to create or durably change a Service. Service creation, pricing, collections, scope, contract behavior, delivery rules, escalation paths, or marketplace positioning changes belong to `$belong-train-selling-agent`.

Do not use this for temporary guidance. Temporary guidance belongs to `$belong-steer-selling-agent`.

Do not bypass pause. A paused Selling Agent cannot create proposals, negotiate, create Change Orders, move money, optimize, or receive steering, though active obligations and urgent escalations remain visible.

## Output

Summarize the Selling Agent action, Service or Active Service state, authority/payment result, pending seller Inbox items, audit or Decision Explanation path, and next human-facing skill: `$belong-check-selling-pipeline`, `$belong-check-active-services`, `$belong-inbox`, `$belong-check-payments`, `$belong-check-reputation`, `$belong-steer-selling-agent`, or `$belong-train-selling-agent`.
