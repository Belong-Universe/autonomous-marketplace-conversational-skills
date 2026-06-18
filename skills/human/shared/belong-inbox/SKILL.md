---
name: belong-inbox
description: "Human-facing day-to-day Belong Marketplace Inbox. Use for operational escalations: information requests, authorization requests, instruction/execution requests, fulfillment tasks, meeting requests, dispute requests, payment exceptions, Change Order approvals, notifications, human overrides, direct operational instructions, agent pause/resume, approval/rejection, cancellation, and Active Service intervention."
---

# Belong Inbox

Use this whenever a human asks what needs attention, what was escalated, or how to override an agent in day-to-day operations.

Inbox is not a durable training or Playbook-editing surface. Route durable behavior changes to `$belong-train-buying-agent` or `$belong-train-selling-agent`. Route temporary non-durable guidance to `$belong-steer-buying-agent` or `$belong-steer-selling-agent`.

## Start

Run:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py inbox --owner-role all --status pending
```

Filter by `buyer` or `seller` when the human role is clear.

Treat the inbox as the canonical next-work list. Before saying there is no pending work, identify and resolve stale, duplicate, superseded, or already-satisfied items with notes that point to the newer object, decision, contract version, payment event, or audit ID.

## Request Types

Handle all Marketplace Request types:

- Information
- Authorization
- Instruction/execution
- Fulfillment
- Meeting
- Dispute
- Payment exception
- Change Order approval
- Pause/resume
- Operational intervention

Notifications are mocked as channel messages that send the human back to the agentic application and this inbox.

## Notes On Specific Request Types

- Meeting: to set up a meeting on demand, use `override` "Request a meeting"; to answer
  one the other side proposed, use `resolve-inbox`. Meetings run on Calendly: accepting a
  meeting always shares the human's Calendly link, the proposing side then picks a slot
  that works on both its own human's calendar and the shared link, and the booking
  auto-creates the video join link. The agent stays within the playbook's scheduling
  authority and escalates here when it would exceed it (for example executive attendance
  or travel). A high-urgency meeting surfaces as a high-priority Inbox item for both
  humans.
- Review Deliverable Evidence Package (file reception): when the seller submits a
  deliverable, the buyer gets this item with the package files, links, and notes. Resolve
  it by checking the files and links against the SOW acceptance criteria, then accept,
  request a revision, or reject. Do not release final payment before the evidence meets
  acceptance.

## Resolve Or Override

Use `resolve-inbox` when the human provides information, approves/rejects authorization, executes an instruction, completes fulfillment, responds to a meeting, handles a dispute, approves a payment exception, signs or rejects a Change Order, pauses/resumes an agent, or intervenes in an Active Service.

Use `override` when the human wants to:

- Pause or resume an agent
- Give direct instructions
- Cancel negotiation
- Request a meeting
- Intervene in an Active Service

Paused agents stop new autonomous actions but preserve active obligations, urgent escalations, deadlines, payment notices, disputes, and required notices.

Enforce pause before every guided action. A paused agent cannot start new search engagement, proposal creation, negotiation, signature, Change Order, payment movement, optimization, or steering. Resume only after explicit human direction and a fresh pending-inbox check.

Do not approve or apply durable Playbook changes here. Durable changes to budget rules, pricing, authority, selection rules, escalation thresholds, contract terms, service scope, or policy behavior belong in the training skills. Direct operational instructions and one-off overrides are not durable Playbook changes.

For payment or authority approvals, include cumulative spend, existing holds/charges/releases/refunds/collections, seller-side platform fee, seller net, merchant-of-record context, and linked contract/SOW version.

## Output

Summarize what was resolved, rejected, cleaned up, or overridden, the linked object, authority/payment result, pause state, audit event path, remaining pending inbox items, and next skill. Remind the user which agent can continue autonomously and what will still escalate.
