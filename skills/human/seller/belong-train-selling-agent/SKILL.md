---
name: belong-train-selling-agent
description: Human-facing Selling Agent training and retraining. Use when a Service Provider human needs guided, section-by-section work with existing drives, data lakes, uploaded files, shared links, compact checkpoints, automatic prefill, explicit approval gates, and a generated markdown Selling Playbook folder for one Service, including value proposition, monetization models, legal/contracts, negotiation rules, active-service delivery work, escalations, human-to-human meetings, disputes, reputation rules, delivery capacity, optimization objective, and Standing Authorization.
---

# Belong Train Selling Agent

Use this for Service Provider Training, Validation, activation, and later durable Selling Playbook retraining. The output of this skill is the Selling Playbook for one Service. A Service Provider can offer multiple Services, but each Service gets its own Belong Selling Agent and its own Selling Playbook.

## Guided Flow

Start with runtime `status`. If no account exists, route to `$belong-setup-account`.

Gather context first, do not interrogate. Open with a single broad question, such as:
"Tell me about the Service you want to sell, who it is for, and how you like to deliver
and price it." Then offer the human every way to provide context, and let them combine
as many as they have: answer in chat, share one or more websites or links, upload one or
more files, or point to existing sources of truth or knowledge bases (Drive folder, data
lake, CRM/export, product docs, sales deck, proposal archive, legal templates, delivery
SOPs, support/dispute history, or spreadsheet). Make clear they can share several at
once, not just one.

You can read shared URLs and documents directly to prefill the playbook: the mock
runtime does not fetch the web, but the agent running this skill can. Inspect whatever
the human shares and prefill as much of the full Selling Playbook as possible. If a
source cannot be accessed, say so and ask the human to paste the relevant excerpt or
provide another.

Decide the offering structure before drafting. Ask whether this is one integral Service
or several offerings that can be purchased separately. Separately purchasable offerings
each become their own Service, with their own Service Playbook and Selling Agent. Keep
variants of a single offering (tiers, scope options, price levels) inside one Service
Playbook. A Selling Agent cannot bundle multiple Services into one combined offer;
buyers combine Services on the demand side.

Once the company/organization and Service name are known, create a markdown playbook folder for this Service. Use `.belong/selling-playbooks/<company-slug>/<service-slug>/` unless the human asks for another destination. Create the full file set immediately with `TBD` placeholders for missing sections, then update files as sections are drafted, revised, approved, and mapped to runtime.

Even when sources fill the playbook well, still review section by section with the human. Treat the auto-filled draft as a starting point, not as approved training. Do not activate training or move across sections without the approval gates below.

Work section by section. Do not ask the human to fill every section at once. For each section:

- Name the section being drafted.
- Invite the human to answer directly, upload files, or share links that may help fill that section.
- Review relevant uploaded files and shared links before asking for information already present in those sources.
- Show what you understood from the shared material and how you plan to fill the section.
- Ask only the targeted questions needed for that section.
- Convert the human's answers into clear playbook rules.
- Mark unknowns as `TBD` instead of inventing them.
- Between sections, show a compact checkpoint with progress percentage and missing playbook pieces.
- Do not continue to the next section or phase until the human approves the current section.

## Source Intake And Approval Gates

### Initial Source Discovery

Open by inviting context in any form before collecting section answers. Example: "Tell me about this Service, and share any links, files, Drive folders, data lakes, docs, sites, sales materials, proposal archives, legal templates, or SOPs — as many as you have, all at once. I can read what you share to prefill this Selling Playbook."

If sources are provided:

- Confirm what you can access and what you cannot access.
- Review the sources before asking section questions.
- Build an initial prefill map across all nine Selling Playbook sections.
- Show a compact source summary: source name, sections informed, confidence, and gaps.
- Ask the human whether to start reviewing the prefilled draft section by section.

Use this compact source summary shape:

| Source | Sections informed | Confidence | Gaps |
| --- | --- | --- | --- |
| Sales deck | Value Proposition, Monetization Models | High | collections |
| MSA template | Legal And Contracts, Disputes And Reputation Rules | Medium | approval limits |

If a source appears useful for later sections, keep the extracted facts in the prefill map. Still present and approve only the current section when working through the guided flow.

### Per-Section Source Intake

At the start of each section, tell the human they can provide files, links, or plain answers. Use shared material to prefill as much of the current section as possible. If a file or link also contains useful information for later sections, remember the extracted points but do not advance early.

For every uploaded file or shared link:

- Inspect the source before asking follow-up questions.
- Extract only facts and rules relevant to the current section.
- Separate source-backed details from assumptions or `TBD` items.
- If a link or file cannot be accessed, say so and ask the human to paste the relevant excerpt or provide another source.

Before locking a section, always show:

- What I understood: compact bullets from the user's answers, files, and links.
- Proposed section fill: the playbook rules you plan to write for that section.
- The section file itself: show or share the updated `0X-...md` so the human can read the full section before approving, not only the summary.
- Still missing: only the items needed to make the section usable.
- Approval gate: ask the human to approve or revise this section.

Use this approval prompt shape: "Approve this section so we can continue to `<next section>`, or tell me what to change." Treat "yes", "approved", "continue", or equivalent confirmation as approval. If the human revises the section, update it and ask for approval again.

## Reference Playbook

When the user asks for the playbook structure, wants examples, or the section draft needs a quality bar, read `references/selling-playbook/index.md`, then load only the relevant linked page. The reference is wiki-style and covers source prefill, all nine seller playbook sections, generated playbook folders, checkpoints, approval gates, consistency checks, and exactly one good and one bad example.

## Generated Playbook Folder

Create and maintain a local markdown playbook folder during the conversation. Follow `references/selling-playbook/generated-playbook-folder.md`.

Default path:

```text
.belong/selling-playbooks/<company-slug>/<service-slug>/
```

Required files:

- `index.md`
- `source-prefill.md`
- `01-value-proposition.md`
- `02-monetization-models.md`
- `03-legal-and-contracts.md`
- `04-negotiations.md`
- `05-active-service-work.md`
- `06-human-to-human-meetings.md`
- `07-escalations.md`
- `08-disputes-and-reputation.md`
- `09-capacity-and-objective.md`
- `checkpoints-and-approval.md`
- `runtime-mapping.md`
- `approval-log.md`
- `final-selling-playbook.md`

Create all files once company and Service are known. Update the current section file before asking for approval. Update `checkpoints-and-approval.md` at every checkpoint. Update `approval-log.md` after every approval or revision. Update `final-selling-playbook.md` only after all nine sections are approved.

## Selling Playbook Sections

Build the Selling Playbook in this order:

1. Value Proposition
2. Monetization Models
3. Legal And Contracts
4. Negotiations
5. Way Of Work During An Active Service
6. Human-To-Human Meetings
7. Escalations
8. Disputes And Reputation Rules
9. Capacity And Objective

## Section Checkpoints

After drafting each section and before asking for approval to move on, show a checkpoint. Keep it compact and easy to scan. Start with a short line like: "Checkpoint: this is where we're at. You're 38% through the Selling Playbook." The checkpoint and approval gate happen together between sections.

Compute progress from the nine playbook sections: `Done` = 1, `Partial` = 0.5, `Missing` = 0. Round to the nearest whole percent. A section can be `Done` when it has enough detail to become playbook rules, even if some optional details remain `TBD`.

Use this table shape:

| Section | Status | Missing |
| --- | --- | --- |
| Value Proposition | Done | - |
| Monetization Models | Partial | collections, refund rules |
| Legal And Contracts | Missing | all |

Keep `Missing` cells short. Use `-` for nothing missing. If the table gets long, combine the not-yet-started sections into one final row such as `Remaining sections`. Do not ask the first question for the next section until the human approves the current section.

### Value Proposition

Capture what the Service is, who it is for, the buyer pain or outcome, proof points, availability, Service Tags, buyer personas, use cases, and seller-led discovery questions that qualify fit.

### Monetization Models

Capture pricing model, starting price, currency, billing cycle, collections process, seller-side platform fee awareness, payment readiness assumptions, refund/hold expectations, and when billing exceptions require human approval.

### Legal And Contracts

Capture standard Service Contract/SOW terms, deliverables, evidence requirements, acceptance criteria, contract authority, scope boundaries, required signatures, Change Order triggers, legal exceptions, and terms the agent must never change without approval.

### Negotiations

Capture discount limit, scope limits, price/timeline/payment concessions, contract fallback positions, buyer qualification rules, walk-away conditions, cumulative exposure checks, the Standing Authorization envelope for autonomous negotiation, and the disclosure scope: what the agent may tell a buyer versus keep internal. Give the agent a clear decision to state (for example, "no discount available" when the buyer is not eligible) without exposing the discount limit, margins, authority thresholds, capacity, or internal policy behind it.

This disclosure discipline is cross-cutting: it applies to every section, not only negotiations. The agent should give buyers a clear, usable answer on pricing, capacity, authority, timelines, and other clients while keeping the underlying limits, costs, thresholds, and policy internal. When in doubt about whether something is shareable, treat it as internal and escalate.

### Way Of Work During An Active Service

Capture the delivery workflow after buyer signature: kickoff, milestones, Fulfillment Tasks, owner responsibilities, deliverable evidence packages, acceptance/revision flow, payment ledger expectations, audit trail, and how the Selling Agent coordinates ordinary provider work.

### Human-To-Human Meetings

Capture when meetings should be proposed, required attendees, agenda/prep expectations, follow-up notes, decision capture, meeting-related escalations, and when the Selling Agent can schedule autonomously.

### Escalations

Capture ordinary fulfillment escalations, exception thresholds, information requests, authorization requests, payment exceptions, Change Order approvals, agent pause/resume rules, notification channels, and who in the Service Provider organization owns each escalation path.

### Disputes And Reputation Rules

Capture dispute posture, evidence standards, response deadlines, refund/rework preferences, when to escalate to Belong Judge or human review, rating behavior, reputation signals, and how outcomes should update future Selling Optimization recommendations.

### Capacity And Objective

Capture the two strategic inputs that frame every other section:

- Delivery capacity: how many Active Services the provider can run at once, typical lead time, and what the agent does when demand exceeds capacity (pause or de-prioritize the listing, extend quoted timelines, or escalate to the human). This keeps the Selling Agent from winning more work than the team can deliver.
- Optimization objective: what the agent should maximize (for example win rate, margin, utilization, or strategic accounts) and the key trade-offs between them, so pricing, negotiation, and acceptance decisions have a clear target.

Surface both during the opening context gathering so they inform the earlier sections, then confirm them here.

Then run `train-selling` with `--activate` when the Playbook is complete and the generated folder contains the approved final playbook.

If the human chose to split the offering into several separately purchasable Services,
repeat this whole flow once per Service, producing one Selling Agent and one generated
playbook folder per Service. Reuse shared context (organization, provider style,
notifications, legal templates) across Services so the human is not asked the same thing
twice; only re-gather the fields specific to each Service.

## Durable Retraining

Use this same skill when the Service Provider human wants durable changes to any Selling Playbook section: value proposition, monetization, legal/contracts, negotiations, active-service work, meetings, escalations, disputes, reputation rules, evidence requirements, Service positioning, or marketplace offer packaging.

For retraining an existing agent, first show the current section being changed and the proposed replacement text. Then run `update-selling-playbook`. This creates a new Selling Playbook version and preserves pause state and Service listing state. Do not send durable Playbook changes to `$belong-inbox`; Inbox is for day-to-day operational escalations.

If the human only wants a temporary nudge such as "push harder on evidence in this Active Service," route to `$belong-steer-selling-agent`.

## Runtime Mapping

When the playbook is complete, map the sections into the runtime:

- Value Proposition -> `--service-name`, `--description`, `--tags`, `--availability`, `--buyer-personas`, `--use-cases`, `--discovery-questions`
- Monetization Models -> `--pricing-model`, `--starting-price`, `--currency`, `--billing-cycle`, `--collections`
- Legal And Contracts -> `--contract-terms`, `--deliverables`, `--evidence-requirements`
- Negotiations -> `--discount-limit`, `--scope-limits`, `--negotiation-limits`
- Way Of Work During An Active Service -> `--delivery-workflow`, plus relevant deliverables and evidence requirements
- Human-To-Human Meetings -> `--meeting-rules`
- Escalations -> `--escalation-paths`
- Disputes And Reputation Rules -> `--dispute-rules`, `--reputation-rules`
- Capacity And Objective -> delivery capacity maps onto `--availability` and at-capacity behavior onto `--escalation-paths`; the optimization objective has no dedicated seller runtime flag (the buyer playbook has `--optimization-goals`), so keep it in the playbook and reflect it through `--negotiation-limits` and `--reputation-rules`

## Validation

Explain validation in the four-phase lifecycle:

Setup -> Training -> Validation -> Production.

Before running validation, do a Consistency Check across the whole Selling Playbook, not just per section. The runtime checks that fields are present; it does not catch contradictions between sections. Read `references/selling-playbook/consistency-check.md` and review the cross-section pairs there. When two statements conflict, show them side by side, ask the human which one is correct, and update the affected section(s). Do not run `train-selling --activate` until the playbook is internally consistent or the human explicitly accepts a remaining conflict.

Validation must check identity, Selling Playbook completeness, payment/legal behavior, notifications, disputes, reputation, audit, delivery, billing/collections, and safety. If the runtime returns missing fields, ask only for those fields and update only the affected playbook section.

## Output

End every training or retraining pass with the generated playbook folder path and the Selling Playbook as the primary output, using the nine section headings above. After the playbook, include the structured Selling Agent and Service objects, phase/status, Playbook version, pending inbox items, and the next human-facing action: usually `$belong-inbox`, `$belong-check-selling-pipeline`, `$belong-steer-selling-agent`, `$belong-check-active-services`, `$belong-check-payments`, or `$belong-check-reputation`.
