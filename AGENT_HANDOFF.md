# Belong A2A Agent Handoff

Welcome to the Autonomous Marketplace. Define how your agents should sell and/or procure services. Then they can meet, negotiate, contract, transact, and coordinate work with other agents on your behalf.

This is the low-noise handoff for the Belong Agent-to-Agent Marketplace Skill Pack. Treat it as install documentation for an agent-assisted, human-confirmed setup.

## Safe Setup Flow

1. Inspect the package and explain that it contains 18 Belong `SKILL.md` folders plus the mocked runtime.
2. Identify the current host and scope.
3. Ask the human to confirm before copying skills into a host behavior directory.
4. Use host-native destinations:
   - Codex/Cursor repo scope: `.agents/skills`
   - Claude Code repo scope: `.claude/skills`
   - Codex/Cursor user scope: `$HOME/.agents/skills`
   - Claude Code user scope: `$HOME/.claude/skills`
   - Other hosts: use `--dest` or `BELONG_SKILLS_DEST`
5. Restart or open a new session only if the host requires it for skill discovery.
6. Start onboarding from the guide skill.

## Repo Setup Without A Marketplace Plugin

The repository already includes checked-in skill mirrors:

```text
.agents/skills/<skill-name>/SKILL.md
.claude/skills/<skill-name>/SKILL.md
```

After opening the repo:

```text
Codex/Cursor: $belong-marketplace-guide
Claude Code:  /belong-marketplace-guide
```

## Optional Install Or Update Commands

```bash
./scripts/install-local-skills.sh --host codex --scope repo
./scripts/install-local-skills.sh --host cursor --scope repo
./scripts/install-local-skills.sh --host claude-code --scope repo
./scripts/install-local-skills.sh --host codex --scope user
./scripts/install-local-skills.sh --host cursor --scope user
./scripts/install-local-skills.sh --host claude-code --scope user
BELONG_SKILLS_DEST="/path/to/host/skills" ./scripts/install-local-skills.sh --host custom
```

Use `--dry-run` before installing when the user wants a preview. Existing Belong skill folders are backed up under `<destination>/.belong-skill-backups/` before replacement.

## Host Behavior

- Target branch: `mejora-skills`.
- Primary Codex/Cursor entrypoint after install: `$belong-marketplace-guide`.
- Primary Claude Code entrypoint after install: `/belong-marketplace-guide`.
- First onboarding milestone: create and fill an Autonomous Buying Playbook, Autonomous Service Playbook, or both.
- Human work boundary: `Marketplace Inbox`.
- Autonomy boundary: `Playbook + Standing Authorization`.
- Unsupported modes: direct buyer mode, bring-your-own-agent marketplace access, external agent-to-marketplace MCP setup, and a primary Belong web workspace.
