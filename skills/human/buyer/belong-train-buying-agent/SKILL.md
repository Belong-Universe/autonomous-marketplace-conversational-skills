---
name: belong-train-buying-agent
description: Human-facing Buying Agent training and retraining. Use when a buyer-side human needs guided, section-by-section work with existing drives, data lakes, uploaded files, shared links, compact checkpoints, automatic prefill, explicit approval gates, and a generated markdown Buying Playbook folder, to define or durably update a Buying Playbook: buying goals and needs, budgets, payment rules, provider preferences, RFP and selection rules, proposal comparison, disclosure scope, contract/SOW authority, acceptance criteria, escalation thresholds, dispute posture, rating behavior, optimization objective, human-to-human meeting scheduling, Provider Optimization behavior, and Standing Authorization.
---

# Belong Train Buying Agent

**Communication:** follow the Belong Communication Standard in `voice.md` — apply its voice and use its verbatim scripts (filling the `<slots>`) for every human-facing message.

Use this for initial Buying Agent Training, Validation, activation, and later durable Buying Playbook retraining. Buyers cannot buy directly; every buying flow goes through a Belong Buying Agent. The output of this skill is one Buying Playbook for the buyer.

## Preconditions (run first, every time)

Before inviting context, reading any source, or drafting a section, confirm an account exists. This gate is mandatory and cannot be skipped, even if the human pastes materials or asks to jump straight in.

1. Run runtime `status`.
2. If no account exists, stop. Do not collect context or prefill. Route to `$belong-setup-account`, and resume only after the account exists.
3. Only once an account is confirmed, continue to the Guided Flow.

Never assume an account exists from conversation, shared files, or prior context. The runtime `status` is the only source of truth for account state, and the runtime will refuse training without an account.

## Use only designated sources (run before any prefill)

Use only sources the human explicitly shares or names in this conversation. Do not prefill from ambient context: other installed skills, unrelated company knowledge bases, files the human did not point to, prior conversations, or your own background knowledge about the buyer. Before prefilling, list back the exact sources you will use ("I'll prefill from: <source 1>, <source 2> — anything to add or remove?") and have the human confirm. If the human gave no source, ask for one or proceed with section questions; never fill from anything they did not designate.

Reading detail, the procurement-system/ERP prefill option, and the source summary shape: `references/buying-playbook/source-prefill.md`.

## Adapt to the buyer profile (never drop sections, never assume silently)

Early on, read the buyer profile along three axes, mostly from what the human already told you plus the account's org-kind: company or individual, single or multiple decision-makers, and one-off or recurring buying. Use the profile to adapt tone and the defaults you propose, never to drop sections. For a company, speak about "your organization"; for an individual, speak about "you". Where a deterministic field does not apply, fill it explicitly as "Not applicable — <reason>" rather than leaving it blank, so the agent still has a clear operating rule.

Never apply a profile-based assumption silently: surface it at the section's approval gate and have the human confirm it, for example "Since you're buying as an individual and not a company, I'm assuming an RFP rule does not apply — do you agree?"

## Guided Flow

Start with runtime `status`. If no account exists, route to `$belong-setup-account`.

Explain the purpose before collecting details: this flow creates and fills an Autonomous Buying Playbook. That playbook is the operating contract that lets the Belong Buying Agent procure services, compare proposals, contract, manage delivery, and optimize providers autonomously inside Standing Authorization, while escalating exceptions to Marketplace Inbox.

Gather context first, do not interrogate. Open with a single broad question, such as: "Tell me about yourself or your organization, what you want to buy, and how you like to work." Then offer the human every way to provide context, and let them combine as many as they have: answer in chat, share one or more websites or links, upload one or more files, or point to existing sources of truth (Drive folder, data lake, ERP/procurement export, policy documents, budget sheets, vendor lists, past RFPs, contract templates, or spreadsheets). Make clear they can share several at once. Then apply the designated-sources rule above before prefilling.

From the confirmed sources, prefill the full Buying Playbook, proposing reasonable values for every field, but review it section by section with the human. Treat the auto-filled draft as a starting point, not as approved training.

Build the playbook in this order:

1. Buying Goals And Needs
2. Budget And Payment
3. Provider Preferences
4. Selection And RFP Rules
5. Legal And Contracts
6. Escalations
7. Disputes And Reputation
8. Optimization Objective
9. Human-To-Human Meetings

Work one section at a time. Do not ask the human to fill every section at once. For each section, show in chat what you understood and the proposed fill, ask only the targeted questions that section needs, convert answers into clear playbook rules, and mark unknowns as `TBD` instead of inventing them. Run the per-section approval gate and the between-section checkpoint following `references/buying-playbook/checkpoints-and-approval.md`. At each approval gate, also state any profile-based assumption you made so the human confirms it rather than having it applied silently. Do not start the next section until the human approves the current one.

Always re-confirm the authority-critical fields live before activation, never accept them silently from an edited file: Contract/SOW authority, escalation thresholds, budget/max spend, and any action types reserved as always human-performed (Scenario B). For an individual or single decision-maker, contract authority usually collapses to "this human signs up to their own budget"; still confirm it live rather than skipping it.

Run `train-buying` with `--activate` once the human confirms and the Playbook is complete.

## Generated Playbook Folder

Once the buyer is known, create the markdown playbook folder and its full file set with `TBD` placeholders, then update each file as its section is drafted, revised, approved, and mapped to runtime. Default path `.belong/buying-playbooks/<org-or-buyer-slug>/` (organization slug for a company, buyer's name slug for an individual). Folder path and required file set: `references/buying-playbook/generated-playbook-folder.md`.

## Buying Playbook Sections

Build the sections in the order above. Each summary below is the headline; the full detail, edge cases, and profile-based collapses live in the linked reference, which you read when working that section.

1. **Buying Goals And Needs** — what the buyer wants to achieve, scope, success criteria, timeline, one-off vs recurring. `references/buying-playbook/01-buying-goals-and-needs.md`
2. **Budget And Payment** — total budget, max spend, currency, payment rules and timing, when spend needs human approval. `references/buying-playbook/02-budget-and-payment.md`
3. **Provider Preferences** — preferred/blocked providers, required constraints, relationship weighting, and the due diligence documents a provider must supply. `references/buying-playbook/03-provider-preferences.md`
4. **Selection And RFP Rules** — direct vs competitive, RFP structure, ranking and proposal comparison, plus the Provider Due Diligence gate/journey. `references/buying-playbook/04-selection-and-rfp-rules.md`
5. **Legal And Contracts** — contract/SOW authority, required terms, acceptance criteria, the cross-cutting disclosure discipline, and modeling a required provider invoice as an acceptance item. `references/buying-playbook/05-legal-and-contracts.md`
6. **Escalations** — thresholds, exceptions, pause/resume, channels, who owns each path, and any high-criticality action types reserved as always human-performed (Scenario B). `references/buying-playbook/06-escalations.md`
7. **Disputes And Reputation** — dispute posture, evidence standards, deadlines, rating behavior. `references/buying-playbook/07-disputes-and-reputation.md`
8. **Optimization Objective** — what to optimize across providers and the Provider Optimization goals (light for one-off, heavy for recurring). `references/buying-playbook/08-optimization-objective.md`
9. **Human-To-Human Meetings** — when to propose/accept, plus the full Calendly scheduling handshake and mechanics. `references/buying-playbook/09-human-to-human-meetings.md`

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
- Legal And Contracts -> `--contract-authority`, `--acceptance-criteria`
- Escalations -> `--escalation-rules`; action types reserved as always human-performed -> `--human-controlled-actions` (comma-separated; eligible: `sign`, `accept`, `payment`, `dispute`)
- Disputes And Reputation -> `--dispute-posture`, `--rating-rules`
- Optimization Objective -> `--optimization-goals`
- Human-To-Human Meetings -> no dedicated buyer runtime flag (the seller playbook has `--meeting-rules`); keep it in the playbook and reflect scheduling escalations through `--escalation-rules`

Identity and channel fields come from setup and context: `--human-name`, `--org-name`, `--org-kind`, `--notifications`.

## Validation

Before validation, do a Consistency Check across the whole Buying Playbook, not just per section: the runtime checks that fields are present but does not catch contradictions between sections. Review the cross-section pairs in `references/buying-playbook/consistency-check.md`, show any conflict side by side, ask the human which is correct, and update the affected section(s). Do not run `train-buying --activate` until the playbook is internally consistent or the human explicitly accepts a remaining conflict.

Explain validation in the four-phase lifecycle: Setup -> Training -> Validation -> Production. Validation must check identity, Buying Playbook completeness, payment readiness, notifications, Standing Authorization, disputes, reputation, audit, and safety. If the runtime returns missing fields, ask only for those fields and run training again.

## Output

End every training or retraining pass with the generated playbook folder path and the Buying Playbook as the primary output, using the ten section headings above. After the playbook, include the structured Buying Agent object, phase/status, Playbook version, authority envelope, what it can do autonomously, what escalates to the buyer-side human, pending inbox items, and the next human-facing action: usually `$belong-start-buying-request`, `$belong-inbox`, `$belong-steer-buying-agent`, `$belong-check-buying-requests`, `$belong-check-active-services`, `$belong-check-payments`, or `$belong-check-reputation`.

After activation, remind the human that they can always reach this agent through the Marketplace Inbox (`$belong-inbox`): respond to anything it escalates with `resolve-inbox`, or direct it at any time with `override` — pause, resume, give a direct instruction, request a meeting, or intervene.
