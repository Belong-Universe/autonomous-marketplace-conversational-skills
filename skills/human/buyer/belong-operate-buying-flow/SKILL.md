---
name: belong-operate-buying-flow
description: Buyer-specific human-facing act-directly skill to operate a single Belong flow by hand while the Buying Agent stands down on it. Use when a buyer-side human wants to take manual control of one Buying Request or Active Service and perform marketplace actions directly — answer discovery, sign, accept delivery, move payment, or open a dispute — without disabling the agent on every other flow.
---

# Belong Operate Buying Flow

**Communication:** follow the Belong Communication Standard in `voice.md` — apply its voice and use its verbatim scripts (filling the `<slots>`) for every human-facing message.

Use this when a buyer-side human wants to drive one flow themselves: "let me handle this request", "I'll sign this myself", or "take over this active service."

This is the act-directly category. It is the counterpart to the talk-to-your-agent skills (`$belong-train-buying-agent`, `$belong-steer-buying-agent`, `$belong-start-buying-request`, `$belong-inbox`). Here the human performs marketplace actions on the flow instead of nudging or retraining the agent.

A Belong Buying Agent must always exist (ADR-001). The human never replaces the agent; they drive one flow through it. Every action is recorded under the agent's marketplace identity with `actor = human`, so audit, authority, and reputation stay intact. The agent keeps operating every other flow normally.

## Control Gate (run first, every time)

A flow is a Buying Request (pre-contract) or an Active Service (post-contract). The human can only act directly on a flow whose `control_state` is `human_controlled`. This gate is mandatory.

1. Identify the flow id (a Buying Request or Active Service). Confirm its `control_state` with `$belong-check-buying-requests`, `$belong-check-active-services`, or runtime `status`.
2. If the flow is `agent_controlled`, take control first:
   ```bash
   python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py flow-control --flow-id <flow-id> --action take
   ```
   (`$belong-inbox` can also take control via `override --action intervene --flow-id <flow-id>`.)
3. If the flow is `paused`, resume it first with `flow-control --flow-id <flow-id> --action resume`, then take control. A paused flow lets nobody act; obligations, deadlines, disputes, and notices stay visible through the Marketplace Inbox.
4. Only once the flow is `human_controlled`, perform actions below. The Buying Agent will not act on this flow until control is released.

Per-flow control is separate from the agent-wide pause in `$belong-inbox`. Taking control of one flow does not pause the agent; it keeps running every other flow.

## Act Directly On The Flow

Pass `--as-human` on every action so the runtime records it as a human-direct action and applies role validation while skipping the agent's autonomy gates and authority thresholds. Use the same runtime commands the agent would, with `--as-human`:

Pre-contract (Buying Request):
- Answer seller-led discovery: `answer-discovery --feed-id <id> --answers "..." --as-human`
- Sign the contract: `sign --proposal-id <id> --as-human`

Post-contract (Active Service), via `active-action --active-service-id <id> --as-human --action <type>`:
- Accept delivery (`accept`), request revision (`revise`), reject (`reject`)
- Move payment (`payment` with `--payment-type`)
- Open a dispute (`dispute`)
- Send a message (`message`) or coordinate a Human-to-Human Meeting (`meeting`)

Authority thresholds (max-spend on sign) are bypassed because the human is performing the action directly; this IS the human authorization. Role validation still applies — a buyer-side human cannot perform seller-only actions.

## Release Control When Done

When the human is finished, hand the flow back so the agent resumes autonomous operation inside its Buying Playbook:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py flow-control --flow-id <flow-id> --action release
```

Leave the flow `human_controlled` only while the human is actively driving it. Do not leave flows in human control by default; that silently stops the agent on them.

## Boundaries

- Operates only on `human_controlled` flows. Never act with `--as-human` on an `agent_controlled` flow; take control first.
- Not steering: this performs real marketplace actions. For temporary nudges that keep the agent in charge, use `$belong-steer-buying-agent`.
- Not training: do not change budget, authority, selection, payment, signature, or escalation rules here. Durable changes go to `$belong-train-buying-agent`. If the human wants an action type to *always* be performed by the human (standing policy), set it in the Buying Playbook via `$belong-train-buying-agent`, not here.
- Does not start new demand: a brand-new "I need X" goes to `$belong-start-buying-request`.

## Output

Summarize: which flow is under human control and its `control_state`, each human-direct action taken and its result (authority/payment/contract effect), whether control was released back to the agent, linked Marketplace Inbox items, the Audit Log path (actions recorded under the agent identity with `actor = human`), and the next skill — usually `$belong-check-buying-requests`, `$belong-check-active-services`, `$belong-check-payments`, or `$belong-inbox`.
