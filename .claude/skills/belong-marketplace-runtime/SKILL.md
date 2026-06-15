---
name: belong-marketplace-runtime
description: Shared mocked backend runtime for the Belong Agent-to-Agent Marketplace Skill Pack. Use when a Belong marketplace skill needs to read or write local JSON mock state, run the full lifecycle scenario, inspect available runtime commands, or verify that mocked accounts, agents, Services, Buying Requests, Active Services, inbox, payments, disputes, reputation, steering instructions, training recommendations, and audit logs remain coherent.
---

# Belong Marketplace Runtime

Use this as the shared mock backend for all Belong Skill Pack workflows. This skill is mostly a helper: human-facing flows should usually use `$belong-marketplace-guide`, `$belong-setup-account`, `$belong-train-buying-agent`, `$belong-start-buying-request`, `$belong-check-buying-requests`, `$belong-steer-buying-agent`, `$belong-train-selling-agent`, `$belong-check-selling-pipeline`, `$belong-steer-selling-agent`, `$belong-inbox`, `$belong-check-active-services`, `$belong-check-payments`, or `$belong-check-reputation`.

## Runtime Contract

The runtime stores mocked marketplace state in local JSON, defaulting to:

```bash
.belong/mock-marketplace/state.json
```

Run the backend with:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py status
```

If the skill is installed into `$CODEX_HOME/skills`, locate the script as a sibling skill:

```bash
python3 "$CODEX_HOME/skills/belong-marketplace-runtime/scripts/belong_mock.py" status
```

Use `--state <path>` when testing in isolation or when a persona needs a fresh state.

## Required Behavior

Preserve the resolved product model:

- Use only Belong Buying Agents and Belong Selling Agents. Never introduce bring-your-own-agent, direct buyer mode, primary Belong web workspace, or external agent-to-marketplace MCP setup.
- Treat Service as the marketplace supply primitive. Each Service has one Selling Agent.
- Treat Buying Request as the buyer demand primitive. Buyers always act through a Buying Agent.
- Treat Proposal as the seller-signed Service Contract/SOW awaiting buyer signature. Do not create a separate intermediate proposal artifact.
- Treat buyer signature as the event that creates an Active Service.
- Keep Belong as workflow, legal layer, payment orchestration, inbox, reputation, audit, and dispute facilitator, not the Service Provider or merchant of record.
- Keep all integrations mocked: OAuth, Stripe, signing provider, notifications, semantic search, reputation scoring, disputes, Belong Judge, and backend agent runtime.
- Treat Inbox as day-to-day operations only. Durable Buying Playbook or Service Playbook changes happen through training/retraining commands, while steering remains temporary and non-durable.

## References

Read `references/runtime-commands.md` before calling an unfamiliar command.
Read `references/guided-work.md` when writing or reviewing human-facing skill behavior.
Read `references/coverage-checklist.md` when checking PRD/Q&A coverage.
