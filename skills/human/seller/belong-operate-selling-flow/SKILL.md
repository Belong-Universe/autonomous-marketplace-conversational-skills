---
name: belong-operate-selling-flow
description: Seller-specific human-facing act-directly skill to operate a single Belong flow by hand while the Selling Agent stands down on it. Use when a Service Provider human wants to take manual control of one inbound flow or Active Service and perform marketplace actions directly — answer-side discovery, create seller-signed proposals, negotiate, deliver, sign a Change Order, move collection/payment, or open a dispute — without disabling the agent on every other flow.
---

# Belong Operate Selling Flow

**Communication:** follow the Belong Communication Standard in `voice.md` — apply its voice and use its verbatim scripts (filling the `<slots>`) for every human-facing message.

Use this when a Service Provider human wants to drive one flow themselves: "I'll handle this buyer myself", "let me send this proposal directly", "I'll negotiate this one", or "take over this active service."

This is the act-directly category. It is the counterpart to the talk-to-your-agent skills (`$belong-train-selling-agent`, `$belong-steer-selling-agent`, `$belong-inbox`). Here the human performs marketplace actions on the flow instead of nudging or retraining the agent.

A Belong Selling Agent must always exist (ADR-001). The human never replaces the agent; they drive one flow through it. Every action is recorded under the agent's marketplace identity with `actor = human`, so audit, authority, and reputation stay intact. The agent keeps operating every other flow normally.

## Control Gate (run first, every time)

A flow is a pre-contract inbound flow (the buyer's Buying Request / Engagement Feed the seller is responding to) or an Active Service (post-contract). The human can only act directly on a flow whose `control_state` is `human_controlled`. This gate is mandatory.

1. Identify the flow id. Confirm its `control_state` with `$belong-check-selling-pipeline`, `$belong-check-active-services`, or runtime `status`.
2. If the flow is `agent_controlled`, take control first:
   ```bash
   python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py flow-control --flow-id <flow-id> --action take
   ```
   (`$belong-inbox` can also take control via `override --action intervene --flow-id <flow-id>`.)
3. If the flow is `paused`, resume it first with `flow-control --flow-id <flow-id> --action resume`, then take control. A paused flow lets nobody act; obligations, deadlines, disputes, and notices stay visible through the Marketplace Inbox.
4. Only once the flow is `human_controlled`, perform actions below. The Selling Agent will not act on this flow until control is released.

Note: pre-contract control is tracked on the buyer's Buying Request, which gates both sides for that engagement. Coordinate before taking pre-contract control so both humans are not surprised. Per-flow control is separate from the agent-wide pause in `$belong-inbox`; taking control of one flow does not pause the agent on others.

## Act Directly On The Flow

Pass `--as-human` on every action so the runtime records it as a human-direct action and applies role validation while skipping the agent's autonomy gates and authority thresholds. Use the same runtime commands the agent would, with `--as-human`:

Pre-contract:
- Answer/handle discovery on the feed: `answer-discovery --feed-id <id> --answers "..." --as-human`
- Create seller-signed Service Contract/SOW proposals: `create-proposals --feed-id <id> --as-human`
- Negotiate a proposal: `negotiate --proposal-id <id> --instruction "..." --as-human`

Post-contract (Active Service), via `active-action --active-service-id <id> --as-human --action <type>`:
- Submit a Fulfillment Task or Deliverable Evidence Package and deliver (`fulfillment-task`, `deliver`)
- Accept a buyer Change Order (`change-order` with `--signed`)
- Move collection/payment (`payment` with `--payment-type`)
- Open a dispute (`dispute`)
- Send a message (`message`) or coordinate a Human-to-Human Meeting (`meeting`)

Negotiation discount limits and other authority thresholds are bypassed because the human is performing the action directly; this IS the human authorization. Role validation still applies — a seller-side human cannot perform buyer-only actions (for example buyer signature or delivery acceptance).

## Release Control When Done

When the human is finished, hand the flow back so the agent resumes autonomous operation inside its Service Playbook:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py flow-control --flow-id <flow-id> --action release
```

Leave the flow `human_controlled` only while the human is actively driving it. Do not leave flows in human control by default; that silently stops the agent on them.

## Boundaries

- Operates only on `human_controlled` flows. Never act with `--as-human` on an `agent_controlled` flow; take control first.
- Not steering: this performs real marketplace actions. For temporary nudges that keep the agent in charge, use `$belong-steer-selling-agent`.
- Not training: do not change pricing, negotiation, legal, delivery, payment, or escalation rules here. Durable changes go to `$belong-train-selling-agent`. If the human wants an action type to *always* be performed by the human (standing policy), set it in the Service Playbook via `$belong-train-selling-agent`, not here.

## Output

Summarize: which flow is under human control and its `control_state`, each human-direct action taken and its result (authority/payment/contract effect, platform fee and seller net when money moved), whether control was released back to the agent, linked Marketplace Inbox items, the Audit Log path (actions recorded under the agent identity with `actor = human`), and the next skill — usually `$belong-check-selling-pipeline`, `$belong-check-active-services`, `$belong-check-payments`, or `$belong-inbox`.
