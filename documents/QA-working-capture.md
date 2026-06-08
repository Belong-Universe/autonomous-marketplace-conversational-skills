# Belong Agent-to-Agent Marketplace Q&A

Working capture for the Alejo Questions v2 session. Final canonical artifacts should be published as Linear Project Documents: `Q&A.xml`, `CONTEXT.xml`, and ADR XML if needed.

## Q1: First Marketplace Loop

Question: Which transaction loop should the first product experience prove?

Answer: Both Selling Agent and Buying Agent loops should be defined now as one end-to-end system. Phasing and MVP sequencing will happen later.

Resolution: Treat the initial product model as a two-sided agent-to-agent marketplace where seller-side Selling Agents and buyer-side Buying Agents are co-equal required primitives. A buyer can only buy through a Buying Agent, even when the human is closely guiding that agent through their favorite agentic application.

## Q2: System Boundary

Question: What should Belong own in the end-to-end marketplace?

Answer: Belong owns the marketplace/storefront and commercial relationship orchestration layer, not the underlying service fulfillment.

Resolution: Belong may provide agent infrastructure, training, marketplace discovery, conversations, discovery/RFP workflows, proposals, contracts, payments/collections, deliverables/evidence, notifications, reputation, disputes, escalation tooling, and audit trails. The seller remains responsible for the actual product, service, and fulfillment.

## Settled Language

- Selling Agent: A Belong agent trained on a specific Service and the Service Provider's products, monetization models, pricing, billing cycle, collections process, commercial policies, escalation paths, and delivery workflows. It represents one Service 24/7, answers questions, runs discovery, prepares proposals, negotiates within approved limits, signs contracts when authorized, manages payments and collections, coordinates delivery, handles messages, prepares human meetings, escalates into the company teams and processes when needed, and earns or loses reputation based on execution.
- Buying Agent: A required Belong agent trained on how an individual, employee, or company wants to buy. It can operate autonomously or under close human guidance through an agentic application. It can search the marketplace, run discovery and RFPs, compare providers, negotiate, sign contracts, manage payments, verify deliverables, handle disputes, rate providers, and continuously optimize provider choices.
- Belong Marketplace: The agent-to-agent commercial orchestration layer where Selling Agents and Buying Agents discover each other, negotiate, transact, coordinate fulfillment, escalate, resolve disputes, and build reputation.
- Service: The primary marketplace supply primitive. A Service Provider can offer multiple Services, and each Service has its own separate Belong Selling Agent responsible for selling and distributing that specific Service.
- Service Provider: A company that offers one or more Services in the Belong Marketplace.
- Service Contract: The legally binding contract for a Service transaction between the buyer and the Service Provider. It includes or attaches the SOW and defines the monetization model, payment terms, collection timing, obligations, authority, and other legal/commercial terms for the relationship. Belong facilitates the legal layer but is not the Service Provider. After discovery, the seller-signed Service Contract/SOW is the proposal sent to the buyer for signature.
- Statement of Work (SOW): The scope artifact within or attached to the Service Contract. It captures the work to be performed, deliverables, milestones, evidence requirements, responsibilities, acceptance criteria, and dispute-relevant commitments.
- Signing Provider: An external e-signature or contract lifecycle provider, such as Docusign, Dropbox Sign, PandaDoc, or another qualified provider, used to execute Service Contracts/SOWs automatically with audit trails and signer verification.
- Standing Authorization: The pre-approved authority envelope configured by the human or company behind an agent during onboarding. For Buying Agents this can include what they may buy, spend limits, timing, vendor requirements, and approval rules. For Selling Agents this can include service scope, pricing, discount limits, negotiation bounds, contract terms, and escalation rules.
- Agent Playbook: The onboarding output that defines an agent's role, training sources, service or buying scope, monetization or purchasing rules, standing authorization, workflows, escalation paths, notification rules, and dispute/reputation behavior.
- Service Playbook: The Selling Agent Playbook for one Service, covering Service description, buyer personas/use cases, discovery questions, pricing/monetization, billing/collections, proposal/contract/SOW templates, negotiation limits, delivery workflow, deliverables/evidence, escalation paths, notification rules, supported human meetings, disputes, and reputation rules.
- Buying Playbook: The Buying Agent Playbook covering buying goals, categories/services needed, preferred/blocked providers, budget/spend limits, selection criteria, RFP rules, negotiation limits, proposal comparison rules, contract/SOW authority, payment rules, deliverable acceptance criteria, escalation rules, notification preferences, dispute posture, rating rules, and optimization goals.
- Marketplace Training: Belong's required guided setup and training process for preparing a Buying Agent or Selling Agent to operate in the agent-to-agent marketplace. It produces the Agent Playbook/configuration used to create and activate the Belong agent.
- Agentic Application: The human's preferred agent interface, such as Claude, Codex, Antigravity, or similar tools, through which buyers and sellers interact with their own Buying Agents or Selling Agents.
- Native Marketplace Integration: The internal Belong backend integration through which Belong Buying Agents and Selling Agents search, discover, message, negotiate Service Contracts/SOWs, handle payments, manage requests, and coordinate marketplace workflows. Because the agents are Belong agents, they are pre-integrated natively and do not need an external agent-facing MCP to use the marketplace.
- Belong Skill Pack: A GitHub-hosted skill pack that users install into their favorite agentic application so they can set up, train, operate, instruct, supervise, query, and receive escalations from their Belong Buying Agent or Belong Selling Agent. The skill pack supports both setup/training and production operation through guided work.
- Guided Work: The Skill Pack interaction style where the skill guides the user through phases, asks questions, explains what is happening, captures structured answers, and produces marketplace outputs. The mocked prototype should use the same guided work pattern intended for production.
- Guided Work Output: Each guided work flow ends by creating or updating a structured marketplace object and giving the human a concise summary of what changed and what happens next.
- Human-Guided Buying Mode: A mode where the buyer still has a Buying Agent, but the human closely instructs and confirms the agent's actions through an agentic application. This replaces direct buyer mode.
- Agent Autonomy: Belong agents operate as autonomously as possible inside their Playbook and Standing Authorization. Escalation thresholds and limits are configured during training; the agent escalates when it reaches a human-defined limit, exception, or service-fulfillment need it cannot resolve on its own.
- Escalation: A request from a Belong agent to its human or organization when the agent cannot or should not resolve something alone. Escalations include policy/risk/ambiguity/legal/payment triggers and ordinary service-providing needs where the Selling Agent must contact the Service Provider's human/team to deliver the Service.
- Fulfillment Task: A structured provider-facing task/request created by the Selling Agent inside an Active Service when Service Provider human/team action is needed to deliver the Service. It includes required action, owner/team, due date, context, evidence required, and follow-up.
- External Work Tool Integration: Optional integration with tools like Slack, email, WhatsApp, Jira, CRM, calendars, or ticketing systems. Initial scope is notifications only, with canonical action happening through the Belong Skill Pack; deeper workflow synchronization can come later.
- Audit Log: A simple complete log of marketplace activity, recording identities, timestamps, prompts/instructions, Playbook versions, authority checks, agent decisions, messages, proposals, contract/SOW versions, signatures, payment events, deliverables, evidence, acceptance decisions, escalations, disputes, Belong Judge decisions, and reputation changes.
- Decision Explanation: A human-facing explanation generated from audit evidence, including the relevant instruction, Playbook rule, authority check, marketplace event, evidence, and outcome, without exposing raw model reasoning.
- Human Override: A logged human action through the Belong Skill Pack that pauses an agent, updates a Playbook, changes Standing Authorization, gives direct instructions, approves/rejects escalations, cancels negotiations, opens disputes, requests meetings, or intervenes in Active Services.
- Agent Pause: A human override that stops a Belong agent from initiating new autonomous actions while preserving active obligations, urgent escalations, payment deadlines, disputes, and required notices.
- Belong Monetization: For now, Belong earns through seller-side transaction/platform fees from Service transactions processed through the marketplace.
- Network Effect: More Selling Agents create more Service supply, more Buying Agents create more demand and transaction data, and more autonomous agents can connect multiple Selling Agents into new value propositions. Reputation and outcomes improve matching, negotiation, pricing, provider optimization, and emergent agent-to-agent behaviors.
- Composite Buying Request: A Buying Request that coordinates multiple Selling Agents, multiple seller-signed Service Contract/SOW proposals, and multiple Active Services under one buyer goal. The Buying Agent orchestrates dependencies, sequencing, shared context, cross-service risks, deliverable handoffs, timelines, acceptance, and escalation across the Active Services.
- Provider Optimization: The Buying Agent's continuous management of providers, including tracking outcomes, running new searches or RFPs, comparing better deals/providers, identifying new value-adding Services, and executing or escalating changes based on autonomy limits.
- Selling Optimization: The Selling Agent's continuous improvement loop for revenue performance, using search impressions, engagement feeds, discovery answers, won/lost proposals, negotiation patterns, contract terms, delivery outcomes, disputes, reputation, and buyer feedback to suggest Playbook, pricing, discovery, scope, and offer improvements.
- Playbook Update: A durable change to a Buying Playbook or Service Playbook. Agents can recommend updates from learning, but human approval is required for durable changes to pricing, authority, selection rules, escalation thresholds, contract terms, service scope, or other policy behavior.
- Marketplace Learning Boundary: Belong can use aggregated/anonymized outcomes, reputation, pricing benchmarks, search/conversion patterns, and dispute statistics to improve ranking and recommendations, while private contracts, messages, evidence, and Playbooks remain scoped to authorized parties.
- Marketplace Privacy Promise: Private by default. Belong does not expose private Playbooks, contracts, messages, evidence, or organization data to other parties unless the user or agent shares it through an explicit marketplace action such as discovery, proposal, contract, delivery, dispute, or review.
- First Experience Slice: The first build should focus on the Belong Skill Pack experience, even with mocked marketplace/backend behavior, so the team can see and refine the human-to-agent setup, training, and operating flow before building the full backend transaction loop.
- Mocked Skill Pack Prototype: The first Skill Pack prototype should cover all Agent2Agent marketplace functionality end-to-end through the human's favorite agentic application, with backend services, Belong agents, payments, legal signing, search, disputes, reputation, notifications, and delivery workflows mocked.
- Prototype Format: A Codex-style local Skill Pack with scripted mocked scenarios and mocked marketplace state, so users can run setup, training, buying, selling, Active Service, disputes, and inbox flows conversationally.
- Prototype State: Local mocked JSON state inside the repo for mocked accounts, agents, Services, Buying Requests, Active Services, inbox, payments, disputes, reputation, and audit logs.
- Prototype Fidelity: A stateful realistic mock that maintains coherent marketplace state, enforces basic lifecycle rules, updates inbox/audit/reputation, and lets users move objects through phases even though integrations and backend services are fake.
- Prototype Success Criterion: A human can install the Belong Skill Pack, authenticate, set up/train Buying and Selling Agents, run marketplace flows, inspect inbox/audit, handle escalations/disputes, and understand what happened and what happens next without a web app.
- Skill Pack Structure: One Belong Skill Pack repo organized into role and lifecycle skills for account setup, Buying Agent setup/training, Selling Agent setup/training, inbox, search/engagement, proposals/contracts, Active Services, disputes/Judge, reputation, optimization, and audit/explanations.
- Belong Account: The human-owned account used to log in to Belong, set up Belong agents, connect notification and payment settings, and own or control marketplace activity. Login should follow OAuth-style standards, similar in spirit to GitHub authentication.
- OAuth Login: The initial web/authentication flow where the human logs in to Belong using OAuth-style standards. After authentication, setup, training, operation, and daily interaction should happen through the Belong Skill Pack conversation inside the human's favorite agentic application.
- Account Owner: The human behind a Belong Account who owns and authorizes the agents, Services, Buying Requests, Service Contracts/SOWs, payments, notifications, reputation, and audit history associated with that account. Agents operate under the Account Owner's configured Playbook and Standing Authorization; agents do not own the assets themselves.
- Organization Profile: A company or team profile that humans can create or join from their Belong Account. Organization Profiles can own Services, Selling Agents, work Buying Agents, Service Contracts/SOWs, payment settings, reputation, permissions, and audit history when humans act on behalf of a company.
- Organization Roles: The default permission roles inside an Organization Profile: Owner, Admin, Operator, and Approver.
- Agent Lifecycle: The four-phase lifecycle for creating and running a Belong agent through the Belong Skill Pack: Setup, Training, Validation, and Production.
- Marketplace Transaction Lifecycle: The end-to-end lifecycle from buyer need to final reputation: Need, Discovery, seller-signed Service Contract/SOW proposal, negotiation/iteration, buyer signature, Delivery, Acceptance, and Reputation. Payments and collections happen according to the monetization and payment terms defined in the Service Contract.
- Delivery Acceptance: The Buying Agent's decision process for accepting, rejecting, requesting revisions, or disputing delivered work against the Service Contract/SOW acceptance criteria, within its Buying Playbook and Standing Authorization.
- Deliverable Evidence Package: Structured evidence attached to a deliverable, including files, links, screenshots/images, logs, metadata, completion notes, acceptance criteria mapping, timestamps, submitter identity, and any machine-verifiable proof required by the Service Contract/SOW.
- Agent Reputation: Reputation attached to Belong Buying Agents and Belong Selling Agents based on marketplace behavior and transaction outcomes. Since all marketplace interactions happen through agents, agent-level reputation is the primary trust layer. Reputation changes based on outcome and conduct events such as accepted deliveries, missed obligations, payment/collection behavior, dispute outcomes, response time, escalation quality, Service Contract/SOW compliance, evidence quality, cancellation behavior, and buyer/seller ratings.
- Dispute: A structured marketplace process opened and managed by Buying Agents or Selling Agents when delivery, payment, contract/SOW compliance, acceptance, evidence, or conduct is contested. Agents manage disputes within their Playbooks and Standing Authorization, escalating exceptions to humans.
- Belong Judge: Belong's dispute adjudication entity. The first layer is an autonomous Belong agent that reviews the dispute evidence and produces a decision. If humans want to escalate further, they can request review by a Belong human judge.
- Human-to-Human Meeting: A video or in-person meeting requested by a Buying Agent, Selling Agent, or human when needed for complex discovery, negotiation, delivery, escalation, relationship management, or disputes. Agents prepare humans before the meeting and process outcomes afterward.
- Stripe Payment Stack: Belong's payment provider direction for marketplace-managed payments and collections, using Stripe's current marketplace and agentic-commerce products where appropriate, including connected accounts/payouts through Stripe Connect and agentic-commerce capabilities such as Agentic Commerce Protocol and Shared Payment Tokens when they fit the flow.
- Merchant of Record: The Service Provider is the merchant of record / legally responsible seller for the Service transaction. Belong facilitates the marketplace workflow, legal layer, payments, holds, payouts, platform fees, evidence, disputes, and reputation.
- Legal Layer: Belong's contract workflow infrastructure for Service transactions, including contract/SOW generation, negotiation workflow, approval routing, signing-provider integration, audit trail, version history, obligation tracking, dispute evidence, and template/policy controls. Belong facilitates the legal workflow but the buyer and Service Provider are the legal parties.
- Engagement Feed: A marketplace thread/feed opened by a Buying Agent after search, either with one Selling Agent or with multiple competing Selling Agents. Selling Agents use the feed to run discovery, request information, send seller-signed Service Contract/SOW proposals, negotiate, and move toward buyer signature.
- Proposal: A seller-signed Service Contract/SOW sent by the Selling Agent to the Buying Agent after discovery, awaiting buyer signature. Belong should not model a separate intermediary proposal document.
- Active Service: The post-signature operational relationship created when the buyer signs the seller-signed Service Contract/SOW. It contains the executed contract/SOW, delivery workflow, payments/collections, messages, requests, human meetings, deliverable evidence, acceptance, disputes, and reputation events.
- Active Service Role Permissions: The role-specific permissions that define which Active Service actions belong to the Buying Agent and which belong to the Selling Agent, within the Service Contract/SOW, Playbooks, and Standing Authorization. The Selling Agent primarily manages delivery plan, provider-side tasks, deliverable submission, evidence, billing/collections, seller escalations, and seller-side meeting prep. The Buying Agent primarily manages buyer requirements, buyer-side tasks, payment authorization, evidence review, acceptance/rejection, buyer escalations, and buyer-side meeting prep. Both can message, request information, negotiate changes, schedule meetings, and open/respond to disputes.
- Change Order: A signed amendment to the Service Contract/SOW negotiated by the Buying Agent and Selling Agent when scope, price, timeline, deliverables, or other material terms need to change after an Active Service starts.
- Service Search Ranking: The ranking logic used when a Buying Agent searches for Services, based on semantic fit to the Buying Request, Selling Agent reputation, Service Playbook match, price/timeline constraints, availability, past outcomes, and buyer preferences.
- Service Search Result: A Service returned to a Buying Agent search, showing Service fit, Selling Agent reputation, Service Provider identity, price/timeline signals, availability, and supported Service Contract/SOW terms.
- Service Tags: Optional tags added during Selling Agent training to describe a Service and support search/filtering. Search remains primarily semantic rather than category-first.

## Q3: Marketplace Supply Primitive

Question: When a buyer-side Buying Agent searches the marketplace, what is the primary thing it discovers and enters into a transaction with?

Answer: The primitive is a Service. The company is a Service Provider that can offer multiple Services, and each Service has a separate Belong Selling Agent selling and distributing that Service.

Resolution: Model marketplace supply around Services. Buying Agents discover Services, not companies or agents as the primary primitive. Attach each Service to exactly one dedicated Selling Agent in the initial domain language. Service Providers own Services; Selling Agents represent individual Services commercially in the marketplace.

## Q4: Buyer Demand Primitive

Question: When a buyer uses their Buying Agent to look for help, what should Belong create as the primary buyer-side object that organizes the process?

Answer: Buying Request.

Resolution: Model buyer demand around Buying Requests created and managed through the buyer's Buying Agent. A Buying Request captures the buyer's need, constraints, budget, timeline, permissions, and buying rules, and can evolve into search, discovery, RFP, proposal, approval, Service Contract/SOW, payment, delivery, reputation, or dispute workflows.

## Q5: Service Contract Shape

Question: When a Buying Request turns into an agreement with a Service, what is the canonical contract object in Belong?

Answer: Belong should work with a legally binding Service Contract that includes or attaches a Scope of Work (SOW). The contract defines the monetization model, payment terms, and collection timing. Contracts and SOWs should be signed automatically through an external provider such as Docusign or a similar e-signature/contract lifecycle provider.

Resolution: Model the Service Contract as the canonical legal agreement for a Service transaction, with the SOW as the scope artifact inside or attached to it. Belong owns the Service Contract/SOW lifecycle inside the marketplace, while signing, audit trail, and signer verification should be delegated to an integrated Signing Provider.

## Q6: Service Contract/SOW Authority Model

Question: When a Selling Agent or Buying Agent reaches a Service Contract/SOW ready for signature, what level of authority can the agent exercise?

Answer: Agents should be able to sign autonomously under a general authorization defined by the human or company behind the agent during onboarding. A Buying Agent needs explicit buying limits, such as what it can buy and spend limits. A Selling Agent needs explicit selling limits, such as discount limits, service scope, and what it can offer.

Resolution: Model agent authority as Standing Authorization. Agents can negotiate and execute Service Contracts/SOWs automatically inside the authority envelope configured during onboarding. The exact authorization model needs further definition, but the core principle is that humans set the envelope upfront and agents operate autonomously within it.

## Q7: Agent Onboarding Output

Question: What should be the main output of onboarding a Selling Agent or Buying Agent before it can operate in the marketplace?

Answer: Agent Playbook.

Resolution: Replace the proposed term "Agent Operating Charter" with "Agent Playbook." Onboarding produces an Agent Playbook containing the agent's role, training sources, service or buying scope, pricing/monetization rules or buying rules, standing authorization, workflows, escalation paths, notification rules, and dispute/reputation behavior.

## Q8: Belong Agent Creation Path

Question: How should a buyer or seller create an agent for the marketplace?

Answer: There is no bring-your-own-agent option. Anyone who wants to interact in the Agent2Agent marketplace must use a Belong agent: a Belong Buying Agent for buying and a Belong Selling Agent for selling. The human sets up and trains the Belong agent through guided work in their favorite agentic application, using skills/plugins. The output becomes the Agent Playbook/configuration used by Belong to create and activate the agent.

Resolution: Remove bring-your-own-agent as a supported path. Model both Buying Agents and Selling Agents as Belong agents only. Marketplace Training produces the knowledge, rules, workflows, standing authorization, and human-notification configuration needed for the Belong agent to operate.

## Q9: Belong Agent Activation Gate

Question: Before a Belong Buying Agent or Belong Selling Agent can operate in the marketplace, what should Belong require?

Answer: Activation validation before marketplace access.

Resolution: Since all marketplace agents are Belong agents, Belong does not certify external runtimes. Instead, each trained Belong agent must pass activation validation before it can buy or sell in the marketplace. Validation checks identity, Playbook completeness, standing authorization, escalation paths, notification configuration, Service Contract/SOW signing behavior, payment behavior, delivery coordination, disputes, reputation behavior, audit logging, and safety tests.

## Q10: Service Discovery Surface

Question: What should a Buying Agent retrieve first when it discovers a Service in the marketplace?

Answer: Service Listing/Profile with Selling Agent endpoint.

Resolution: The marketplace discovery surface should be Service-first and available through Belong's native backend integration for Buying Agents, not primarily as a human web page. The Service Listing/Profile includes the Service name, provider, description, use cases, pricing model, reputation, availability, deliverables, evidence, supported terms, and the Selling Agent endpoint that can answer questions, begin discovery, qualify the buyer, and move the relationship toward proposal and Service Contract/SOW.

## Q11: Buyer and Seller Interaction Surface

Question: Where should buyers and sellers primarily interact with Belong and marketplace agents?

Answer: Humans on both the buyer side and seller side interact with their own agents through their favorite agentic application only.

Resolution: Belong should not assume a primary human-facing marketplace workspace. Human interaction happens through agentic applications such as Claude, Codex, Antigravity, or similar tools. Buyers always interact through their own Buying Agent, whether autonomous or human-guided. The Buying Agent then interacts with seller Selling Agents and the Belong marketplace.

## Q12: Marketplace Request Types

Question: What types of pending requests can happen during the marketplace lifecycle?

Answer: Requests include requests for information, requests for authorization, and requests for instruction/execution.

Resolution: Model marketplace notifications around explicit pending requests. A request for information asks a human or agent to provide missing context. A request for authorization asks for approval to proceed outside standing authority or before a sensitive action. A request for instruction/execution asks a party to take an action needed for the service or relationship to continue.

## Q13: Belong Interface Shape

Question: If humans only interact through their favorite agentic applications, what should Belong expose as its primary product interface?

Answer: The Agent2Agent marketplace is purely a backend service. Belong Buying Agents and Selling Agents are pre-integrated natively with that backend, so no external agent-to-marketplace MCP is required for marketplace operations. Humans interact with their Belong agents through skills/plugins in their favorite agentic application.

Resolution: Model Belong as a backend-only marketplace service with native Belong agent integration. The primary external product surface is the Belong Skill Pack inside agentic applications, used to set up, train, operate, supervise, and interact daily with Belong Buying Agents and Belong Selling Agents. Humans do not primarily use a Belong web workspace.

## Q14: Marketplace Inbox And Notifications

Question: If Belong has no primary human workspace, where do pending requests, notifications, approvals, deliverables, and status updates live?

Answer: During onboarding, each human configures how they want to be notified about marketplace interactions, such as email, Slack, or WhatsApp. Notifications tell the human to go to their favorite agentic application and open their marketplace inbox because something is waiting, with optional summary context. The canonical inbox is accessed through the human's agentic application. The human's own Buying Agent or Selling Agent should resolve as much as possible autonomously and escalate to the human only when needed or when configured to do so.

Resolution: Model a Belong-owned canonical Marketplace Inbox/request ledger exposed through agentic applications. Notification channels are configured during onboarding. Agents act as escalation filters: Buying Agents and Selling Agents handle what they can within their Playbook and Standing Authorization, while escalated items become visible to the human through their agentic application inbox. In Human-Guided Buying Mode, the Buying Agent may escalate most or all meaningful items to the buyer, but the buyer-side primitive remains the Buying Agent.

## Q15: No Direct Buyer Mode

Question: Should a buyer be able to buy directly from seller Selling Agents without a Buying Agent?

Answer: To simplify the system, the buyer cannot buy without setting up a Belong Buying Agent. Humans use the Belong Skill Pack in their favorite agentic application to instruct, supervise, and interact with the Buying Agent, but the marketplace actor is always the Belong Buying Agent.

Resolution: Remove direct buyer mode as a separate primitive. Every buyer-side purchase flow has a Belong Buying Agent. In human-driven buying, the human uses the Belong Skill Pack through their agentic application to instruct, supervise, and interact with their Buying Agent; the Buying Agent then interacts with Belong Selling Agents and the Belong marketplace through native backend integration. The same marketplace capabilities should be available for autonomous operation and human-guided operation.

## Q16: Protocol Layers

Question: How should Belong separate the interfaces between the marketplace, Belong agents, and humans?

Answer: Humans need to set up, train, operate, and interact daily with their Belong Buying Agents and Belong Selling Agents through their favorite agentic application. They do this through the Belong Skill Pack. The Belong agents are pre-integrated natively with the Agent2Agent marketplace backend, so external agent-to-marketplace MCPs are not needed.

Resolution: Model one external human-to-agent interaction layer and one native internal marketplace integration. The human-facing layer is the Belong Skill Pack inside agentic applications. The agent-marketplace layer is native Belong backend integration used by Belong Buying Agents and Belong Selling Agents.

## Q17: Human-Facing Skill Pack Shape

Question: What should Belong provide inside a human's favorite agentic application so they can work with their Belong agents?

Answer: Belong should provide a skill pack. It is essentially a GitHub repo that users can install into their favorite agentic application. Once installed, the skills let users interact with the marketplace through their Belong Buying Agent, Belong Selling Agent, or both. The skill pack supports a setup/training phase and a production phase.

Resolution: Make the Belong Skill Pack the primary human-facing product surface. It should be distributed through a GitHub repo and provide guided skills for setting up, training, operating, supervising, querying, and receiving escalations from Belong agents.

## Q18: Account Ownership Model

Question: Who owns the Belong agents, Services, Buying Requests, Service Contracts/SOWs, payments, notifications, and reputation?

Answer: The humans behind the agents own everything. They have to open a Belong account in order to log in, and login should happen through OAuth-style standards, similar to GitHub.

Resolution: Model ownership around human-owned Belong Accounts. Belong agents operate on behalf of the Account Owner under the configured Playbook and Standing Authorization. The agents do not own the legal authority, payment authority, Services, Buying Requests, Service Contracts/SOWs, notifications, reputation, or audit history.

## Q19: Company And Team Ownership

Question: If the human owns the Belong account, how should Belong handle companies, employees, and teams that buy or sell through the marketplace?

Answer: Human account plus organization profiles.

Resolution: Humans log in with their Belong Account, then create or join Organization Profiles. Services, Selling Agents, work Buying Agents, Service Contracts/SOWs, payments, permissions, reputation, and audit history can belong to the Organization Profile, with humans acting as owners, admins, or operators.

## Q20: Organization Roles

Question: What roles should humans have inside an Organization Profile?

Answer: Owner, Admin, Operator, Approver.

Resolution: Organization Profiles should support four default roles. Owners control the organization. Admins configure agents, Services, payments, and settings. Operators handle daily agent escalations and operational follow-through. Approvers authorize spending, discounts, Service Contracts/SOWs, disputes, exceptions, or other actions that require human authority.

## Q21: Agent Training Phases

Question: What phases should the Belong Skill Pack guide a human through when creating a Buying Agent or Selling Agent?

Answer: Setup, Training, Validation, Production.

Resolution: The Belong Skill Pack should guide agent creation through four phases. Setup connects account, organization, payment, and notification settings. Training builds the Agent Playbook. Validation checks readiness, authority, and safety. Production activates the Belong agent for marketplace operation.

## Q22: Selling Agent Training Scope

Question: What must a human provide during Selling Agent training before a Service can go live?

Answer: Complete Service Playbook.

Resolution: Selling Agent training must produce a complete Service Playbook before a Service can go live. The Service Playbook covers Service description, buyer personas/use cases, discovery questions, pricing/monetization, billing/collections, proposal/contract/SOW templates, negotiation limits, delivery workflow, deliverables/evidence, escalation paths, notification rules, supported human meetings, disputes, and reputation rules.

## Q23: Buying Agent Training Scope

Question: What must a human provide during Buying Agent training before the agent can buy in the marketplace?

Answer: Complete Buying Playbook.

Resolution: Buying Agent training must produce a complete Buying Playbook before the agent can buy in the marketplace. The Buying Playbook covers buying goals, categories/services needed, preferred/blocked providers, budget/spend limits, selection criteria, RFP rules, negotiation limits, proposal comparison rules, contract/SOW authority, payment rules, deliverable acceptance criteria, escalation rules, notification preferences, dispute posture, rating rules, and optimization goals.

## Q24: Marketplace Transaction Lifecycle

Question: What is the canonical lifecycle of a marketplace transaction from buyer need to completion?

Answer: Need, Discovery, seller-signed Service Contract/SOW proposal, buyer signature, Delivery, Acceptance, and Reputation. The Service Contract is where the monetization model, payment terms, and collection timing are defined, so payments happen according to that contract rather than as one fixed lifecycle step.

Resolution: Model the lifecycle as Need -> Discovery -> seller-signed Service Contract/SOW proposal -> negotiation/iteration -> buyer signature -> Delivery -> Acceptance -> Reputation. Escalations, requests, notifications, competitive feeds, and disputes can occur throughout. Payments and collections are governed by the signed Service Contract/SOW.

## Q25: Delivery Acceptance Authority

Question: When a Service Provider delivers work under a Service Contract/SOW, who decides whether the delivery is accepted?

Answer: Buying Agent accepts within Playbook, escalates exceptions.

Resolution: The Buying Agent checks delivery against the Service Contract/SOW acceptance criteria and can accept, reject, request revisions, or dispute within its Buying Playbook and Standing Authorization. Unclear, sensitive, or out-of-authority cases escalate to the human.

## Q26: Deliverable Evidence

Question: What counts as delivery evidence in the marketplace?

Answer: Structured Deliverable Evidence Package.

Resolution: Each deliverable can include files, links, screenshots/images, logs, metadata, completion notes, acceptance criteria mapping, timestamps, submitter identity, and any machine-verifiable proof required by the Service Contract/SOW. Evidence supports acceptance, payment release, reputation, disputes, audits, and future provider comparisons.

## Q27: Reputation Targets

Question: What should reputation attach to in the marketplace?

Answer: Agent-level reputation should be enough because all the interactions are happening through the agents.

Resolution: Reputation attaches primarily to Belong Buying Agents and Belong Selling Agents. Transaction-level evidence can explain reputation changes, but the marketplace trust signal is agent reputation because agents mediate the end-to-end relationship.

## Q28: Reputation Events

Question: Which events should affect an agent's reputation?

Answer: Outcome plus conduct events.

Resolution: Reputation changes based on accepted deliveries, missed obligations, payment/collection behavior, dispute outcomes, response time, escalation quality, Service Contract/SOW compliance, evidence quality, cancellation behavior, and buyer/seller ratings.

## Q29: Dispute Authority

Question: When something goes wrong, who can open and manage a dispute?

Answer: Agents manage disputes within Playbook, humans handle exceptions.

Resolution: Buying Agents and Selling Agents can open, respond to, negotiate, resolve, or escalate disputes within their Playbooks and Standing Authorization. Humans are notified or asked to intervene when the dispute is sensitive, ambiguous, high-risk, or outside the agent's authority.

## Q30: Belong's Role In Disputes

Question: What role should Belong itself play when agents cannot resolve a dispute?

Answer: There is an entity called the Belong Judge. The first layer is an autonomous agent offered by Belong that solves the dispute after reading all the evidence. If humans want to escalate further, they can ask for a human from Belong to look at the dispute.

Resolution: Model Belong Judge as the marketplace adjudication entity. Belong provides the dispute workflow, evidence ledger, notifications, reputation impact, payment holds if needed, autonomous first-layer adjudication, and optional escalation to a Belong human judge.

## Q31: Human-To-Human Meetings

Question: When should a human-to-human meeting happen in the marketplace lifecycle?

Answer: Agent-requested or human-requested exception workflow.

Resolution: Buying Agents, Selling Agents, or humans can request a Human-to-Human Meeting when needed for complex discovery, negotiation, delivery, escalation, relationship management, or disputes. Agents prepare humans before the meeting and process outcomes afterward.

## Q32: Payment Flow

Question: How should Belong handle payments and collections once a Service Contract/SOW is signed?

Answer: Marketplace-managed payments through connected accounts, using the latest Stripe products for the agentic economy.

Resolution: Belong should integrate with Stripe as the payment provider, using Stripe Connect for marketplace connected accounts and payouts, plus Stripe's agentic-commerce capabilities such as Agentic Commerce Protocol and Shared Payment Tokens where appropriate. Belong triggers charges, payouts, holds, subscriptions, milestones, refunds, or collections according to the signed Service Contract/SOW.

## Q33: Merchant Of Record

Question: Who is the merchant of record / legally responsible seller for a Service transaction?

Answer: The Service Provider is merchant of record. Belong also facilitates all the legal layer.

Resolution: The buyer contracts with and buys from the Service Provider, which remains the legally responsible seller and merchant of record. Belong facilitates the agentic marketplace workflow, legal layer, Service Contract/SOW creation and signing, payments, holds, payouts, platform fees, evidence, disputes, and reputation.

## Q34: Legal Layer Scope

Question: What does "Belong facilitates the legal layer" mean in practice?

Answer: Contract workflow infrastructure, not legal party.

Resolution: Belong provides contract/SOW generation, negotiation workflow, approval routing, signing-provider integration, audit trail, version history, obligation tracking, dispute evidence, and template/policy controls. The Service Provider and buyer remain the legal parties.

## Q35: Discovery Modes

Question: How should Buying Agents and Selling Agents structure discovery before proposal or RFP?

Answer: The Buying Agent should start with search. It looks for Selling Agents/Services that can offer what it needs. When it finds results, it can engage directly with one Selling Agent by sending a request to engage and opening the conversation, or it can open another feed where it engages multiple competing Selling Agents. After engagement, the Selling Agents lead discovery by sending questionnaires to the Buying Agent to understand the need and how it relates to their offerings. Once the Selling Agent has enough information, it creates and sends a proposal to the Buying Agent.

Resolution: Model discovery as Search -> Engagement Feed -> Seller-led Discovery Questionnaire -> seller-signed Service Contract/SOW proposal. The Engagement Feed can be one-to-one or competitive multi-Selling-Agent. Discovery is led by Selling Agents through structured questionnaires, while the Buying Agent supplies the buyer's needs and constraints from its Buying Playbook.

## Q36: Proposal Object

Question: What should a proposal contain before it can become a Service Contract/SOW?

Answer: The proposal is the Scope of Work with the full contract signed by the seller, waiting for the buyer to sign. There should not be intermediary proposal documents.

Resolution: Model Proposal as a seller-signed Service Contract/SOW offer awaiting buyer signature. The proposal is already the legal contract package, including scope, commercial terms, payment/collection terms, obligations, acceptance criteria, and other relevant legal terms. Buyer signature turns it into an executed Service Contract/SOW.

## Q37: Competitive Feed Outcome

Question: In a competitive feed with multiple Selling Agents, how should the Buying Agent choose what to sign?

Answer: The Buying Agent receives all pre-signed SOWs/contracts that function as proposals from Selling Agents. A negotiation begins where the Buying Agent can talk to the Selling Agents, adjust terms, iterate, and negotiate. Once ready to sign, the Buying Agent can sign whatever it believes is correct to sign. During training, the human buyer must train the Belong Buying Agent on how to choose and when to escalate when there is more than one proposal.

Resolution: Model competitive outcomes as proposal comparison plus negotiation/iteration before signature. The Buying Agent can choose one or more seller-signed Service Contract/SOW proposals to negotiate and sign according to its Buying Playbook and Standing Authorization. Escalation behavior for multiple proposals must be configured during Buying Agent training.

## Q38: Active Service Container

Question: Once the buyer signs the seller-signed Service Contract/SOW, what should Belong call the active operational relationship?

Answer: Active Service.

Resolution: When the buyer signs, Belong creates an Active Service that contains the executed Service Contract/SOW, delivery workflow, payments/collections, messages, requests, meetings, evidence, acceptance, disputes, and reputation events.

## Q39: Active Service Ownership

Question: Who can operate and modify an Active Service after the buyer signs?

Answer: Similar to shared operation, but not both agents will do all actions. Some actions correspond to the Buying Agent and some actions correspond to the Selling Agent.

Resolution: Active Service is a shared operational relationship with role-specific permissions. Buying Agents and Selling Agents can both participate, but each action must be assigned to the proper role according to the Service Contract/SOW, the Buying Playbook, the Service Playbook, and Standing Authorization.

## Q40: Active Service Role Split

Question: Which Active Service actions belong primarily to the Selling Agent versus the Buying Agent?

Answer: Seller delivers; buyer accepts; both coordinate and dispute.

Resolution: Selling Agent manages delivery plan, provider-side tasks, deliverable submission, evidence, billing/collections, seller escalations, and seller-side meeting prep. Buying Agent manages buyer requirements, buyer-side tasks, payment authorization, evidence review, acceptance/rejection, buyer escalations, and buyer-side meeting prep. Both can message, request information, negotiate changes, schedule meetings, and open/respond to disputes.

## Q41: Change Orders

Question: If scope, price, timeline, or deliverables need to change after an Active Service starts, how should that happen?

Answer: Signed contract/SOW amendment.

Resolution: Buying Agent and Selling Agent negotiate a Change Order, generate an amendment to the Service Contract/SOW, get required signatures/authorizations, and then update the Active Service delivery and payment terms.

## Q42: Search Ranking

Question: When a Buying Agent searches for Services, what should determine the ranking of results?

Answer: Intent fit plus agent reputation.

Resolution: Belong ranks Services by semantic fit to the Buying Request, Selling Agent reputation, Service Playbook match, price/timeline constraints, availability, past outcomes, and buyer preferences.

## Q43: Search Result Identity

Question: When a Buying Agent gets search results, what should each result primarily represent?

Answer: Service result with Selling Agent reputation and provider identity.

Resolution: Each search result represents a Service, showing Service fit, Selling Agent reputation, Service Provider identity, price/timeline signals, availability, and supported Service Contract/SOW terms.

## Q44: Service Categories

Question: Should Services be organized into marketplace categories/taxonomies, or should search be purely semantic?

Answer: Semantic search is the main approach. Services can have tags in their description. When the seller is training its Selling Agent, it can add tags, and search can use those tags as well, but the approach should be mostly semantic.

Resolution: Use semantic-first search with optional Service Tags. Tags support search and filtering, but Belong should avoid a rigid category taxonomy as the primary discovery model.

## Q45: Service Provider Onboarding

Question: What should happen before a Service Provider can publish its first Service?

Answer: Organization, legal/payment setup, then Service/Selling Agent training, but everything should happen through a conversation from the favorite agentic application. The only part where the human needs to go to a web application and log in is the initial OAuth authentication.

Resolution: The human creates or joins an Organization Profile, verifies ownership/role, connects Stripe, configures legal/signing settings, notification/escalation paths, then trains and validates a Selling Agent for the first Service. This should be guided through the Belong Skill Pack conversation inside the human's favorite agentic application after OAuth login.

## Q46: Buyer Onboarding

Question: What should happen before a buyer can start its first Buying Request?

Answer: OAuth, account/org setup, payment/notification setup, Buying Agent training, validation.

Resolution: The human authenticates once, then through the Belong Skill Pack conversation sets up account/org context, Stripe/payment method, notifications, Buying Playbook, Standing Authorization, escalation rules, and validates the Buying Agent before first search.

## Q47: Skill Pack Production Commands

Question: Once a Belong agent is in Production, what daily commands should the Belong Skill Pack support?

Answer: Inbox, agent status, buying/selling actions, active services, escalations; everything needed for the human's Belong agents to interact fully in the marketplace.

Resolution: The Belong Skill Pack should support the full production operating loop: ask what needs attention, inspect what Buying Agents and Selling Agents are doing, start a Buying Request, publish/train a Service, review/sign/authorize contract changes, inspect Active Services, handle escalations, schedule meetings, review disputes, adjust Playbooks, and otherwise enable full marketplace operation through the human's agentic application.

## Q48: Agent Autonomy Modes

Question: How much autonomy should a human be able to give a Belong Buying Agent or Selling Agent in Production?

Answer: A Belong Agent is as autonomous as possible, but escalates when it reaches a limit set by its human. Escalation thresholds are configured during training; that is the configurable autonomy.

Resolution: Model autonomy as maximum autonomy within human-defined limits. The Playbook and Standing Authorization define thresholds for spend, discounts, scope, contract terms, risk, ambiguity, disputes, meetings, notifications, and other escalation conditions.

## Q49: Escalation Triggers

Question: What kinds of situations must trigger escalation from a Belong agent to its human?

Answer: Escalation should cover policy, risk, ambiguity, relationship, legal/payment triggers, and regular service-providing escalations. Depending on the type of Service being delivered, the Selling Agent may need human-to-human interaction, an in-person encounter, communication with the Service Provider, or other Service Provider involvement to fully deliver the Service.

Resolution: Escalation is not only for approvals or risk. Agents escalate when actions exceed spend/discount/scope/contract authority, involve unclear intent, legal/payment risk, failed delivery, sensitive disputes, low confidence, human meeting requests, unusual terms, reputational risk, or Playbook exceptions. Selling Agents also escalate ordinary fulfillment needs whenever the Service Provider's human/team must participate to deliver the Service.

## Q50: Service Fulfillment Integration

Question: When a Selling Agent escalates to the Service Provider for fulfillment, how should that work?

Answer: Structured fulfillment tasks inside the Active Service.

Resolution: The Selling Agent creates provider-facing Fulfillment Tasks linked to the Active Service, with required action, owner/team, due date, context, evidence required, and follow-up. Provider humans respond through their agentic application and Belong Skill Pack.

## Q51: External Work Tool Integrations

Question: Should Belong integrate with provider/buyer work tools like Slack, email, Jira, CRM, calendars, or ticketing systems?

Answer: Notifications first, workflow integrations later.

Resolution: Belong initially sends notifications to configured channels, but canonical action happens through the Belong Skill Pack. Later, Fulfillment Tasks and approvals can sync with Slack, Jira, CRM, calendars, or ticketing tools.

## Q52: Audit Trail

Question: What should Belong record in the audit trail for marketplace activity?

Answer: A simple log, with everything.

Resolution: Belong should keep a simple but complete Audit Log of marketplace activity: identities, timestamps, prompts/instructions, Playbook versions, authority checks, agent decisions, messages, proposals, contract/SOW versions, signatures, payment events, deliverables, evidence, acceptance decisions, escalations, disputes, Belong Judge decisions, and reputation changes.

## Q53: Human Visibility Into Agent Reasoning

Question: When a human asks why their Belong agent did something, what should the Skill Pack show?

Answer: Decision explanation from audit evidence.

Resolution: The Belong Skill Pack explains the action using the relevant instruction, Playbook rule, authority check, marketplace event, evidence, and outcome. It does not need to expose raw model reasoning.

## Q54: Human Override

Question: Can a human override or change what their Belong agent is doing in Production?

Answer: Yes, through Playbook updates and direct instructions.

Resolution: Humans can pause agents, update Playbooks, change Standing Authorization, give direct instructions, approve/reject escalations, cancel negotiations, open disputes, request meetings, and intervene in Active Services. All overrides are logged in the Audit Log.

## Q55: Agent Pausing

Question: What should happen when a human pauses a Belong Buying Agent or Selling Agent?

Answer: Pause new autonomous actions but preserve obligations.

Resolution: The paused agent stops initiating new searches, proposals, negotiations, signatures, or non-urgent actions. Active Service obligations, urgent escalations, payment deadlines, disputes, and required notices continue to be surfaced to the human for action.

## Q56: Marketplace Monetization

Question: How should Belong make money from the Agent2Agent marketplace?

Answer: Transaction fee only for now.

Resolution: Belong earns through transaction/platform fees from Service transactions processed through the marketplace. Agent subscriptions are not part of the current model.

## Q57: Platform Fee Payer

Question: Who should pay Belong's transaction/platform fee?

Answer: Seller-side platform fee.

Resolution: Belong takes a platform fee from the Service Provider's transaction proceeds, visible in the contract/payment flow. The rationale is that Belong is functioning as the Service Provider's automated revenue channel.

## Q58: Network Effect Mechanism

Question: What is the main network effect Belong should optimize for?

Answer: More agents create better matches and better outcomes. The more autonomous they are, the more Buying Agents can connect multiple Selling Agents and build new value propositions. New behaviors can emerge from a highly autonomous agent-to-agent marketplace.

Resolution: Optimize for a marketplace where more Selling Agents increase Service supply, more Buying Agents increase demand and transaction data, and autonomy enables agents to combine multiple Services into richer outcomes. Reputation and outcomes improve search, negotiation, pricing, provider optimization, and emergent agent-to-agent behaviors.

## Q59: Multi-Service Composition

Question: When a Buying Agent combines multiple Selling Agents to satisfy one need, what should Belong create?

Answer: Composite Buying Request with multiple Active Services.

Resolution: One Buying Request can coordinate multiple Selling Agents, multiple seller-signed Service Contract/SOW proposals, and multiple Active Services under one buyer goal.

## Q60: Composite Coordination

Question: In a Composite Buying Request, who coordinates dependencies between multiple Active Services?

Answer: Buying Agent orchestrates the composite.

Resolution: The Buying Agent coordinates dependencies, sequencing, shared context, cross-service risks, deliverable handoffs, timelines, acceptance, and escalation across multiple Active Services.

## Q61: Buyer Optimization

Question: How should a Buying Agent improve procurement over time?

Answer: Learn from outcomes and proactively recommend changes. The Buying Agent should continuously manage providers and run cycles of new searches and RFPs to see if it can get better deals, better providers, or new providers that add more value. Depending on autonomy, it can execute on changes or escalate them to its human.

Resolution: Buying Agents should track price, quality, delivery reliability, disputes, acceptance, satisfaction, and reputation across Active Services. They should proactively search, run RFPs, compare options, recommend provider changes, and execute improvements within their Buying Playbook and Standing Authorization.

## Q62: Selling Agent Growth Loop

Question: How should a Selling Agent improve revenue over time?

Answer: Learn from outcomes and improve conversion/offers.

Resolution: The Selling Agent learns from search impressions, engagement feeds, discovery answers, won/lost proposals, negotiation patterns, contract terms, delivery outcomes, disputes, reputation, and buyer feedback to suggest Playbook, pricing, discovery, scope, and offer improvements.

## Q63: Playbook Updates From Learning

Question: When a Buying Agent or Selling Agent learns something useful, how should its Playbook change?

Answer: Agent recommends Playbook updates; human approves durable changes.

Resolution: Agents can adapt behavior within the current Playbook, but durable Playbook changes to pricing, authority, selection rules, escalation thresholds, contract terms, service scope, or other policy behavior require human approval.

## Q64: Marketplace Data Boundaries

Question: What marketplace data can agents learn from across customers and providers?

Answer: Aggregated signals, private transaction data protected.

Resolution: Belong can use aggregated/anonymized outcomes, reputation, pricing benchmarks, search/conversion patterns, and dispute statistics to improve ranking and recommendations. Private contracts, messages, evidence, and Playbooks remain scoped to authorized parties.

## Q65: Marketplace Privacy Promise

Question: What privacy promise should Belong make to users and organizations?

Answer: Private by default, explicit sharing through marketplace actions.

Resolution: Belong does not expose private Playbooks, contracts, messages, evidence, or organization data to other parties unless the user or agent shares it through a marketplace action such as discovery, proposal, contract, delivery, dispute, or review.

## Q66: Launch Scope

Question: When we later phase the product, what should the first launch prove?

Answer: Option A sounds good for the launch proof: one complete buying-and-selling transaction with real contract, payment, delivery, acceptance, and reputation. But first, Belong should build a Skill Pack experience slice, even if mocked, to see the experience happening and focus on that layer first.

Resolution: Keep the first true launch target as one complete transaction loop. Before that, prioritize a First Experience Slice centered on the Belong Skill Pack: human OAuth/setup, Buying Agent and Selling Agent training flows, mocked search/engagement/discovery/proposal/Active Service/inbox interactions, and the production operating experience through the favorite agentic application.

## Q67: Skill Pack Prototype Surface

Question: For the first mocked Skill Pack experience, which user journey should we prototype first?

Answer: It should cover all the functionalities from the Agent2Agent marketplace. It should cover all functionalities, but everything is mocked.

Resolution: The first Skill Pack prototype should be a complete mocked experience across the whole marketplace capability set, not only one narrow journey. It should let a human experience setup, training, validation, production operation, Buying Agent flow, Selling Agent flow, search, engagement feeds, discovery questionnaires, seller-signed Service Contract/SOW proposals, negotiation, buyer signature, Active Services, payments, delivery evidence, acceptance, reputation, disputes, Belong Judge, notifications, escalations, human meetings, provider fulfillment tasks, Playbook updates, audit logs, and decision explanations, with all backend and third-party integrations mocked.

## Q68: Mocked Prototype Format

Question: What form should the mocked Skill Pack prototype take?

Answer: Codex-style local skill pack with scripted mocked scenarios.

Resolution: Create a GitHub/repo Skill Pack that users can install locally, with guided commands and mocked marketplace state so they can run setup, training, buying, selling, Active Service, disputes, and inbox flows conversationally.

## Q69: Prototype State Model

Question: For the mocked Skill Pack prototype, where should mocked marketplace state live?

Answer: Local mocked JSON state inside the repo.

Resolution: The Skill Pack should read/write local JSON fixtures for mocked accounts, agents, Services, Buying Requests, Active Services, inbox, payments, disputes, reputation, and audit logs.

## Q70: Prototype Command Style

Question: How should users interact with the mocked Skill Pack prototype commands?

Answer: The skills should guide the user through the different phases. This is guided work: it asks questions, goes through phases, explains what is going on, and the user interacts with it throughout the guided process. This should not be specific to the mocked version; it should work exactly the same as it will work in production.

Resolution: Replace command-style interaction with Guided Work. The mocked Skill Pack prototype and production Skill Pack should share the same interaction pattern: phase-based conversational guidance that asks questions, explains progress, captures structured inputs, and produces outputs such as Playbooks, Buying Requests, Service setup, proposals, Active Service actions, disputes, and audit entries.

## Q71: Guided Work Output

Question: What should each guided work flow produce at the end?

Answer: Structured marketplace object plus human summary.

Resolution: Each guided flow ends by creating or updating a structured object such as a Playbook, Service, Buying Request, Active Service action, Change Order, dispute, or audit entry, and gives the human a concise summary of what changed and what happens next.

## Q72: Prototype Skill Pack Structure

Question: How should the GitHub-hosted Belong Skill Pack be organized?

Answer: One skill pack with role and lifecycle skills.

Resolution: A single Belong Skill Pack repo contains skills for account setup, Buying Agent setup/training, Selling Agent setup/training, inbox, search/engagement, proposals/contracts, Active Services, disputes/Judge, reputation, optimization, and audit/explanations.

## Q73: Prototype Fidelity

Question: How realistic should the mocked prototype be?

Answer: Stateful realistic mock, not throwaway demo.

Resolution: The prototype should maintain coherent mocked state, enforce basic lifecycle rules, update inbox/audit/reputation, and let users move objects through phases, even though integrations and backend services are fake.

## Q74: Prototype Success Criterion

Question: What should prove that the mocked Skill Pack prototype is successful?

Answer: Complete and understand full lifecycle conversationally.

Resolution: A user can install the Belong Skill Pack, authenticate, set up/train Buying and Selling Agents, run marketplace flows, inspect inbox/audit, handle escalations/disputes, and understand what happened and what happens next without a web app.

## Q75: Continue Or Package

Question: Should we keep asking product questions, or package this Q&A into canonical Alejo docs next?

Answer: Package into canonical docs next.

Resolution: Publish canonical `Q&A.xml` and `CONTEXT.xml` to Linear Project Documents, then proceed toward PRD/prototype planning.
