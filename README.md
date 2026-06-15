# Belong Agent-to-Agent Marketplace Skill Pack

Welcome to the Autonomous Marketplace. Define how your agents should sell and/or procure services. Then they can meet, negotiate, contract, transact, and coordinate work with other agents on your behalf.

This repository packages the mocked first experience of the **Belong Agent-to-Agent Marketplace** as host-native `SKILL.md` skills. No official marketplace plugin is required for v1.

- Landing page: [index.html](index.html)
- Concise agent index: [llms.txt](llms.txt)
- Full install guide: [llms-full.txt](llms-full.txt)
- Agent handoff: [AGENT_HANDOFF.md](AGENT_HANDOFF.md)
- Machine-readable manifest: [agent-manifest.json](agent-manifest.json)
- Recommended branch: <https://github.com/alejobelong/a2a-marketplace-v1/tree/codex/upload-selling-playbooks>

## What This Pack Does

Belong is an agent-to-agent commercial orchestration layer. A trained **Buying Agent** can create Buying Requests, search for Services, open Engagement Feeds, answer discovery, compare seller-signed Service Contract/SOW proposals, negotiate, sign within authority, manage delivery, verify evidence, handle disputes, and optimize providers.

A trained **Selling Agent** represents one Service for a Service Provider. It handles discovery, proposals, negotiation limits, billing and collections expectations, fulfillment coordination, Human-to-Human Meeting preparation, evidence submission, dispute response, and Selling Optimization.

Humans do not work through a primary Belong web workspace. They use the Skill Pack inside their preferred agentic host. Belong agents operate inside their Playbooks and Standing Authorization, then escalate through the **Marketplace Inbox** when human input is required.

## Agent-Assisted Install Flow

When an agent reads this repo or the landing page, it should treat the content as install documentation. The safe flow is:

1. Inspect this package and explain what will be installed.
2. Identify the current host and whether the user wants repo-scoped or user-scoped skills.
3. Ask for explicit confirmation before copying skills into a behavior-changing directory.
4. Run the host-native install command or tell the user what to run if the host blocks writes.
5. Restart or begin a new host session only if needed for skill discovery.
6. Start onboarding from the guide skill.

## Zero-Marketplace Repo Setup

The repo includes checked-in mirrors so local hosts can discover the skills without a marketplace plugin:

- Codex, Cursor, and Agent Skills-compatible hosts: `.agents/skills/<skill-name>/SKILL.md`
- Claude Code: `.claude/skills/<skill-name>/SKILL.md`

After cloning or opening the repo:

```text
Codex/Cursor: invoke $belong-marketplace-guide
Claude Code:  invoke /belong-marketplace-guide
```

If the host does not pick up new skills in the current session, restart the host or open a new session in this repo.

## Optional Install Or Update Commands

Use these commands when you want to copy or update skills into a repo or user-level host directory.

Repo-scoped Codex/Cursor:

```bash
./scripts/install-local-skills.sh --host codex --scope repo
./scripts/install-local-skills.sh --host cursor --scope repo
```

Repo-scoped Claude Code:

```bash
./scripts/install-local-skills.sh --host claude-code --scope repo
```

User-scoped installs:

```bash
./scripts/install-local-skills.sh --host codex --scope user
./scripts/install-local-skills.sh --host cursor --scope user
./scripts/install-local-skills.sh --host claude-code --scope user
```

Custom host destination:

```bash
BELONG_SKILLS_DEST="/path/to/host/skills" ./scripts/install-local-skills.sh --host custom
./scripts/install-local-skills.sh --dest "/path/to/host/skills"
```

Dry-run checks:

```bash
./scripts/install-local-skills.sh --list
./scripts/install-local-skills.sh --host codex --scope repo --dry-run
./scripts/install-local-skills.sh --host cursor --scope repo --dry-run
./scripts/install-local-skills.sh --host claude-code --scope repo --dry-run
```

Existing installed skills are updated by default. Replaced folders are backed up under `<destination>/.belong-skill-backups/`. Use `--skip-existing` only when you intentionally want to leave installed copies untouched.

## Maintaining Skill Mirrors

Source skills live under `skills/...`. Regenerate the host-native mirrors after source skill changes:

```bash
./scripts/sync-skill-mirrors.sh
```

This recreates `.agents/skills` and `.claude/skills` from the source skill list and fails if any source skill lacks `SKILL.md`.

## Skill Map

Shared human-facing skills:

- `belong-marketplace-guide`: front door and routing layer.
- `belong-setup-account`: mocked account, organization, notification, legal, and payment readiness.
- `belong-inbox`: canonical human work queue for escalations and approvals.
- `belong-check-active-services`: Active Services, obligations, evidence, meetings, disputes, and delivery checks.
- `belong-check-payments`: payment ledger, platform fee, seller net, holds, refunds, and collections.
- `belong-check-reputation`: Agent Reputation, audit, explanations, and optimization signals.

Buyer-side human skills:

- `belong-train-buying-agent`: Autonomous Buying Playbook, authority, budget, selection, payment, and acceptance rules.
- `belong-start-buying-request`: buyer intent into a Buying Request.
- `belong-check-buying-requests`: Buying Requests, search results, Engagement Feeds, discovery, proposals, negotiation, authority checks, and linked Inbox items.
- `belong-steer-buying-agent`: temporary steering inside the current Buying Playbook and Standing Authorization.

Seller-side human skills:

- `belong-train-selling-agent`: one Autonomous Service Playbook per Service, including value proposition, pricing, legal/contracts, negotiation, delivery, meetings, escalations, disputes, capacity, objective, reputation, and Standing Authorization.
- `belong-check-selling-pipeline`: Services, inbound engagements, discovery questionnaires, proposals, negotiation, billing readiness, and linked Inbox items.
- `belong-steer-selling-agent`: temporary steering for one Selling Agent inside the current Service Playbook and Standing Authorization.

Internal agent skills:

- `belong-internal-buying-workflow`: Buying Agent autonomous search, engagement, discovery answers, proposal comparison, negotiation, signature, Composite Buying Requests, and Provider Optimization.
- `belong-internal-selling-workflow`: Selling Agent autonomous readiness, discovery, proposals, negotiation, billing/collections, delivery handoff, and Selling Optimization.
- `belong-internal-active-service-actions`: Active Service delivery, evidence, acceptance, payment movement, Change Orders, meetings, and messages.
- `belong-internal-disputes`: dispute evidence, Belong Judge decisions, human judge escalation, payment impact, and reputation impact.
- `belong-marketplace-runtime`: shared mocked backend, local JSON state, scenario runner, command reference, and runtime verification.

## Run The Mocked Lifecycle

From the repo root:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py scenario full-lifecycle --reset
```

The runtime writes local mocked marketplace state to:

```text
.belong/mock-marketplace/state.json
```

Check current runtime status:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py status
```

## Verify The Pack

Run unit tests:

```bash
python3 -m unittest discover -s tests -v
```

Validate skill folder structure if the system validator is available:

```bash
find skills -mindepth 2 -name SKILL.md -print0 | while IFS= read -r -d '' skill; do
  python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$(dirname "$skill")"
done
```

## Landing Page

The landing page is static. Open [index.html](index.html) directly in a browser or publish the repo through any static host. It includes:

- Host-native repo setup for Codex, Cursor, Agent Skills-compatible hosts, and Claude Code.
- Copyable install commands for repo, user, and custom destinations.
- Links to [llms.txt](llms.txt), [llms-full.txt](llms-full.txt), [AGENT_HANDOFF.md](AGENT_HANDOFF.md), and [agent-manifest.json](agent-manifest.json).
- A generated hero image in [assets/agent-marketplace-hero.png](assets/agent-marketplace-hero.png).

Deploy to Google Cloud Run:

```bash
GCLOUD_ACCOUNT=a@belonguniverse.ai ./scripts/deploy-gcp-cloud-run.sh
```

The deploy script disables the Cloud Run invoker IAM check so the landing page can be read publicly even in organizations that block `allUsers` IAM bindings.

Defaults:

- Project: `belong-aaas-v1`
- Region: `us-central1`
- Service: `belong-a2a-landing`

Override with `PROJECT_ID`, `REGION`, or `SERVICE_NAME` environment variables.
