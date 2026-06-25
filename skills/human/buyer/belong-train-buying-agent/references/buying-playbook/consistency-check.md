# Consistency Check

[Back to index](index.md)

Run this once the sections are drafted and before `train-buying --activate` or `update-buying-playbook`. The runtime checks that fields are present; it does not check that sections agree with each other.

## How To Run It

- Read the whole playbook, not one section at a time.
- For each check below, compare the relevant sections.
- When two statements conflict, show them side by side, ask the human which is correct, and update the affected section(s).
- Do not activate until every conflict is resolved or the human explicitly accepts it.

## Cross-Section Checks

| Check | Sections | Conflict example |
| --- | --- | --- |
| Spend within budget | Budget And Payment vs Negotiations | max spend or concessions exceed the stated budget |
| Selection matches preferences | Selection And RFP Rules vs Provider Preferences | a blocked provider can still win under the ranking criteria |
| Authority matches escalation | Legal And Contracts vs Escalations | signing authority above the escalation threshold |
| Acceptance matches payment | Legal And Contracts vs Budget And Payment | payment release does not line up with accepted delivery |
| Objective matches tactics | Optimization Objective vs Negotiations/Selection | "minimize cost" but ranking and concessions favor speed |
| Meeting authority matches escalation | Human-To-Human Meetings vs Escalations | confirming a meeting beyond scheduling authority auto-confirms instead of escalating |

## Output Of The Check

- A short list of conflicts found, each with the two sections and a proposed resolution.
- If none, state the playbook is internally consistent and ready for runtime validation.
