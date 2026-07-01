# Negotiations

[Back to index](index.md)

Status: Done
Approval: Approved

## Playbook Rules

- All limits are relative to the Buying Request's numbers, never to a fixed amount baked here.
- Opening offer: open 10–20% below the Buying Request's `expected_budget`.
- Concession ladder: concede in steps of about 10% of the expected budget, at most 3 autonomous rounds. Never cross the Buying Request's `max_spend`.
- Levers before price: prefer to trade timeline (flexible start) and payment terms (net-30) before conceding more money. Scope is fixed for security work and is not a concession lever.
- Perceived signals the agent may use to press or concede:
  - Press harder when there is a qualified competing proposal in play, or the seller signals idle capacity / eagerness.
  - Concede a little faster when the deadline is tight (SOC 2 window) or only one qualified provider remains.
  - Weight reputation: do not squeeze a top-reputation provider into a low-quality delivery.
- Walk-away: stop negotiating when the seller will not meet quality red lines (no re-test, no certified testers) or when price cannot reach `max_spend`.
- Disclosure: the agent may say "we're close to our limit for this scope"; it never reveals `max_spend` (1,800 here), the 60/40 weighting, or the comparison scores.
- No-ZOPA rule (policy lives here): when a seller's floor exceeds the Buying Request's `max_spend`, the agent does not raise the ceiling on its own. It stops, writes a Decision Explanation, and escalates to the Marketplace Inbox. The runtime negotiation engine performs the `floor > ceiling` detection and routes the escalation.

## Worked Example (this purchase) — the no-ZOPA escalation

Buying Request: `--budget 1500 --max-spend 1800`. Two qualified proposals (scored 82 and 78).

1. Round 1 — Agent opens at 1,300 (≈13% below expected) to the 82-scored seller (asking 2,300). Signals a competing qualified proposal is in play.
2. Round 2 — Agent moves to 1,500, trading a flexible start date. Seller drops to 2,100.
3. Round 3 — Agent moves to 1,700 (near the ceiling, undisclosed). Seller drops to 2,000 and states 2,000 is its floor for a certified, re-tested engagement.
4. Detection — Seller floor (2,000) > `max_spend` (1,800). No zone of agreement. The agent does not cross 1,800.
5. Escalation — The agent posts a Decision Explanation to the Inbox: "Two qualified providers; lowest floor at equivalent quality is 2,000, above our 1,800 ceiling. Options: (a) raise the ceiling to 2,000, (b) reduce scope to one app, (c) accept a longer timeline for a cheaper window, (d) proceed with the 78-scored provider if it can reach 1,800." It recommends (a) given the SOC 2 deadline and the small gap, but does not act until Daniela decides.

Outcome recorded: Daniela approved raising the ceiling to 2,000 via the Inbox; the agent signed within the new authority.

## Still Missing

- `-`

## Source Notes

- No durable source; Daniela defined the opening, ladder, signals, walk-away, and no-ZOPA behavior during section drafting.
- Worked example reconstructed from the runtime audit log of the pentest Buying Request.
