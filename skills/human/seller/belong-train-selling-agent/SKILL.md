---
name: belong-train-selling-agent
description: Human-facing Selling Agent training and retraining. Use when a Service Provider human needs guided, section-by-section work with existing drives, data lakes, uploaded files, shared links, compact checkpoints, automatic prefill, explicit approval gates, and a generated markdown Selling Playbook folder for one Service, including value proposition, monetization models, legal/contracts, negotiation rules, active-service delivery work, escalations, human-to-human meetings, disputes, reputation rules, and Standing Authorization.
---

# Belong Train Selling Agent

Use this for Service Provider Training, Validation, activation, and later durable Selling Playbook retraining. The output of this skill is the Selling Playbook for one Service. A Service Provider can offer multiple Services, but each Service gets its own Belong Selling Agent and its own Selling Playbook.

## Guided Flow

Start with runtime `status`. If no account exists, route to `$belong-setup-account`.

Before drafting sections, ask whether the human already has a source of truth or knowledge base to use: Drive folder, data lake, CRM/export, website, product docs, sales deck, proposal archive, legal templates, delivery SOPs, support/dispute history, spreadsheet, uploaded files, or shared links. If they provide sources or connection details that are available in the current environment, inspect them and prefill as much of the full Selling Playbook as possible.

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

Open by asking for existing information sources before collecting section answers. Example: "Do you already have a Drive folder, data lake, docs, site, sales materials, proposal archive, legal templates, SOPs, or other source I can use to prefill this Selling Playbook?"

If sources are provided:

- Confirm what you can access and what you cannot access.
- Review the sources before asking section questions.
- Build an initial prefill map across all eight Selling Playbook sections.
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
- Still missing: only the items needed to make the section usable.
- Approval gate: ask the human to approve or revise this section.

Use this approval prompt shape: "Approve this section so we can continue to `<next section>`, or tell me what to change." Treat "yes", "approved", "continue", or equivalent confirmation as approval. If the human revises the section, update it and ask for approval again.

## Reference Playbook

When the user asks for the playbook structure, wants examples, or the section draft needs a quality bar, read `references/selling-playbook/index.md`, then load only the relevant linked page. The reference is wiki-style and covers source prefill, all eight seller playbook sections, generated playbook folders, checkpoints, approval gates, and exactly one good and one bad example.

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
- `checkpoints-and-approval.md`
- `runtime-mapping.md`
- `approval-log.md`
- `final-selling-playbook.md`

Create all files once company and Service are known. Update the current section file before asking for approval. Update `checkpoints-and-approval.md` at every checkpoint. Update `approval-log.md` after every approval or revision. Update `final-selling-playbook.md` only after all eight sections are approved.

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

## Section Checkpoints

After drafting each section and before asking for approval to move on, show a checkpoint. Keep it compact and easy to scan. Start with a short line like: "Checkpoint: this is where we're at. You're 38% through the Selling Playbook." The checkpoint and approval gate happen together between sections.

Compute progress from the eight playbook sections: `Done` = 1, `Partial` = 0.5, `Missing` = 0. Round to the nearest whole percent. A section can be `Done` when it has enough detail to become playbook rules, even if some optional details remain `TBD`.

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

Capture discount limit, scope limits, price/timeline/payment concessions, contract fallback positions, buyer qualification rules, walk-away conditions, cumulative exposure checks, and the Standing Authorization envelope for autonomous negotiation.

### Way Of Work During An Active Service

Capture the delivery workflow after buyer signature: kickoff, milestones, Fulfillment Tasks, owner responsibilities, deliverable evidence packages, acceptance/revision flow, payment ledger expectations, audit trail, and how the Selling Agent coordinates ordinary provider work.

### Human-To-Human Meetings

Capture when meetings should be proposed, required attendees, agenda/prep expectations, follow-up notes, decision capture, meeting-related escalations, and when the Selling Agent can schedule autonomously.

### Escalations

Capture ordinary fulfillment escalations, exception thresholds, information requests, authorization requests, payment exceptions, Change Order approvals, agent pause/resume rules, notification channels, and who in the Service Provider organization owns each escalation path.

### Disputes And Reputation Rules

Capture dispute posture, evidence standards, response deadlines, refund/rework preferences, when to escalate to Belong Judge or human review, rating behavior, reputation signals, and how outcomes should update future Selling Optimization recommendations.

Then run `train-selling` with `--activate` when the Playbook is complete and the generated folder contains the approved final playbook.

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

## Validation

Explain validation in the four-phase lifecycle:

Setup -> Training -> Validation -> Production.

Validation must check identity, Selling Playbook completeness, payment/legal behavior, notifications, disputes, reputation, audit, delivery, billing/collections, and safety. If the runtime returns missing fields, ask only for those fields and update only the affected playbook section.

## Output

End every training or retraining pass with the generated playbook folder path and the Selling Playbook as the primary output, using the eight section headings above. After the playbook, include the structured Selling Agent and Service objects, phase/status, Playbook version, pending inbox items, and the next human-facing action: usually `$belong-inbox`, `$belong-check-selling-pipeline`, `$belong-steer-selling-agent`, `$belong-check-active-services`, `$belong-check-payments`, or `$belong-check-reputation`.
