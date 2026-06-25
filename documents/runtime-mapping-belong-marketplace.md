# Runtime Mapping — Conversational Skills ↔ Belong Marketplace runtime

> Purpose: compare the **mock runtime** that ships with the conversational skills
> (`skills/marketplace/belong-marketplace-runtime/scripts/belong_mock.py`) against the **real
> marketplace runtime** (`github.com/Belong-Universe/belong-marketplace`), and determine **which
> variables each conversational skill must fill** so the real runtime is actually exercised instead
> of the mock.
>
> Sources of truth used:
> - Real runtime ubiquitous language: `belong-marketplace/docs/CONTEXT.md`
> - Real runtime surface (1:1 over REST): `belong-marketplace/packages/cli/skills/{discovery,negotiation,contract-management,delivery,settlement,admin}/SKILL.md`
> - Real use-cases: `belong-marketplace/src/application/use-cases/*`
> - Mock surface: `belong_mock.py` argparse (subcommands + flags)
>
> Status: analysis only (option **a**). No code is changed. Runtime alignment remains deferred.
>
> Update (2026-06-23): the real repo now ships an official **bilingual user manual**
> (`belong-marketplace/docs/manual/{en,es}/`) describing the intended product UX, plus a **live dev
> environment**. This reframes the integration strategy — see **§8. New approach (manual-informed)**.

---

## 0. The single most important difference (read first)

The two runtimes do **not** share the same actor model:

| | Mock runtime (ours) | Real runtime (belong-marketplace) |
|---|---|---|
| Tenancy unit | `account` + `org` | **Company** (the only unit of tenancy; buyer/seller capability is *emergent*, never a declared type) |
| Human identity | folded into `account` | **User** (Better Auth / OAuth), acts under an `activeCompany` |
| Buyer side | **Buying Agent** (first-class) | **No buyer agent.** The buyer is a User/Company acting via the **Belong CLI** (REST) or **MCP tools** |
| Seller side | **Selling Agent** | **Provider Agent** (the *only* agent in the system; reachable at `agentUrl`, discovered via Agent Card) |
| Offering | `service` (svc) | **Listing** (attached to a Provider Agent; carries no price) |

Consequence for variable-filling: in the real runtime **almost every command carries an
`activeCompany` (`--company <companyId>` / `X-Company-Id` header / MCP arg)**. That field does not
exist in our mock (we route by `*-agent-id`). This is the #1 variable the conversational skills would
have to start producing. There is **no buyer-agent concept to fill** on the real side — the buyer's
conversational skill drives the CLI directly on behalf of a Company.

---

## 1. Entity mapping (concept ↔ concept)

| Mock concept | Real runtime concept | Owning module | Notes / divergence |
|---|---|---|---|
| `account` (human) | **User** | Auth | Real User is OAuth-managed; no password/identity in our mock. |
| `org` | **Company** | Org & Roles | `account_type` is `individual \| organization`. |
| `org-kind: individual \| company` | `account_type: individual \| organization` | Org & Roles | **Rename value** `company` → `organization`. |
| membership role (implicit) | **Company Membership** role: `owner\|admin\|developer\|finance\|support\|buyer\|approver` | Org & Roles | Our mock has no explicit role set; 7 canonical roles exist on the real side. |
| Selling Agent | **Provider Agent** | Onboarding / Provider Gateway | Has `agentUrl`, Agent Card at `/.well-known/agent.json`, Signing Secret, API-key scopes. |
| Buying Agent | *(no equivalent)* | — | Buyer acts as User/Company via CLI/MCP. Buying-side autonomy lives only in our conversational layer. |
| `service` / svc | **Listing** | Catalog Integration + Universe | Declares exactly one **PricingModel** + `scoping_required`; **never carries a price**. |
| service tags/description | Catalog data (title, description, embedding) | Universe | Held Universe-side; Backend keeps only a thin anchor. |
| Buying Request (direct) | **Quote Request** | Negotiation | Customer-initiated request for a commercial offer against a Listing. |
| Buying Request (competitive) | **Broadcast RFP** → N **RFP Invitations** | Negotiation | Fans one requirements set to N qualifying providers; each replies with a **Sealed Quote**. |
| Discovery Questionnaire | **Service Scoping** | Service Scoping | Optional per Listing (`scoping_required`); scope summary + requirements + acceptance criteria. |
| Proposal | **Quote** | Negotiation | Commercial offer: `amount` (minor units) + `currency` + `expiry/TTL`. May be a **revision** in a counter chain. |
| Negotiation round | **Counter-offer / Revision / Round** | Negotiation | Immutable revision chain (`parent_quote_id`, `round_index`, `root_quote_id`, per-round TTL). |
| Sign / acceptance | **Accept Quote** → creates **MSA + SOW** | Negotiation → Contract Engine | Accept fires SOW creation inside the same transaction. |
| Contract | **MSA (Master Service Agreement)** | Contract Engine | Created implicitly on the first SOW between a (buyer, provider) pair; holds governing law/jurisdiction. |
| Active Service | **SOW (Statement of Work)** | Contract Engine | Owns delivery, progress, SLA, settlement; own state machine. |
| milestone | SOW milestone (PricingModel `milestone`) | Contract Engine | Real supports fixed/hourly/milestone/recurring/consumption billing shapes. |
| deliverable | **Deliverable** | Contract Engine | `external_url` + `description` + `content_hash` (`sha256:<64 hex>`). Both kinds wired: `external_url` (off-platform link) and `platform_file` (uploaded to Belong storage, server-computed sha256 + AV scan, size up to 5 GiB). |
| accept/reject/revise deliverable | **Customer Request** (kind `choice`, options `accept\|request_revision\|reject`) | Contract Engine | **No direct accept/reject** — acceptance flows ONLY through answering a Choice. |
| revise thread | **Deliverable Feedback** (`comment\|revision_request\|resolution`) | Contract Engine | Append-only thread. |
| evidence / evidence package | *(no entity)* | Audit | Evidence = the audit trail filtered by `sow_id`; plus the deliverable itself. |
| payment / escrow | **Escrow hold** (Checkout Session) → **Release** (Transfer) / **Refund** | Settlement / payments | Stripe is source of truth; SOW stores Stripe **refs + status string** only. |
| platform fee 8% | **Take Rate**: B2C `individual` = 15% (1500 bps), B2B `organization` = 10% (1000 bps) | payments | Realised as the **reduced transfer** (`charge − take_rate`), NOT `application_fee_amount`. |
| dispute | **Dispute** | Dispute Resolution | Tracer = admin/manual-only stub; evidence from audit by `sow_id`. |
| judge / dispute-respond | *(no entity yet)* | Dispute Resolution | Deferred (slices 40–41); `admin resolve dispute` returns `NOT_FOUND`. |
| reputation / rate | **Reputation** | Reputation | Deferred (Tier 3); `reviews` is a schema stub. |
| meeting (in-service + pre-contract) | **H2H Meeting** | Communication | Marketplace generates prep briefs + surfaces provider scheduling URL; happens off-platform. |
| inbox | **Notifications** (channel `inbox`) + **Customer Request** | Notifications / Contract Engine | 13 typed NotificationType values; `inbox` is one NotificationChannel. |
| flow-control / human-controlled actions / approval | **Approval Chain** | Approval Chains | Buyer-Company governance: thresholds/caps gate Quote acceptance → `pending_approval`. Deferred (Tier 3). |
| steer-agent / playbooks | *(no equivalent)* | — | Steering + playbooks are purely conversational-layer state; the runtime has none. |
| (n/a) | **API-key scope** (`quotes:write`, `deliverables:submit`, …) | Agent Auth | How Provider Agents authenticate to the marketplace. |
| (n/a) | **Connected Account** | Settlement | Company's PSP (Stripe) account; gates publication/payouts via VerificationStatus. |
| (n/a) | **Promoted Placement / Bid / Daily Budget / Impression** | Promoted Placements | Paid search boost; separate commercial flow. No mock equivalent. |

---

## 2. Value object / type mapping (the variables that change shape)

| Concept | Mock representation | Real runtime requirement | Action for skills |
|---|---|---|---|
| Money | `--starting-price "5000"`, `--budget "10000"` (decimal-ish strings, `USD`) | **Integer minor units + explicit currency.** Field names `priceCents`/`amountMinorUnits` + `currency`. Never a float. | Convert to integer minor units (e.g. `$5000.00` → `500000`). |
| Currency | `USD` (uppercase, default) | **lowercase ISO-4217** in CLI (`--currency usd`) | Lowercase the code. |
| Account type | `org-kind: individual \| company` | `account_type: individual \| organization` | Map `company` → `organization`. |
| Tenancy | `--*-agent-id` | **`activeCompany`** — `--company <companyId>` (CLI) / `X-Company-Id` (REST) / MCP arg | **Every** command must carry the acting Company id. New required variable. |
| Execution mode | *(none)* | **ExecutionMode** `test \| live` (propagated end-to-end; selects Stripe key set) | Decide and pass mode (Agent-Tester SOWs auto-route to `test`). |
| Idempotency | *(none)* | **Idempotency-Key** on money-moving / state-transition commands | Generate + persist a key for accept/checkout/release/refund/admin actions. |
| Basis points | `8%`, `0%` strings | **Integer bps** (`takeRateBps`, etc.) | Use integers (15% → 1500). |
| Duration | free text timelines | **Integer + unit suffix** (`cure_period_seconds`, `ttlSeconds`, `expires_at` timestamp) | Emit ISO-8601 timestamps / integer seconds. |
| Content hash | free `--files`/`--links` | **`sha256:<64 lowercase hex>`** (provider-computed) | Provider computes the OCI-digest form. |
| Quote expiry | *(none)* | `--expires <iso8601>` (future) + per-round TTL `[1h, 30d]` | Always set an expiry on a Quote. |

---

## 3. Action mapping — mock command → real `belong` CLI command + variables to fill

> The real Belong CLI is a thin 1:1 adapter over the REST API; each command = one REST call. These
> are the concrete variables a conversational skill would populate to drive the real runtime.

### Auth / account
| Mock | Real | Variables to fill on the real side |
|---|---|---|
| `setup-account --human-name --role --org-name --org-kind --notifications` | `belong login` (PKCE) / `belong login --device`; Company + Membership are seeded/onboarded; **Connected Account** onboarding initiation | OAuth sign-in (no name/role passed as flags); `account_type`; Stripe onboarding to reach `charges_enabled`. |
| `update-account …` | (Company/membership/notification-preference REST) | `company_id`, membership role, `notification_preferences` (per type × channel). |

### Discovery
| Mock | Real | Variables to fill |
|---|---|---|
| `search --request-id --query --tags --limit` | `belong search <query>` (`GET /v1/search`) | `query` (free text → also feeds Semantic Search), facet filters (`category`, `pricing_model`), keyset `cursor`. |
| (inspect service) | `belong listing get <listingId> --company <companyId>` | `listingId`, **`companyId`**. |
| `engage` / `answer-discovery --feed-id --answers` | `belong scoping create <listingId> --company <companyId> --summary --requirement … --acceptance …` then `scoping submit <scopingId> --company`; `scoping get`/`scoping cancel` | `listingId`, `companyId`, `summary`, repeatable `requirement`, repeatable `acceptance`, `scopingId`. |

### Negotiation
| Mock | Real | Variables to fill |
|---|---|---|
| `buying-request --need --budget --timeline --constraints --mode` | **direct:** `belong quote request <listingId> --company <companyId> [--scoping <scopingId>] [--requirements "<text>"]` | `listingId`, **`companyId`**, `scopingId` (if `scoping_required`), or inline `requirements`. |
| `buying-request --mode competitive` | **Broadcast RFP** (fan-out to N RFP Invitations; qualification reuses discovery search) | requirements set, structured discovery `filters_json`, `expires_at`. |
| `create-proposals --feed-id` | `belong quote respond <quoteRequestId> --company <companyId> --amount <minorUnits> --currency <code> --expires <iso8601>` | `quoteRequestId`, **`companyId`** (provider), **`amount` (minor units)**, `currency` (lowercase), `expires` (future ISO-8601). |
| `negotiate --proposal-id --instruction --price-delta --seller-approved` | **Counter-offer** → new Quote **revision** (slice 24) | `quoteId` of active revision, revised `amount`/`currency`/scope/`ttl_seconds`/`jurisdiction` (B2B). |
| `sign --proposal-id --human-approved` | `belong quote accept <quoteRequestId> --company <companyId>` (creates MSA + SOW) | `quoteRequestId`, **`companyId`** (buyer), `Idempotency-Key`. |
| (reject) | `belong quote reject <quoteRequestId> --company <companyId>` | `quoteRequestId`, `companyId`. |

### Contract / SOW reads
| Mock | Real | Variables to fill |
|---|---|---|
| `active-services` / `buying-requests` | `belong sow get <sowId> --company <companyId>`; `belong msa get <msaId> --company <companyId>` | `sowId`/`msaId`, **`companyId`** (party-scoped). |
| (list deliverables) | `belong sow deliverables <sowId> --company <companyId> [--cursor]` | `sowId`, `companyId`, `cursor`. |

### Delivery / acceptance
| Mock | Real | Variables to fill |
|---|---|---|
| `active-action --action deliver --files --links --deliverable` | provider: `POST /v1/sows/:id/deliverables` (REST-only — no CLI submit) | `sowId`, `external_url`, `description`, `content_hash` (`sha256:…`), `kind=external_url`. |
| `active-action --action accept/reject/revise` | `belong request respond <requestId> --company <companyId> --choice accept\|request_revision\|reject [--message <text>] [--idempotency-key <key>]` | `requestId` (the acceptance **Customer Request**), **`companyId`** (buyer), `choice`, optional `message`, `Idempotency-Key` for `accept`. |
| `active-action --action message` (info) | `belong request respond <requestId> --company <companyId> --information <text>` (≤4 KB) | `requestId`, `companyId`, `information` text. |
| (list requests) | `belong request list <sowId> --company <companyId> [--cursor]` | `sowId`, `companyId`, `cursor`. |
| (revise thread) | `belong deliverable feedback <deliverableId> --company <companyId> --kind comment\|revision_request\|resolution --message <text>`; `feedback-list` | `deliverableId`, `companyId`, `kind`, `message`. |

### Settlement / payment
| Mock | Real | Variables to fill |
|---|---|---|
| `active-action --action payment --payment-type` | **fund escrow:** `belong sow checkout <sowId> --company <buyerCompanyId>` (`POST /v1/sows/:id/checkout`) → returns hosted Stripe `url` | `sowId`, **buyer `companyId`**. (Buyer-only, pending-payment-only, idempotent.) |
| (release) | *No command* — **automatic on Deliverable `accept`** (Transfer `charge − take_rate`) | nothing extra; triggered by the `accept` Choice. |
| (refund) | *No command for parties* — system-driven on cancellation; admin: `belong admin refund sow <id>` | `sowId` (admin path). |
| `payments` (read) | `belong sow settlement <sowId> --company <companyId>` (`settlementStatus` + Stripe refs, **no amounts**) | `sowId`, `companyId`. |

### Disputes / reputation / meetings
| Mock | Real | Notes |
|---|---|---|
| `dispute-open` / `dispute-respond` / `judge` | `belong admin resolve dispute <id>` (**`NOT_FOUND` stub**, slices 40–41) | No party-facing dispute flow yet; admin-only stub. |
| `reputation` / `rate` | Reputation module (**deferred Tier 3**) | `reviews` is a schema stub. |
| `propose-meeting` / `active-action --action meeting` | **H2H Meeting** (prep brief + scheduling URL) | Off-platform; runtime surfaces the provider's scheduling URL. |

### Governance / control (conversational-only on the real side)
| Mock | Real | Notes |
|---|---|---|
| `flow-control` / `override --action intervene` / human-controlled actions (ADR-002) | **Approval Chain** (amount thresholds, caps, approver users / procurement webhook) → Quote `pending_approval` | Deferred (Tier 3). Our per-flow control + Scenario-B routing has **no runtime backing**; closest real concept is the Approval Chain on Quote acceptance. |
| `steer-agent` / `steer-buying-agent` / `steer-selling-agent` | *(no runtime concept)* | Steering lives entirely in the conversational layer. |
| `update-buying-playbook` / `update-selling-playbook` / `train-*` | *(no runtime concept)* | Playbooks are conversational-layer artifacts; the runtime stores none. |

### Admin (operator surface)
| Mock | Real | Variables to fill |
|---|---|---|
| (no real admin in mock) | `belong admin queue {pending-provider-agents,pending-listings,dead-outbox,dead-integration-events,open-disputes}` | `--limit`, `--cursor`. |
| | `belong admin approve\|reject provider-agent <id> [--reason <code>]` | `id`, typed `reason` code, `Idempotency-Key`. |
| | `belong admin approve\|reject listing <id> [--reason <code>]` | same. |
| | `belong admin suspend\|reinstate company\|provider-agent <id> [--reason <code>]` | freezes settlement on suspend. |
| | `belong admin take-rate set --account-type <…> --basis-points <bps>` | new effective-dated row. |

---

## 4. Per conversational skill — what it must produce for the real runtime

| Conversational skill | Real commands it would drive | New / changed variables it must fill |
|---|---|---|
| `belong-setup-account` | `belong login`; Connected Account onboarding | OAuth (no flags); `account_type` (`individual\|organization`); Stripe onboarding → `charges_enabled`. |
| `belong-train-selling-agent` | Provider Agent registration; `belong listing` create/publish | `agentUrl` + Agent Card; per Listing: exactly one **PricingModel**, `scoping_required`; **no price on the Listing**; API-key scopes. |
| `belong-train-buying-agent` | *(no runtime agent)* — buyer drives CLI directly | Buyer playbook stays conversational; at run time it supplies `companyId`, budgets as **minor units**, approval thresholds (→ Approval Chain when it lands). |
| `belong-start-buying-request` | `belong search`; `belong scoping …`; `belong quote request` (or Broadcast RFP) | `companyId`, `query`/filters, `listingId`, `scopingId`, `requirements`, `mode` (direct vs RFP). |
| `belong-operate-buying-flow` | `quote accept/reject`, `request respond`, `sow checkout`, `sow settlement` reads | `companyId` (buyer), `quoteRequestId`/`sowId`/`requestId`, `choice`, **`Idempotency-Key`**. |
| `belong-operate-selling-flow` | `quote respond`, deliverable submit (REST), `request` create (REST), feedback | `companyId` (provider), `amount` (minor units) + `currency` + `expires`, deliverable `external_url`+`description`+`content_hash`. |
| `belong-check-buying-requests` | `quote`/`sow`/`msa` get | `companyId` + ids (party-scoped reads). |
| `belong-check-selling-pipeline` | `sow get`, `sow deliverables`, `request list` | `companyId` + ids. |
| `belong-check-active-services` | `sow get`, `request list`, `sow settlement` | `companyId` + `sowId`. |
| `belong-check-payments` | `sow settlement` | `companyId` + `sowId` (no amounts returned). |
| `belong-check-reputation` | Reputation (deferred) | n/a until Tier 3. |
| `belong-inbox` | Notifications (`inbox` channel) + Customer Requests | `companyId`; `notification_preferences` (type × channel); `requestId` to respond. |
| `belong-steer-*` | *(no runtime concept)* | conversational-only. |
| `belong-marketplace-guide` | — | documentation only. |

---

## 5. Concepts in our skills with NO real-runtime backing (gaps)

These cannot "fill a runtime variable" because the runtime has nothing to fill — they are
conversational-layer constructs or are deferred in the real runtime:

1. **Buying Agent** — the real runtime has only Provider (seller) Agents. Buyer autonomy is ours alone.
2. **Playbooks + training** (`train-*`, `update-*-playbook`) — no runtime storage.
3. **Steering** (`steer-*`) — no runtime concept.
4. **Per-flow control + Scenario-B human-performed actions** (ADR-002) — closest real concept is the
   **Approval Chain** (deferred Tier 3); our `flow-control`/`intervene` have no runtime equivalent.
5. **Disputes party flow** (`dispute-open/respond/judge`) — real side is an admin-only `NOT_FOUND`
   stub until slices 40–41.
6. **Reputation/rating** — deferred Tier 3 (`reviews` stub).
7. **Evidence packages** — no entity; evidence = audit trail by `sow_id`.
8. **Take-rate 8% flat** — real is 15% B2C / 10% B2B and realised as a reduced transfer.

Conversely, real-runtime concepts our skills don't yet surface: **MSA**, **Counter-offer revision
chains / per-round TTL**, **Broadcast RFP / Sealed Quote**, **Connected Account / VerificationStatus**,
**Approval Chain**, **Promoted Placement**, **SLA / Cure Period**, **Signing Secret / Rotation
Window**, **API-key scopes**, **ExecutionMode (test/live)**, **Idempotency-Key**.

---

## 6. Minimum variable set to "actually use the real runtime"

If the goal is to make a conversational skill drive the real runtime end-to-end (buy flow), the
non-negotiable new variables it must start producing are:

1. **`activeCompany` / `companyId`** on every call (the central tenancy variable).
2. **Money as integer minor units + lowercase ISO-4217 `currency`** (no decimals, no `USD`).
3. **`account_type` = `individual | organization`** (map our `company` → `organization`).
4. **PricingModel + `scoping_required`** on Listings (and `agentUrl`/Agent Card to register the agent).
5. **`expires` (ISO-8601)** on every Quote.
6. **`content_hash` `sha256:<64 hex>`** + `external_url` + `description` on every Deliverable.
7. **The acceptance `choice`** (`accept|request_revision|reject`) via a Customer Request — there is
   no direct accept/reject.
8. **`Idempotency-Key`** on accept / checkout / release / refund / admin actions.
9. **`ExecutionMode` (test|live)** propagated alongside the Company.

Everything else (search/scoping/reads) is a thin overlay on top of these.

---

## 7. Suggested next steps (not done here)

- Decide the **integration boundary**: have the conversational skills call the real `belong` CLI /
  REST / MCP directly, or keep the mock and add a translation adapter.
- Resolve the **buyer-agent gap**: the real runtime has no buyer agent — confirm the conversational
  buying layer drives the CLI as the buyer Company.
- Map our **per-flow control / Scenario-B** (ADR-002) onto the real **Approval Chain** once it lands.
- Build a **field-level adapter** for the 9 variables in §6 (money conversion, company id resolution,
  idempotency-key generation, content-hash, expiry).
- Pick one flow (e.g. the buy path: search → scoping → quote → accept → checkout → accept deliverable)
  as a proof-of-concept before widening.

---

## 8. New approach (manual-informed)

The official bilingual manual (`belong-marketplace/docs/manual/{en,es}/`) and the live dev
environment change the recommended strategy. Three things the manual makes explicit:

1. **Belong is operated conversationally by design, not via a website.**
   - **Buyer** talks to their own assistant (Claude/ChatGPT), which is connected to Belong's **MCP**
     server (`https://marketplace.dev.belonguniverse.ai/v1/mcp`). The buyer never touches REST
     directly — the MCP tools *are* the buyer interface (`search_listings`, `request_quote`,
     `accept_quote`, `get_checkout_link`, `respond_to_customer_request`, …).
   - **Seller** uses **Claude Code + the `belong` CLI** (account, Provider Agent, Listing, publish,
     quote respond, deliverable submit).
   - This is **exactly the actor model our conversational skills already implement** (talk to a human,
     issue runtime commands). The product is built to be driven by an assistant — which is what we are.

2. **The runtime is far more complete than the older CONTEXT.md / CLI skills implied.** The dev env is
   live (Stripe test mode, card `4242…`) and the full commercial path works end-to-end: search →
   quote → negotiate → accept (MSA+SOW) → escrow checkout → deliverable → acceptance → settlement
   (transfer minus 15% B2C / 10% B2B take rate). The earlier "deferred / not built yet" assessments
   for several flows are **outdated**.

3. **The buyer-agent gap is reframed, not a blocker.** The manual confirms there is no buyer *agent*,
   but the buyer *is meant to act through a conversational assistant over MCP*. Our buying skills are
   precisely that missing "buyer brain" the manual assumes the user already has: playbook-driven
   authority, spend limits, escalation, per-flow human control. **Belong supplies the engine; our
   skills supply the buyer's face and judgement; MCP is the ready-made join.**

### Revised recommendation

- **Drop the "big translator" plan.** MCP already speaks the marketplace's language and is the
  official buyer surface, so the adapter shrinks to a thin concept→MCP-tool mapping (and the §6
  field conversions: money minor units, companyId, expiry, content_hash, idempotency, choice-accept).
- **Division of labour:**
  - *Belong (the engine)* — contracts, escrow, payments, take rate, state machine. We do **not**
    replicate this.
  - *Our skills (the brain + face)* — how to converse, what authority the agent has, when to stop and
    ask the human, how to train the playbook. This is value the real runtime does **not** ship.
  - *MCP / `belong` CLI (the join)* — already built by Belong.
- **Test against the live dev env now**, no real money. Safest first slice = **read-only** (read a
  SOW / settlement status) to prove the MCP↔skills fit before any state-changing call.

### Manual-confirmed facts that de-risk this (from `docs/manual/es/issues/hallazgos-validacion-manual.md`)

- The earlier blocker — *no API way to learn the `sowId` after accepting a Quote* — is **fixed**
  (PR #305): `accept` now returns `sowId`/`msaId` across REST/MCP/CLI/SDK. The buyer happy path is
  unbroken.
- Provider Agent scopes are a **closed set**: `quotes:write`, `deliverables:submit` (anything else →
  `400 SCOPES_REQUIRED`).
- A fixed-price SOW's terminal money state is `settlement_status: released` (the SOW stays
  `delivered`); only the **milestone** flow rolls up to `status: settled`. Skill copy should not
  promise "SOW settled" for fixed price.
- Take rate verified live: transfer `212500` on `250000` = 15% B2C.
