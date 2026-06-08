# Belong Agent-to-Agent Marketplace Skill Pack

This repo contains the mocked first-experience Skill Pack for the Belong Agent-to-Agent Marketplace. It is built as a set of Codex skills plus a shared local JSON runtime.

## Layout

- `documents/`: Linear project document mirrors and the Skill Pack coverage review.
- `skills/human/shared/`: human-facing shared marketplace skills.
- `skills/human/buyer/`: buyer-side human skills.
- `skills/human/seller/`: seller-side human skills.
- `skills/autonomous/`: internal Buying Agent and Selling Agent capabilities.
- `skills/marketplace/`: mocked marketplace backend/runtime.
- `tests/`: validation for the mocked lifecycle, skill routing, and runtime behavior.

## Install

Install all skill folders from this repo into Codex:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo alejobelong/a2a-marketplace-v1 \
  --path skills/marketplace/belong-marketplace-runtime \
  --path skills/human/shared/belong-marketplace-guide \
  --path skills/human/shared/belong-setup-account \
  --path skills/human/shared/belong-inbox \
  --path skills/human/shared/belong-check-active-services \
  --path skills/human/shared/belong-check-payments \
  --path skills/human/shared/belong-check-reputation \
  --path skills/human/buyer/belong-train-buying-agent \
  --path skills/human/buyer/belong-start-buying-request \
  --path skills/human/buyer/belong-run-buying-agent \
  --path skills/human/buyer/belong-check-buying-requests \
  --path skills/human/buyer/belong-steer-buying-agent \
  --path skills/human/seller/belong-train-selling-agent \
  --path skills/human/seller/belong-run-selling-agent \
  --path skills/human/seller/belong-check-selling-pipeline \
  --path skills/human/seller/belong-steer-selling-agent \
  --path skills/autonomous/belong-internal-buying-workflow \
  --path skills/autonomous/belong-internal-selling-workflow \
  --path skills/autonomous/belong-internal-active-service-actions \
  --path skills/autonomous/belong-internal-disputes
```

Restart Codex after installing.

## Start

Use:

```text
$belong-marketplace-guide
```

The guide routes the human through shared setup/checks, buyer-specific Buying Agent training, Buying Request start/run/check/steering, seller-specific Selling Agent training, seller run/pipeline check/steering, Inbox escalations, Active Service checks, payment checks, reputation/audit checks, and the full mocked scenario.

The autonomous Buying Agent and Selling Agent capabilities remain available as internal skills. Humans should not use them as the main surface; agents execute those workflows and escalate through `belong-inbox` when needed.

## Mock State

The runtime writes local mocked marketplace state to:

```text
.belong/mock-marketplace/state.json
```

Run the complete scripted scenario:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py scenario full-lifecycle --reset
```

Run checks:

```bash
python3 -m unittest discover -s tests -v
find skills -mindepth 2 -name SKILL.md -print0 | while IFS= read -r -d '' skill; do python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$(dirname "$skill")"; done
```
