# Negotiations

[Back to index](index.md) | Previous: [Selection And RFP Rules](04-selection-and-rfp-rules.md) | Next: [Legal And Contracts](06-legal-and-contracts.md)

This section defines how far the Buying Agent can negotiate without human approval, and how it haggles the way a person would — reading signals, conceding in steps, and knowing when to walk away. The seller side mirrors this with its own floor and signals in `04-negotiations.md`.

## Source Signals

Look for negotiation notes, lost/won-deal notes, procurement redlines, discount expectations, payment-term standards, and leadership guidance on concessions.

## Required Fields

- `opening_offer`: the first counter, typically below the expected budget.
- `concession_ladder`: how much the agent concedes and in what steps, and the maximum number of autonomous rounds.
- `perceived_signals`: the cues the agent uses to press harder or concede — competitive tension (other quotes available), buyer-side urgency, seller eagerness or stated constraints, provider reputation, service exclusivity.
- `levers`: what the agent can trade besides price — scope, timeline, payment terms.
- `walk_away`: conditions to stop (price, terms, risk).
- `cumulative_exposure`: checks against total committed spend across active purchases.
- Standing Authorization envelope for autonomous negotiation.
- `disclosure_scope`: give a clear, usable answer without exposing the ceiling, ranking weights, walk-away point, or internal policy.
- `no_zopa`: when the seller's floor exceeds the binding ceiling (`max_spend`) and there is no zone of agreement, the agent escalates to the Marketplace Inbox with a Decision Explanation. It must **never** raise the ceiling on its own.

## Quality Bar

The section is `Done` when the Buying Agent can open, concede, and close inside a clear authority envelope, use perceived signals to negotiate price/scope/timeline/payment, and stop or escalate at the right point.

## Guardrails

- Do not concede or sign above the binding `max_spend` for the purchase.
- Do not reveal the ceiling, ranking weights, walk-away point, margins, or internal policy to a seller.
- Do not loop past the maximum autonomous rounds; escalate instead.
- No-ZOPA division of labor: the **decision** (escalate, never auto-widen the ceiling) is playbook policy and lives here; the runtime negotiation engine **detects** floor > ceiling, stops the loop, emits the Decision Explanation, and routes to the Inbox.
