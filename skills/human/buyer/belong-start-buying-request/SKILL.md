---
name: belong-start-buying-request
description: Buyer-specific human-facing guided work for starting a Belong Buying Request from buyer intent. Use when a buyer-side human says they need a provider, service, solution, RFP, competitive search, or help buying something through the Agent-to-Agent Marketplace.
---

# Belong Start Buying Request

**Communication:** follow the Belong Communication Standard in `voice.md` — apply its voice and use its verbatim scripts (filling the `<slots>`) for every human-facing message.

Use this when the buyer-side human expresses a new buying intention: "I need X", "find me a provider", "run an RFP", or "look in the marketplace."

This creates a Buying Request, launches semantic Service search with an optional category filter, and may open an Engagement Feed if the Buying Playbook and Standing Authorization allow it. This is not steering. Steering only nudges behavior on an existing agent/object.

## Preconditions (run first, every time)

Before starting a request, confirm a Buying Agent in Production exists. This gate is mandatory and cannot be skipped, even if the human is in a hurry.

1. Run runtime `status`.
2. If no account exists, route to `$belong-setup-account`. If an account exists but no Buying Agent is in Production, route to `$belong-train-buying-agent`. Resume only once a Buying Agent is in Production.
3. Only once a Production Buying Agent is confirmed, continue to the Guided Flow.

Never assume the agent exists from conversation or prior context. The runtime `status` is the only source of truth, and the runtime will refuse to start a request without a Buying Agent.

## Guided Flow

Start with runtime `status`. If no Buying Agent is in Production, route to `$belong-train-buying-agent`.

Collect only what is needed to start:

- Need or desired outcome
- Budget and timeline when known
- Constraints or blocked providers when known
- Direct or competitive mode
- Search query and an optional Service Category filter when useful
- Whether the request may become composite
- Whether the Buying Agent should auto-engage one or more search results

Run `start-buying-request`. The command creates the Buying Request, runs semantic search, and can open an Engagement Feed with `--auto-engage-count`.

## Boundaries

Do not sign contracts, answer seller discovery, move money, or approve exceptions in this skill. Those are autonomous Buying Agent/internal workflow actions unless they exceed the Buying Playbook and escalate through `$belong-inbox`.

If the human wants to temporarily influence an existing request, route to `$belong-steer-buying-agent`. If the human wants durable changes to budget, selection, payment, signature, or escalation rules, route to `$belong-train-buying-agent`.

## Output

Summarize the Buying Request, semantic Service Search Results, any Engagement Feed opened, what the Buying Agent will continue autonomously inside its Buying Playbook, pending Marketplace Inbox items, and the next human-facing skill: usually `$belong-check-buying-requests`, `$belong-inbox`, `$belong-steer-buying-agent`, or `$belong-check-reputation`.
