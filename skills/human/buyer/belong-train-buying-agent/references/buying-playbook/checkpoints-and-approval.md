# Checkpoints And Approval Gates

## Per-section approval gate

Work one section at a time. Do not ask the human to fill every section at once. Before
locking a section, always show:

- What I understood, in chat only: compact bullets from the human's answers, files, and links.
- Proposed section fill: the playbook rules you plan to write for that section.
- The section file itself: show or share the updated `0X-...md` so the human can read
  the full section before approving, not only the summary.
- Profile-based assumptions: any field you marked Not applicable or collapsed because of
  the buyer profile, stated plainly so the human can confirm the inference rather than
  having it applied silently.
- Still missing: only the items needed to make the section usable.
- Approval gate: ask the human to approve or revise this section.

Use this approval prompt shape: "Approve this section so we can continue to `<next
section>`, or tell me what to change." Treat "yes", "approved", "continue", or equivalent
confirmation as approval. If the human revises the section, update it and ask for approval
again. Do not ask the first question for the next section until the human approves the
current one.

## Section checkpoints

After drafting each section and before asking for approval to move on, show a checkpoint.
Keep it compact and easy to scan. Start with a short line like: "Checkpoint: this is where
we're at. You're 38% through the Buying Playbook." The checkpoint and approval gate happen
together between sections.

Compute progress from the ten playbook sections: `Done` = 1, `Partial` = 0.5, `Missing` =
0. Round to the nearest whole percent. A section can be `Done` when it has enough detail to
become playbook rules, even if some optional details remain `TBD`.

Use this table shape:

| Section | Status | Missing |
| --- | --- | --- |
| Buying Goals And Needs | Done | - |
| Budget And Payment | Partial | max spend, payment timing |
| Provider Preferences | Missing | all |

Keep `Missing` cells short. Use `-` for nothing missing. If the table gets long, combine
the not-yet-started sections into one final row such as `Remaining sections`.
