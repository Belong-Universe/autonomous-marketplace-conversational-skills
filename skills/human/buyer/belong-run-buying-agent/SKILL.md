---
name: belong-run-buying-agent
description: Buyer-specific human-facing guided work for letting a Belong Buying Agent continue autonomous marketplace work. Use when a buyer-side human wants the Buying Agent to advance an existing Buying Request, answer seller-led discovery, compare proposals, sign within authority, manage buyer-side Active Service work, create Composite Buying Requests, or run Provider Optimization without exposing internal workflow skills as the human surface.
---

# Belong Run Buying Agent

Use this when the buyer-side human asks their Buying Agent to keep going on existing marketplace work.

This is not a direct human action skill. The human is asking the Buying Agent to act inside the current Buying Playbook and Standing Authorization. If the next action exceeds authority, creates legal/payment risk, is ambiguous, or needs human judgment, route to `$belong-inbox`.

## Guided Flow

Start with runtime `status`, identify the Buying Agent, and inspect buyer Inbox items first.

Then run `run-buying-agent` for the correct scope:

- Pre-contract Buying Request: search, engage, answer seller-led discovery, compare seller-signed Service Contract/SOW proposals, and optionally sign the best proposal when it fits authority.
- Active Service: review Deliverable Evidence Packages, accept/reject/revise/dispute within the Buying Playbook, trigger buyer-side payment behavior, or wait for seller evidence.
- Composite Buying Request: coordinate multiple Active Services under one buyer goal.
- Provider Optimization: create training recommendations for better providers, better deals, or complementary Services.

Use `--sign-best` only when the Buying Agent can sign inside Standing Authorization or the relevant buyer Inbox authorization is already approved.

## Boundaries

Do not use this to create a new buyer need. New "I need X" intent belongs to `$belong-start-buying-request`.

Do not use this for durable budget, provider preference, payment, acceptance, dispute, or escalation changes. Durable changes go through `$belong-train-buying-agent`.

Do not bypass pause. A paused Buying Agent cannot start new autonomous work, sign, move money, optimize, create composite requests, or receive steering.

## Output

Summarize the Buying Agent action, Buying Request or Active Service state, authority/payment result, pending buyer Inbox items, audit or Decision Explanation path, and next human-facing skill: `$belong-check-buying-requests`, `$belong-check-active-services`, `$belong-inbox`, `$belong-check-payments`, `$belong-check-reputation`, `$belong-steer-buying-agent`, or `$belong-train-buying-agent`.
