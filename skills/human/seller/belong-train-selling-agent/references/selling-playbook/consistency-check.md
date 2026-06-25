# Consistency Check

[Back to index](index.md)

Run this once the sections are drafted and before `train-selling --activate` or `update-selling-playbook`. The runtime checks that fields are present; it does not check that sections agree with each other.

## How To Run It

- Read the whole playbook, not one section at a time.
- For each check below, compare the relevant sections.
- When two statements conflict, show them side by side, ask the human which is correct, and update the affected section(s).
- Do not activate until every conflict is resolved or the human explicitly accepts it.

## Cross-Section Checks

| Check | Sections | Conflict example |
| --- | --- | --- |
| Price is a fixed USD amount | Monetization | escrow modality described but no fixed `price` set |
| Capacity matches availability | Capacity And Objective vs Value Proposition | "max 2 concurrent" but "24/7 unlimited" |
| Objective matches tactics | Capacity And Objective vs Monetization | "maximize margin" but capacity left unbounded |
| Authority matches escalation | Legal And Contracts vs Escalations | contract authority above the escalation threshold |
| Acceptance matches evidence | Legal And Contracts vs Way Of Work | acceptance needs proof the evidence package never produces |
| Scope limits agree | Legal And Contracts vs Way Of Work | the SOW scope and the delivery plan disagree |
| Lead time matches timelines | Capacity And Objective vs Way Of Work | quoted delivery faster than stated lead time |

## Output Of The Check

- A short list of conflicts found, each with the two sections and a proposed resolution.
- If none, state the playbook is internally consistent and ready for runtime validation.
