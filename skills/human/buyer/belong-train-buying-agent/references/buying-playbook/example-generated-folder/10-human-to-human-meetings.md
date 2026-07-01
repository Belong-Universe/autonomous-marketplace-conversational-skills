# Human-To-Human Meetings

[Back to index](index.md)

Status: Done
Approval: Approved

## Playbook Rules

- Pre-contract, the common meeting is a scoping call before signing a pentest, to confirm assets, rules of engagement, and timing.
- Triggers: propose a scoping call when scope is ambiguous or assets are sensitive; accept a seller-proposed scoping call when the proposal scored at or above the 70 minimum.
- Required attendees: Daniela for any security scoping or rules-of-engagement call. Engineering lead optional for API scope.
- Scheduling preferences: Tuesday–Thursday, 9:00–12:00 America/Bogota. Avoid Mondays and Fridays.
- Scheduling authority: the agent may confirm a scoping call on its own inside the preferred window. Outside the window, or if executive attendance/travel is needed, it escalates to Daniela first.
- Handshake: when accepting, the agent always shares Daniela's Calendly link so the seller's agent can book; the booking auto-creates the video link. When proposing, it waits for the seller's agent to share its Calendly, then books a slot that fits both within the preferred window.
- Counter-proposals: at most two rounds. If no slot fits, escalate to Daniela through the Inbox instead of looping.
- Urgency: a scoping call blocking a deadline-bound purchase (SOC 2 window) is high urgency — offer the nearest slots, compress to one counter-proposal round, and escalate fast if nothing fits.
- Record the agreed time, an explicit timezone, and the join link in the meeting details (the runtime meeting object has no separate time/link field).

## Worked Example (this purchase)

- A 30-minute scoping call was booked Wed 10:00 America/Bogota via Daniela's Calendly to confirm rules of engagement before signing. It fit the preferred window, so the agent confirmed it without escalating.

## Still Missing

- `-`

## Source Notes

- Daniela's working-hours and calendar norms.
- There is no dedicated buyer meeting runtime flag; rules live in the playbook and scheduling escalations reflect through `--escalation-rules`.
