# Source Intake And Prefill

## Use only designated sources

Use only sources the human explicitly shares or names in this conversation. Do not
prefill from ambient context: other installed skills, unrelated company knowledge bases,
files the human did not point to, prior conversations, or your own background knowledge
about the buyer or what they want. What is defined here must come from what the human
tells or hands you now, never inferred from material that merely happens to be available.
Before prefilling, list back the exact sources you will use ("I'll prefill from:
<source 1>, <source 2> — anything to add or remove?") and have the human confirm. If the
human has not provided any source, ask for one or proceed with section questions directly;
never fill from anything they did not designate.

You can read shared URLs and documents directly to prefill the playbook: the runtime
does not fetch the web, but the agent running this skill can. Inspect whatever the human
shares and prefill as much of the full Buying Playbook as possible. If a source cannot be
accessed, say so and ask the human to paste the relevant excerpt or provide another.

## Connecting an existing procurement system or ERP (prefill only)

If the buyer's organization already runs a procurement system or ERP (for example SAP
Ariba, Coupa, or Oracle), Belong can connect to it to prefill this playbook: read the
already-approved budgets by category, approved and blocked vendors, payment policies,
contract templates, and approval thresholds, and propose them as starting values the
human still reviews section by section. Today this works through an export from that
system; a direct connector is on the roadmap. The connection is used only to prefill the
playbook — Belong acts as the autonomous execution layer on top of the system of record,
not a replacement for it.

## Source summary

When sources are provided, build an initial prefill map across all ten Buying Playbook
sections and show a compact source summary: source name, sections informed, confidence,
and gaps.

| Source | Sections informed | Confidence | Gaps |
| --- | --- | --- | --- |
| Procurement policy | Budget And Payment, Provider Preferences | High | acceptance criteria |
| Vendor list | Provider Preferences, Selection And RFP Rules | Medium | due diligence docs |

If a source appears useful for later sections, keep the extracted facts in the prefill map
but still present and approve only the current section while working through the guided
flow.
