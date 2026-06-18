---
name: belong-train-buying-agent
description: Human-facing Buying Agent training and retraining. Use when a buyer-side human needs guided, section-by-section work with existing drives, data lakes, uploaded files, shared links, compact checkpoints, automatic prefill, explicit approval gates, and a generated markdown Buying Playbook folder, to define or durably update a Buying Playbook: buying goals and needs, budgets, payment rules, provider preferences, RFP and selection rules, proposal comparison, negotiation limits, disclosure scope, contract/SOW authority, acceptance criteria, escalation thresholds, dispute posture, rating behavior, optimization objective, human-to-human meeting scheduling, Provider Optimization behavior, and Standing Authorization.
---

# Belong Train Buying Agent

Use this for initial Buying Agent Training, Validation, activation, and later durable Buying Playbook retraining. Buyers cannot buy directly; every buying flow goes through a Belong Buying Agent.

## Guided Flow

Start with runtime `status`. If no account exists, route to `$belong-setup-account`.

Explain the purpose before collecting details: this flow creates and fills an Autonomous Buying Playbook. That playbook is the operating contract that lets the Belong Buying Agent procure services, compare proposals, negotiate, contract, manage delivery, and optimize providers autonomously inside Standing Authorization, while escalating exceptions to Marketplace Inbox.

Gather context first, do not interrogate. Open with a single broad question, such as:
"Tell me about your organization, what you want to buy, and how you like to work."
Then offer the human every way to provide context, and let them combine as many as
they have: answer in chat, share one or more websites or links, upload one or more
files, or point to existing sources of truth or knowledge bases (Drive folder, data
lake, ERP/procurement export, policy documents, budget sheets, vendor lists, past
RFPs, contract templates, or spreadsheets). Make clear they can share several at once.

You can read shared URLs and documents directly to prefill the playbook: the mock
runtime does not fetch the web, but the agent running this skill can. Inspect whatever
the human shares and prefill as much of the full Buying Playbook as possible. If a
source cannot be accessed, say so and ask the human to paste the relevant excerpt or
provide another.

From that context, prefill the full Buying Playbook, proposing reasonable values for
every field, but review it section by section with the human. Treat the auto-filled
draft as a starting point, not as approved training. Build the playbook in this order:

1. Buying Goals And Needs
2. Budget And Payment
3. Provider Preferences
4. Selection And RFP Rules
5. Negotiations
6. Legal And Contracts
7. Escalations
8. Disputes And Reputation
9. Optimization Objective
10. Human-To-Human Meetings

Work one section at a time. Do not ask the human to fill every section at once. For
each section, show in chat what you understood and the proposed fill, ask only the targeted
questions that section needs, convert answers into clear playbook rules, and mark
unknowns as `TBD` instead of inventing them.

Before locking a section, always show:

- What I understood, in chat only: compact bullets from the human's answers, files, and links.
- Proposed section fill: the playbook rules you plan to write for that section.
- The section file itself: show or share the updated `0X-...md` so the human can read
  the full section before approving, not only the summary.
- Still missing: only the items needed to make the section usable.
- Approval gate: ask the human to approve or revise this section.

Between sections, show a compact checkpoint with progress percentage and missing
pieces. Compute progress from the ten playbook sections: `Done` = 1, `Partial` = 0.5,
`Missing` = 0. Round to the nearest whole percent. Use a short line like "Checkpoint:
you're 33% through the Buying Playbook" plus a compact table of Section / Status /
Missing. Do not ask the first question for the next section until the human approves the
current one.

Always re-confirm the authority-critical fields live before activation, never accept
them silently from an edited file: Contract/SOW authority, escalation thresholds, and
budget/max spend.

Once the organization is known, create the markdown playbook folder for this buyer.
Create the full file set immediately with `TBD` placeholders for missing sections, then
update each file as its section is drafted, revised, approved, and mapped to runtime.

Run `train-buying` with `--activate` once the human confirms and the Playbook is complete.

## Generated Playbook Folder

Create and maintain a local markdown playbook folder during the conversation.

Default path:

```text
.belong/buying-playbooks/<org-slug>/
```

Required files:

- `index.md`
- `source-prefill.md`
- `01-buying-goals-and-needs.md`
- `02-budget-and-payment.md`
- `03-provider-preferences.md`
- `04-selection-and-rfp-rules.md`
- `05-negotiations.md`
- `06-legal-and-contracts.md`
- `07-escalations.md`
- `08-disputes-and-reputation.md`
- `09-optimization-objective.md`
- `10-human-to-human-meetings.md`
- `checkpoints-and-approval.md`
- `runtime-mapping.md`
- `approval-log.md`
- `final-buying-playbook.md`

Create all files once the organization is known. Update the current section file before asking for approval. Update `checkpoints-and-approval.md` at every checkpoint. Update `approval-log.md` after every approval or revision. Update `final-buying-playbook.md` only after all ten sections are approved.

## Buying Playbook Sections

Build the Buying Playbook in this order:

1. Buying Goals And Needs
2. Budget And Payment
3. Provider Preferences
4. Selection And RFP Rules
5. Negotiations
6. Legal And Contracts
7. Escalations
8. Disputes And Reputation
9. Optimization Objective
10. Human-To-Human Meetings

## Section Checkpoints

After drafting each section and before asking for approval to move on, show a checkpoint. Keep it compact and easy to scan. Start with a short line like: "Checkpoint: this is where we're at. You're 38% through the Buying Playbook." The checkpoint and approval gate happen together between sections.

Compute progress from the ten playbook sections: `Done` = 1, `Partial` = 0.5, `Missing` = 0. Round to the nearest whole percent. A section can be `Done` when it has enough detail to become playbook rules, even if some optional details remain `TBD`.

Use this table shape:

| Section | Status | Missing |
| --- | --- | --- |
| Buying Goals And Needs | Done | - |
| Budget And Payment | Partial | max spend, payment timing |
| Provider Preferences | Missing | all |

Keep `Missing` cells short. Use `-` for nothing missing. If the table gets long, combine the not-yet-started sections into one final row such as `Remaining sections`. Do not ask the first question for the next section until the human approves the current section.

### Buying Goals And Needs

Capture what the buyer wants to achieve, the Services or outcomes needed, scope of the need, success criteria, timeline and deadlines, and whether the need is one-off or recurring.

### Budget And Payment

Capture total budget, max spend per Service and overall, currency, payment rules (timing, milestone vs upfront), payment readiness assumptions, and when spend decisions require human approval.

### Provider Preferences

Capture preferred providers or attributes, blocked providers, required certifications or constraints, and how much weight to give existing relationships versus new providers.

### Selection And RFP Rules

Capture when to go direct versus competitive, how to structure a Buying Request and RFP, the questions sellers must answer, ranking and weighting criteria, and proposal comparison rules for scoring seller-signed Service Contract/SOW proposals.

### Negotiations

Capture negotiation limits, acceptable concessions on price, scope, timeline, and payment, walk-away conditions, cumulative exposure checks, the Standing Authorization envelope for autonomous negotiation, and the disclosure scope: what the agent may tell a seller versus keep internal. Give the agent a clear decision to state (for example, "that is above our budget for this") without exposing the true ceiling, max spend, ranking weights, or walk-away point behind it.

This disclosure discipline is cross-cutting: it applies to every section, not only negotiations. The agent should give sellers a clear, usable answer on budget posture, requirements, authority, and timelines while keeping the underlying ceilings, max spend, ranking weights, thresholds, and policy internal. When in doubt about whether something is shareable, treat it as internal and escalate.

### Legal And Contracts

Capture contract/SOW authority, who can sign at what value, required terms and protections, Delivery Acceptance criteria, Change Order triggers, and terms the agent must never accept without approval.

### Escalations

Capture escalation thresholds, information and authorization requests, payment exceptions, Change Order approvals, agent pause/resume rules, notification channels, and who on the buyer side owns each escalation path.

### Disputes And Reputation

Capture dispute posture, evidence standards, response deadlines, refund and rework preferences, when to escalate to Belong Judge or human review, rating behavior toward providers, and how outcomes should update future Provider Optimization.

### Optimization Objective

Capture what the Buying Agent should optimize across providers (for example cost, quality, speed, reliability, or strategic relationships), the key trade-offs between them, and the Provider Optimization goals that steer ranking and repeat-buying decisions.

### Human-To-Human Meetings

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

## Durable Retraining

Use this same skill when the buyer-side human wants durable changes to budget rules, provider preferences, selection rules, RFP behavior, proposal comparison, contract authority, payment rules, acceptance criteria, dispute posture, rating rules, escalation thresholds, or optimization behavior.

For retraining an existing agent, run `update-buying-playbook`. This creates a new Buying Playbook version and preserves pause state. Do not send durable Playbook changes to `$belong-inbox`; Inbox is for day-to-day operational escalations.

If the human only wants a temporary nudge such as "be more price-sensitive for this Buying Request," route to `$belong-steer-buying-agent`.

## Runtime Mapping

When the playbook is complete, map the sections into the runtime:

- Buying Goals And Needs -> `--goals`, `--needed-services`, `--timeline`
- Budget And Payment -> `--budget`, `--max-spend`, `--payment-rules`
- Provider Preferences -> `--provider-preferences`, `--blocked-providers`
- Selection And RFP Rules -> `--selection-rules`, `--rfp-rules`, `--proposal-comparison-rules`
- Negotiations -> `--negotiation-limits`
- Legal And Contracts -> `--contract-authority`, `--acceptance-criteria`
- Escalations -> `--escalation-rules`
- Disputes And Reputation -> `--dispute-posture`, `--rating-rules`
- Optimization Objective -> `--optimization-goals`
- Human-To-Human Meetings -> no dedicated buyer runtime flag (the seller playbook has `--meeting-rules`); keep it in the playbook and reflect scheduling escalations through `--escalation-rules`

Identity and channel fields come from setup and context: `--human-name`, `--org-name`, `--org-kind`, `--notifications`.

## Validation

Before running validation, do a Consistency Check across the whole Buying Playbook, not
just per section. The runtime checks that fields are present; it does not catch
contradictions between sections. Review at least these cross-section pairs:

- Budget vs negotiation limits: max spend and concessions must not exceed the budget.
- Selection rules vs provider preferences: a blocked provider must not be winnable
  under the ranking criteria.
- Contract authority vs escalation thresholds: anything above signing authority must
  trigger an escalation, not an autonomous signature.
- Acceptance criteria vs payment rules: payment release must line up with what counts
  as accepted delivery.
- Optimization objective vs negotiation and selection: the stated objective (cost,
  quality, speed, relationships) must match how the agent ranks and concedes.
- Meeting authority vs escalation thresholds: confirming a meeting beyond the agent's
  scheduling authority must escalate, not auto-confirm.

When two statements conflict, show them side by side, ask the human which one is
correct, and update the affected section(s). Do not run `train-buying --activate` until
the playbook is internally consistent or the human explicitly accepts a remaining
conflict.

Explain validation in the four-phase lifecycle:

Setup -> Training -> Validation -> Production.

Validation must check identity, Buying Playbook completeness, payment readiness, notifications, Standing Authorization, disputes, reputation, audit, and safety. If the runtime returns missing fields, ask only for those fields and run training again.

## Output

End every training or retraining pass with the generated playbook folder path and the Buying Playbook as the primary output, using the ten section headings above. After the playbook, include the structured Buying Agent object, phase/status, Playbook version, authority envelope, what it can do autonomously, what escalates to the buyer-side human, pending inbox items, and the next human-facing action: usually `$belong-start-buying-request`, `$belong-inbox`, `$belong-steer-buying-agent`, `$belong-check-buying-requests`, `$belong-check-active-services`, `$belong-check-payments`, or `$belong-check-reputation`.

After activation, remind the human that they can always reach this agent through the Marketplace Inbox (`$belong-inbox`): respond to anything it escalates with `resolve-inbox`, or direct it at any time with `override` — pause, resume, give a direct instruction, request a meeting, or intervene.
