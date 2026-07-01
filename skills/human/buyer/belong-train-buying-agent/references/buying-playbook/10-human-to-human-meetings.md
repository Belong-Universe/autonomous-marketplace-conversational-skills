# Human-To-Human Meetings

[Back to index](index.md) | Previous: [Optimization Objective](09-optimization-objective.md) | Next: [Checkpoints And Approval](checkpoints-and-approval.md)

This section defines when the Buying Agent proposes or accepts a Human-to-Human Meeting with a provider, the buyer's scheduling preferences, and the scheduling authority. Pre-contract, the common type is a scoping call before committing.

## Source Signals

Look for calendars, meeting norms, working-hours policy, timezone, and notes on which decisions require a live conversation.

## Required Fields

- Meeting triggers and types (scoping, kickoff, review, dispute) and which apply pre-contract
- Required attendees per meeting type
- Buyer scheduling preferences: preferred days, time windows, and explicit timezone
- Duration and mode (video or in person)
- Agenda and prep expectations
- Scheduling authority: when the agent confirms on its own versus checks with the human first

### Agent-to-agent handshake

- Proposing: what triggers the Buying Agent to propose a meeting, and the duration and mode.
- Accepting or declining: when to accept (always sharing its human's Calendly link so the other agent can book), when to counter-propose, and when to escalate to the human through the Inbox before confirming.

### Scheduling mechanics

- Calendly is required: every Belong human connects a Calendly account at setup, and each agent owns its own human's Calendly. That link is how an agent exposes real-time availability.
- Acceptance always carries availability: whenever the Buying Agent accepts, it includes its human's Calendly link. The proposing agent books through it, and the booking auto-creates the video join link.
- Proposing direction: when the Buying Agent proposes, it waits for the seller's agent to accept and share its Calendly link, then picks a slot that works on both calendars within authority.
- Time, timezone, and link: record the agreed time, an explicit timezone, and the join link in the meeting details (the runtime meeting object has no separate time/link field).
- Counter-proposals and escalation: at most two rounds; if no match, or executive attendance or travel is required, escalate to the human through the Inbox instead of looping.
- Urgency and SLA: classify each meeting as normal or high urgency. High urgency compresses to a single counter-proposal round and escalates fast; normal urgency uses the full two rounds. Urgency travels with the meeting so both sides see the same priority.

## Quality Bar

The section is `Done` when the Buying Agent can propose, accept, schedule within the buyer's preferred windows, and escalate the right meetings without looping.

## Guardrails

- Do not confirm a meeting beyond the agent's scheduling authority; escalate instead (see consistency check vs [Escalations](07-escalations.md)).
- Do not loop past two counter-proposal rounds.
- There is no dedicated buyer meeting runtime flag; keep meeting rules in the playbook and reflect scheduling escalations through `--escalation-rules`.
