# Escalations

Capture escalation thresholds, information and authorization requests, payment exceptions, Change Order approvals, agent pause/resume rules, notification channels, and who on the buyer side owns each escalation path. For a single decision-maker, escalations route back to the same human; for multiple decision-makers, route them to the relevant invited roles (for example finance or approver).

Escalation thresholds are authority-critical: re-confirm them live before activation.

## Human-performed actions (standing manual control)

Beyond "agent executes" and "agent escalates for approval", the Buying Playbook can mark specific high-criticality action types as **always performed by the human**. This is a third authority outcome: when the agent reaches one of these, it does not execute and does not ask for approval — it hands the action to the buyer-side human, who performs it directly with `$belong-operate-buying-flow`.

Only this fixed set of buyer action types is eligible: `sign`, `accept` (delivery acceptance), `payment`, `change-order`, `dispute`. Operational actions (negotiate, discovery answers, meeting, message) are not eligible and stay with the agent; the human can still take any single flow over ad-hoc with `$belong-operate-buying-flow`.

This is a standing rule per action type, not per flow, and never arbitrary sub-flow slicing. Treat it as authority-critical and confirm it live before activation. Map the confirmed set to `--human-controlled-actions` (comma-separated).
