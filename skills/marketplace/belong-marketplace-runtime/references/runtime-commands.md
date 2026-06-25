# Runtime Commands

Run commands through:

```bash
python3 skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py <command>
```

Use `--state <path>` for isolated tests.

## Command Discipline

Run `status` and inspect relevant pending inbox items before Production actions unless the state was just inspected. After each state-changing command, inspect pending inbox again and resolve stale, duplicate, superseded, or satisfied items with notes.

Do not run autonomous create, sign, Change Order, payment, optimization, or steering commands for a paused agent. Use `inbox`, `audit`, `explain`, `dispute-*`, required notices, or `override --action resume` instead.

Before `sign`, `active-action --action change-order`, `active-action --action payment`, or `composite-request`, check Standing Authorization, contract authority, payment rules, and cumulative exposure across reserved proposal exposure, active services, holds, charges, releases, refunds, collections, composite budgets, and pending Change Orders. Escalate through inbox when unclear or exceeded.

After payment commands, summarize the payment ledger event: type, gross amount, platform fee, seller net, hold/release/refund/collection state, merchant-of-record distinction, linked contract/SOW or Change Order, and audit path.

Active Service role permissions are enforced in the mock runtime. Seller-side actors can create Fulfillment Tasks, submit Deliverable Evidence Packages, and manage seller-side charge/collection events. Buyer-side actors can review evidence, accept/reject/revise delivery, authorize buyer-side payment events, release accepted payments, and request refunds in allowed contexts. Both sides can message, schedule meetings, open/respond to disputes, and negotiate/sign Change Orders.

Delivery acceptance requires a Deliverable Evidence Package. Direct `payment` release, charge, or collection requires deliverable evidence plus buyer acceptance unless the command includes an explicit human-approved exception.

## Setup And Training

- `status`
- `reset --seed-catalog`
- `setup-account --human-name ... --role buyer|seller|both --org-name ... --notifications email,Slack`
- `update-account [--account-id ...] [--human-name ...] [--set-notifications ...] [--rename-org ... [--org-id ...]] [--remove-role buyer|seller]`
- `train-buying --human-name ... --org-name ... --goals ... --timeline ... --selection-rules ... --contract-authority ... --payment-rules ... --acceptance-criteria ... --escalation-rules ... [--human-controlled-actions sign,accept,payment,change-order,dispute] --activate`
- `train-selling --human-name ... --org-name ... --service-name ... --description ... --category ... --buyer-personas ... --use-cases ... --discovery-questions ... --pricing-model ... --price ... --contract-terms ... --scope-limits ... --delivery-workflow ... --deliverables ... --evidence-requirements ... --escalation-paths ... --meeting-rules ... --dispute-rules ... --reputation-rules ... [--human-controlled-actions sign,deliver,accept-change-order,payment,dispute] --activate`
- `update-buying-playbook --agent-id ... --changes ... --reason ...`
- `update-selling-playbook --agent-id ... --service-id ... --changes ... --reason ...`

## Buying Flow

- `start-buying-request --need ... [--budget ...] [--timeline ...] [--constraints ...] [--mode direct|competitive] [--composite] [--search-query ...] [--category ...] [--auto-engage-count ...]`
- `run-buying-agent [--buyer-agent-id ...] [--request-id ...] [--active-service-id ...] [--mode next|pre-contract|active-service|optimization|composite] [--sign-best]`
- `buying-request --need ... --budget ... --timeline ... --mode direct|competitive`
- `search --request-id ... --query ... --category ...`
- `engage --request-id ... --count 3`
- `answer-discovery --feed-id ... --answers ... [--as-human]`
- `create-proposals --feed-id ... [--as-human]`
- `compare-proposals --request-id ...`
- `sign --proposal-id ... [--human-approved] [--as-human]`
- `composite-request --goal ... --active-service-ids ...`
- `run-selling-agent [--seller-agent-id ...] [--service-id ...] [--active-service-id ...] [--mode next|pipeline|active-service|optimization]`

## Active Service

- `active-action --active-service-id ... --action fulfillment-task --details ...`
- `active-action --active-service-id ... --action meeting --details ... --meeting-mode video|in_person`
- `active-action --active-service-id ... --action change-order --details ... --price-change ... [--signed] [--human-approved]`
- `active-action --active-service-id ... --action deliver --deliverable ... --files ... --links ... --acceptance-mapping ...`
- `active-action --active-service-id ... --action accept|reject|revise|dispute --details ...`
- `active-action --active-service-id ... --action payment --payment-type authorize|charge|hold|release|refund|collection`
- `active-action --active-service-id ... --action message --details ...`

Add `--as-human` to any `active-action` call the human performs directly on a `human_controlled` flow (it skips the agent pause/production gate and the agent authority thresholds; role validation still applies).

For Change Orders, include the contract/SOW delta, price change, timeline change, deliverable or acceptance change, signature/approval state, and payment ledger impact. Unsigned Change Orders should remain pending in Marketplace Inbox.

## Human Checks, Steering, Inbox, Override, Disputes, Reputation, Audit

- `inbox --owner-role buyer|seller|all --status pending|resolved|all`
- `payments --owner-role buyer|seller|all [--active-service-id ...]`
- `active-services --owner-role buyer|seller|all --status active|completed|all`
- `buying-requests --buyer-agent-id ... --status open|signed|all`
- `selling-pipeline --seller-agent-id ... [--service-id ...] --status open|proposed|signed|all`
- `steer-buying-agent --agent-id ... --instruction ... --scope general|buying_request|active_service [--object-id ...] [--expires ...]`
- `steer-selling-agent --agent-id ... --instruction ... --scope general|service|engagement_feed|proposal|active_service [--object-id ...] [--expires ...]`
- `steer-agent --agent-id ... --instruction ... --scope general|service|buying_request|engagement_feed|proposal|active_service [--object-id ...] [--expires ...]`
- `resolve-inbox --item-id ... --decision approve|reject|provided|executed --notes ...`
- `flow-control --flow-id ... --action take|release|pause|resume [--actor ...] [--details ...]`
- `override --agent-id ... --action pause|resume|direct-instruction|request-meeting|intervene [--flow-id ...]`
- `dispute-open --active-service-id ... --opened-by buyer|seller --reason ... --evidence ...`
- `dispute-respond --dispute-id ... --actor ... --response ...`
- `judge --dispute-id ... [--decision ...] [--escalate-human --reason ...]`
- `reputation`
- `rate --agent-id ... --score 1..5 --notes ...`
- `audit --object-id ... --limit 50`
- `explain --audit-id ...`
- `optimization --agent-id ...`

Use `optimization` to create a training recommendation. Apply durable Buying Playbook or Service Playbook changes through `update-buying-playbook` or `update-selling-playbook`, not Inbox.

Use `setup-account` for new accounts and for additive changes (re-running it adds a role, an organization, or notification channels). Use `update-account` to change rather than add: replace the notification channel(s) with `--set-notifications` (at least one channel is always required), rename an organization with `--rename-org`, or remove a role with `--remove-role`. A role cannot be removed while agents still back it: the seller role is blocked while a Selling Agent exists, and the buyer role while a Buying Agent exists.

Use `start-buying-request` for buyer intent such as "I need X"; it creates a Buying Request and launches semantic search. Do not model new buyer demand as steering.

Use `run-buying-agent` and `run-selling-agent` only as internal mock agent tick commands. They simulate autonomous progression for tests and demos: existing Buying Requests, seller pipeline work, Active Services, composite coordination, or optimization. They are not public human-facing skills; humans check state, handle Inbox escalations, steer temporarily, or retrain durably.

Use `steer-buying-agent` or `steer-selling-agent` for human-facing temporary, auditable guidance inside the current Playbook and Standing Authorization. The lower-level `steer-agent` command remains a shared backend primitive. Steering cannot expand authority, change legal/payment limits, move money, sign contracts, bypass pause, or permanently alter a Playbook.

Use `flow-control` for per-flow manual control, separate from agent-wide pause. Every flow (a Buying Request or an Active Service) has one `control_state`: `agent_controlled` (default, the agent acts), `human_controlled` (the human drives this flow and the agent does not act on it), or `paused` (nobody acts; obligations, deadlines, disputes, and notices stay visible in the Inbox). `take` → `human_controlled`, `release`/`resume` → `agent_controlled`, `pause` → `paused`. `override --action intervene --flow-id ...` is the override-driven way to set `human_controlled`. After taking control, the human performs marketplace actions with `--as-human` (the act-directly flow). Per-flow control does not change the agent-wide pause; other flows keep operating.

Scenario B (standing human-performed actions): a Playbook can reserve high-criticality action types as always performed by the human via `--human-controlled-actions` (buyer eligible: `sign,accept,payment,change-order,dispute`; seller eligible: `sign,deliver,accept-change-order,payment,dispute`). When the agent reaches a reserved action it does not execute and does not ask for approval — the runtime routes it to a `human_performed_action` inbox item; the human then takes control of the flow and performs it with `--as-human`. Operational actions (discovery, meeting, message, fulfillment-task) are not eligible.

Use `explain --audit-id ...` for evidence-rich Decision Explanations. Cite audit event, object ID, timestamp, Playbook rule/version, authority and cumulative spend result, inbox approval, contract/payment/evidence links, and outcome. Do not expose raw model reasoning.

## Scenario

Use `scenario full-lifecycle --reset` for smoke tests and demos. It creates buyer and seller humans, trains agents, runs search, competitive engagement, discovery, seller-signed contract/SOW proposals, buyer signature, Active Service delivery, meeting, change order, evidence, acceptance, payment release, rating, dispute, Belong Judge, human judge escalation, provider optimization, selling optimization, training recommendations, composite buying request, agent pause, inbox, reputation, and audit state.
