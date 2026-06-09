# Checkpoints And Approval

[Back to index](index.md) | Previous: [Disputes And Reputation Rules](08-disputes-and-reputation.md) | Next: [Generated Playbook Folder](generated-playbook-folder.md)

Use this between sections. The checkpoint keeps the human oriented and prevents silent advancement.

## Progress Calculation

There are eight playbook sections. Score each section:

- `Done` = 1
- `Partial` = 0.5
- `Missing` = 0

Progress percentage = section score total / 8, rounded to the nearest whole percent.

## Checkpoint Shape

Start with one sentence:

`Checkpoint: this is where we're at. You're <percent>% through the Selling Playbook.`

Then show a compact table:

| Section | Status | Missing |
| --- | --- | --- |
| Section name | Done, Partial, or Missing | Short gap list |

Use `-` when nothing is missing. If the table is too long, group not-yet-started sections as `Remaining sections`.

## Approval Gate

After the checkpoint, ask:

`Approve this section so we can continue to <next section>, or tell me what to change.`

Do not ask questions for the next section until the human approves the current section. If the human edits the section, update the draft and show the approval gate again.

## Final Gate

After the eighth section, show the complete Selling Playbook and ask for final approval before running `train-selling --activate` or `update-selling-playbook`.
