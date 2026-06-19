# Consistency Check

Before running validation, do a Consistency Check across the whole Buying Playbook, not
just per section. The runtime checks that fields are present; it does not catch
contradictions between sections. Review at least these cross-section pairs:

- Budget vs negotiation limits: max spend and concessions must not exceed the budget.
- Selection rules vs provider preferences: a blocked provider must not be winnable
  under the ranking criteria.
- Contract authority vs escalation thresholds: anything above signing authority must
  trigger an escalation, not an autonomous signature.
- Acceptance criteria vs payment rules: payment release must line up with what counts
  as accepted delivery.
- Optimization objective vs negotiation and selection: the stated objective (cost,
  quality, speed, relationships) must match how the agent ranks and concedes.
- Meeting authority vs escalation thresholds: confirming a meeting beyond the agent's
  scheduling authority must escalate, not auto-confirm.

When two statements conflict, show them side by side, ask the human which one is
correct, and update the affected section(s). Do not run `train-buying --activate` until
the playbook is internally consistent or the human explicitly accepts a remaining
conflict.
