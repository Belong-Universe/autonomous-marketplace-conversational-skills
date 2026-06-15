# Generated Playbook Folder

[Back to index](index.md) | Previous: [Checkpoints And Approval](checkpoints-and-approval.md) | Next: [Examples](examples.md)

During `$belong-train-selling-agent`, create a local markdown playbook folder for the seller's Service. This folder is the durable human-readable output of the training conversation.

## Default Location

Use this default unless the human asks for another destination:

```text
.belong/selling-playbooks/<company-slug>/<service-slug>/
```

If the company is unknown, use:

```text
.belong/selling-playbooks/unknown-company/<service-slug>/
```

If the Service is unknown, ask for the Service name before creating the folder. The Service is the playbook unit.

## Slug Rules

- Lowercase ASCII
- Replace spaces and separators with hyphens
- Remove characters that are not letters, numbers, or hyphens
- Collapse duplicate hyphens
- Keep the slug short but recognizable

## Required Files

Create the full file set as soon as company and Service are known. Unstarted sections should contain `Status: Missing` and `TBD` placeholders.

```text
index.md
source-prefill.md
01-value-proposition.md
02-monetization-models.md
03-legal-and-contracts.md
04-negotiations.md
05-active-service-work.md
06-human-to-human-meetings.md
07-escalations.md
08-disputes-and-reputation.md
09-capacity-and-objective.md
checkpoints-and-approval.md
runtime-mapping.md
approval-log.md
final-selling-playbook.md
```

## File Roles

| File | Role |
| --- | --- |
| `index.md` | Entry point, company/service metadata, current progress, and links to all files. |
| `source-prefill.md` | Sources reviewed, access status, source summary, extracted facts, conflicts, and gaps. |
| `01-*` through `09-*` | One approved or draft playbook section per file. |
| `checkpoints-and-approval.md` | Current progress table and latest approval gate. |
| `runtime-mapping.md` | Mapping from approved playbook content to `train-selling` or `update-selling-playbook` arguments. |
| `approval-log.md` | Human approvals, requested revisions, timestamps when available, and section status changes. |
| `final-selling-playbook.md` | Consolidated final playbook assembled after all nine sections are approved. |

## Section File Shape

Each section file should use this shape:

```markdown
# <Section Name>

[Back to index](index.md)

Status: Missing | Partial | Done
Approval: Not requested | Pending | Approved

## Playbook Rules

- Rules the Selling Agent should follow.

## Still Missing

- `TBD` items or `-` when complete.

## Source Notes

- Source names, links, or file references used for this section.
```

## Update Rhythm

- Create all files once company and Service are known.
- Update `source-prefill.md` after reviewing existing sources.
- Update the current section file before asking for approval.
- Update `checkpoints-and-approval.md` at every checkpoint.
- Update `approval-log.md` whenever the human approves, rejects, or revises a section.
- Update `runtime-mapping.md` after a section is approved and again before runtime activation.
- Update `final-selling-playbook.md` only after all nine sections are approved.

Do not mark a section `Approved` in files until the human explicitly approves it in conversation.
