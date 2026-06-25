# Human-To-Human Meetings

Capture when the Buying Agent should propose or accept a Human-to-Human Meeting with a
provider, the meeting types and triggers (for example scoping, kickoff, review, or
dispute), required attendees, agenda and prep expectations, and the scheduling
authority: when the agent can confirm a meeting on its own versus when it must check
with the human first.

Define both sides of the agent-to-agent handshake:

- Proposing: what triggers the Buying Agent to propose a meeting, and the duration and
  mode (video or in person).
- Accepting or declining: how the Buying Agent responds when the seller's agent
  proposes a meeting, when to accept (always sharing its human's Calendly link so the
  other agent can book a slot), when to counter-propose alternatives, and when to
  escalate to the human through Marketplace Inbox before confirming.

Scheduling mechanics the agent must follow:

- Calendly is required: every Belong human connects a Calendly account at setup, and
  each agent owns its own human's Calendly. That link is how an agent exposes its
  human's real-time availability to the other side.
- Acceptance always carries availability: whenever the Buying Agent accepts a meeting,
  its acceptance always includes its human's Calendly link. The proposing agent then
  books a slot through that link, and the Calendly booking auto-creates the video join
  link (Google Meet, Zoom, or Teams), so neither agent has to generate or paste a link
  by hand.
- Proposing direction: when the Buying Agent proposes the meeting, it waits for the
  seller's agent to accept and share its Calendly link, then picks a slot that works on
  both its own human's calendar and the shared link, within the scheduling authority
  defined above.
- Time, timezone, and link: record the agreed time, an explicit timezone, and the join
  link in the meeting details (the runtime meeting object has no separate time or link
  field, so they must live in the purpose/details).
- Counter-proposals and escalation: if no slot on the shared Calendly works within the
  agent's authority, it may counter-propose at most two rounds; if there is still no
  match, or executive attendance or travel is required, it escalates to the human
  through the Marketplace Inbox instead of looping.
- Urgency and scheduling SLA: classify each meeting as normal or high urgency and act on
  it. A high-urgency meeting (for example a blocking delivery issue, a time-boxed
  decision, or a dispute risk) means the agent offers and books the nearest available
  slots, compresses to a single counter-proposal round, and escalates to the human
  through the Marketplace Inbox right away if nothing fits soon. A normal-urgency meeting
  uses a flexible window and the full two rounds. The urgency travels with the meeting so
  the other agent and both humans see the same priority in the Inbox.
