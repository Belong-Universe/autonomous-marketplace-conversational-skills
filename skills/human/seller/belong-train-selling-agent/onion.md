The Onion Method

 1.⁠ ⁠Definition

The Onion Method is an AI-native software development method for building a new service from the outside in.

It starts by defining the target audience and value proposition, then designs the complete human, agentic, and system experience. From there, it builds a fully experiential outer layer, de-risks the technology, and then implements the product feature set by feature set, layer by layer, until the system reaches its core.

The method is designed for new services in a services or microservices architecture. It is not the default method for modifying an existing service.

---

 2.⁠ ⁠Core Principles

2.1 Build from the outside in

The Onion Method starts with what the human experiences and progressively moves inward toward the real logic, reasoning, integrations, data, and core processes that power the product.

2.2 The first layer is experiential

The first built layer is the fully experiential prototype. It should feel functional to the human, even if the internal system is still simulated.

2.3 Features are the unit of implementation

The experience is mapped into features from the beginning. Implementation happens by selecting coherent feature sets and building them inward through the required layers.

2.4 Layers are product-specific

There is no fixed number of layers. The layers are derived from the product’s humans, agents, systems, and sequence diagrams.

A product may need a simple structure:

Experience → Logic → Core Data

Or a more complex structure:

Experience → Agent Reasoning → Workflow Orchestration → Integrations → Core Data

The method does not prescribe the layers. It discovers them through design.

2.5 Humans, agents, and systems must be modeled together

The product is not only a user interface. It may involve human touchpoints, agents, MCPs, APIs, backends, databases, queues, external providers, and other systems.

The method requires that these actors be modeled explicitly.

2.6 Secrets must be handled safely

Raw secrets must never be shared with an LLM, written into methodology files, or exposed in issues, prompts, logs, or documentation.

Only secret names, purposes, owners, environments, and secure references may be documented.

---

 3.⁠ ⁠Step 0 — New Service Decision

Before applying The Onion Method, determine whether the work is a new service or a modification of an existing service.

The Onion Method applies when:

•⁠  ⁠A new service is being created.
•⁠  ⁠The architecture supports a services or microservices approach.
•⁠  ⁠The service can be built end-to-end with reasonable independence.
•⁠  ⁠The work is not merely editing, refactoring, or extending an existing service.

If the work is about modifying an existing service, a different process should be used.

Output

"build-mode-decision.md"

This file should state:

•⁠  ⁠Whether The Onion Method applies
•⁠  ⁠Why it applies or does not apply
•⁠  ⁠Whether the target architecture supports the method
•⁠  ⁠Any assumptions or constraints

---

 4.⁠ ⁠Step 1 — Constitution

The Constitution is the strategic anchor of the product.

It contains only two things:

4.1 Target Audience / User Personas

Who is this product for?

This may include:

•⁠  ⁠End users
•⁠  ⁠Buyers
•⁠  ⁠Operators
•⁠  ⁠Admins
•⁠  ⁠Developers
•⁠  ⁠Agent users
•⁠  ⁠Customer segments
•⁠  ⁠Context of use

4.2 Value Proposition

What value does the product create for them?

This should clarify:

•⁠  ⁠Pain solved
•⁠  ⁠Outcome created
•⁠  ⁠Reason to adopt
•⁠  ⁠Why the product should exist

Nothing else belongs in the Constitution.

No technical architecture.
No user stories.
No implementation notes.
No scope details.
No product principles.

Output

"constitution.md"

Containing only:

•⁠  ⁠Target audience / user personas
•⁠  ⁠Value proposition

---

 5.⁠ ⁠Step 2 — Experience & Solution Design Document

Step 2 creates the compact master design document for the product experience and high-level solution behavior.

This replaces the traditional PRD.

The document should define:

 1.⁠ ⁠How the human experiences the product
 2.⁠ ⁠Which humans, agents, and systems participate
 3.⁠ ⁠Which features exist
 4.⁠ ⁠How the actors interact through complete sequence diagrams
 5.⁠ ⁠What product layers are likely required

Output

"experience-solution-design.md"

This file should include the following sections.

---

5.1 Experience Platforms

Define where the human will experience the product.

Possible platforms include:

•⁠  ⁠Browser
•⁠  ⁠Web application
•⁠  ⁠Mobile application
•⁠  ⁠Desktop application
•⁠  ⁠Agentic application, such as Claude, Codex, ChatGPT, Cursor, or similar
•⁠  ⁠CLI
•⁠  ⁠MCP
•⁠  ⁠Skill pack
•⁠  ⁠Plugin
•⁠  ⁠Public API documentation
•⁠  ⁠Developer sandbox
•⁠  ⁠SDK documentation
•⁠  ⁠Integration surface

The core question is:

«How will the human live through the product experience?»

Even when the product is technically consumed by agents, APIs, CLIs, MCPs, or systems, the method still asks how the human experiences, understands, invokes, supervises, integrates, or trusts it.

---

5.2 Actor Map: Humans, Agents, and Systems

The document must classify every actor into one of three categories.

Humans

People who experience, operate, configure, supervise, approve, or consume the product.

Examples:

•⁠  ⁠End user
•⁠  ⁠Admin
•⁠  ⁠Operator
•⁠  ⁠Analyst
•⁠  ⁠Developer
•⁠  ⁠Approver
•⁠  ⁠Customer support user
•⁠  ⁠Buyer or evaluator

Agents

AI-native actors that reason, execute, coordinate, assist, review, or automate work.

Examples:

•⁠  ⁠User-facing agent
•⁠  ⁠Workflow agent
•⁠  ⁠Data analysis agent
•⁠  ⁠Planning agent
•⁠  ⁠Review agent
•⁠  ⁠Integration agent
•⁠  ⁠MCP tool-using agent
•⁠  ⁠Background automation agent

Systems

Non-agentic software components, services, APIs, databases, and infrastructure.

Examples:

•⁠  ⁠Web app
•⁠  ⁠Backend service
•⁠  ⁠API
•⁠  ⁠Database
•⁠  ⁠Queue
•⁠  ⁠MCP server
•⁠  ⁠CLI
•⁠  ⁠External API
•⁠  ⁠Authentication provider
•⁠  ⁠Notification service
•⁠  ⁠File storage
•⁠  ⁠Observability system
•⁠  ⁠Third-party SaaS system

---

5.3 Feature Classification

Everything inside the document should be mapped to features.

This includes:

•⁠  ⁠User stories
•⁠  ⁠User journeys
•⁠  ⁠Screens
•⁠  ⁠Commands
•⁠  ⁠Prompts
•⁠  ⁠Agentic interactions
•⁠  ⁠API documentation flows
•⁠  ⁠CLI flows
•⁠  ⁠MCP flows
•⁠  ⁠States
•⁠  ⁠Edge cases
•⁠  ⁠Error paths
•⁠  ⁠Approval moments
•⁠  ⁠Feedback loops
•⁠  ⁠Trust-building moments
•⁠  ⁠Success criteria
•⁠  ⁠Mermaid sequence diagrams

Each item should answer:

«Which feature does this belong to?»

The Experience & Solution Design Document is therefore both:

 1.⁠ ⁠A product experience document
 2.⁠ ⁠The first structured feature map

---

5.4 Complete Mermaid Sequence Diagrams

The sequence diagrams must cover interactions between:

•⁠  ⁠Humans
•⁠  ⁠Agents
•⁠  ⁠Systems

They should not only show what the human clicks or sees. They must also show what happens between human touchpoints.

Between:

Human Touchpoint 1 → Human Touchpoint 2

The diagram should clarify, at a high level:

•⁠  ⁠Which agent is activated
•⁠  ⁠What reasoning or decision happens
•⁠  ⁠Which systems are called
•⁠  ⁠What data is retrieved
•⁠  ⁠What data is written
•⁠  ⁠Which integrations are involved
•⁠  ⁠What state changes
•⁠  ⁠What output is prepared
•⁠  ⁠What the next human interaction receives

The diagrams should be high-level enough to remain product-oriented, but complete enough to understand the solution logic.

---

5.5 High-Level Product Layer Plan

The high-level product layer plan lives inside the Experience & Solution Design Document.

It is derived from:

•⁠  ⁠Human touchpoints
•⁠  ⁠Agent behavior
•⁠  ⁠System behavior
•⁠  ⁠Sequence diagrams
•⁠  ⁠Feature classification
•⁠  ⁠Required integrations
•⁠  ⁠Required data and core processes

The layer plan should answer:

•⁠  ⁠What inner layers are likely needed to make the experience real?
•⁠  ⁠What is the order from the outer experience to the core?
•⁠  ⁠Which features require which layers?
•⁠  ⁠Which actors belong to which layer?
•⁠  ⁠Which layers are shared across multiple features?
•⁠  ⁠Which layers are optional or uncertain?
•⁠  ⁠What is the likely core of the system?
•⁠  ⁠What dependencies exist between layers?

The number of layers is not fixed.

The layers should be discovered from the actual solution design.

---

5.6 Initial Simulation Inventory

The document should identify which behaviors are expected to be simulated in the prototype.

Examples:

•⁠  ⁠Fake backend response
•⁠  ⁠Hardcoded data
•⁠  ⁠Simulated agent reasoning
•⁠  ⁠Stubbed API call
•⁠  ⁠Static report generation
•⁠  ⁠Fake authentication
•⁠  ⁠Manual background process
•⁠  ⁠Simulated external integration

This inventory becomes important later, because implementation will progressively replace simulations with real functionality.

---

 6.⁠ ⁠Step 3 — Fully Experiential Prototypes

Step 3 builds the outermost product layer: the fully experiential prototype.

The prototype should feel fully functional to the human.

It should not feel like a wireframe, mock, or static demo. The human should be able to live the intended experience as if the product already existed.

Behind the scenes, the prototype may still use:

•⁠  ⁠Fake data
•⁠  ⁠Hardcoded logic
•⁠  ⁠Lightweight backend
•⁠  ⁠Simulated responses
•⁠  ⁠Stubbed integrations
•⁠  ⁠Basic orchestration
•⁠  ⁠Manual or semi-manual processes

The prototype is complete from the human perspective, but incomplete from the system perspective.

Outputs

•⁠  ⁠Working prototype or prototypes
•⁠  ⁠"prototype-feature-map.md"
•⁠  ⁠"prototype-simulation-map.md"

---

6.1 Prototype-to-Feature Mapping

Every prototype should map back to the features defined in the Experience & Solution Design Document.

The mapping should show:

•⁠  ⁠Which screens map to which features
•⁠  ⁠Which flows map to which features
•⁠  ⁠Which commands map to which features
•⁠  ⁠Which prompts map to which features
•⁠  ⁠Which API documentation sections map to which features
•⁠  ⁠Which agentic workflows map to which features
•⁠  ⁠Which outputs map to which features

---

6.2 Prototype Simulation Map

The prototype simulation map should document what is fake, stubbed, hardcoded, manual, or lightweight.

For each simulated behavior, it should specify:

•⁠  ⁠Where it appears in the prototype
•⁠  ⁠Which feature it belongs to
•⁠  ⁠Which actor it simulates: human, agent, or system
•⁠  ⁠Which future layer should eventually replace it
•⁠  ⁠What real behavior will be required later

The prototype is not just a demo. It is the outer implementation reference for the product.

---

 7.⁠ ⁠Step 4 — Riskiest Technical Assumptions

Step 4 identifies the technical assumptions that must be proven before building the real inner layers.

This step asks:

«What technical assumptions could break the product if they are wrong?»

Examples:

•⁠  ⁠Can the AI model reason accurately enough?
•⁠  ⁠Can the agent execute the workflow reliably?
•⁠  ⁠Can the required integrations be achieved?
•⁠  ⁠Can the system meet latency requirements?
•⁠  ⁠Can the system scale to the required volume?
•⁠  ⁠Can the system produce auditable outputs?
•⁠  ⁠Can the data model support the required use cases?
•⁠  ⁠Can the authentication and authorization model work?
•⁠  ⁠Can the system be secured properly?
•⁠  ⁠Can the infrastructure support the expected workload?
•⁠  ⁠Can the MCP / CLI / agent execution model work reliably?

Each assumption should include:

•⁠  ⁠Assumption name
•⁠  ⁠Related feature or features
•⁠  ⁠Related layer or layers
•⁠  ⁠Why it is risky
•⁠  ⁠What must be proven
•⁠  ⁠What failure would mean
•⁠  ⁠What proof of concept is needed
•⁠  ⁠Success criteria

Output

"risky-technical-assumptions.md"

---

 8.⁠ ⁠Step 5 — Technical POCs

Step 5 builds technical proof-of-concepts to validate the riskiest assumptions.

These are not human-facing product prototypes. They are technical tests.

A Technical POC may test:

•⁠  ⁠AI model accuracy
•⁠  ⁠Agent execution reliability
•⁠  ⁠MCP feasibility
•⁠  ⁠CLI feasibility
•⁠  ⁠API integration feasibility
•⁠  ⁠Data pipeline performance
•⁠  ⁠Storage architecture
•⁠  ⁠Workflow orchestration
•⁠  ⁠Authentication model
•⁠  ⁠Permission model
•⁠  ⁠Observability approach
•⁠  ⁠Auditability
•⁠  ⁠Cost profile
•⁠  ⁠Latency profile
•⁠  ⁠Provider limitations

Each POC should include:

•⁠  ⁠Assumption tested
•⁠  ⁠Related features
•⁠  ⁠Related layers
•⁠  ⁠Test design
•⁠  ⁠Providers evaluated
•⁠  ⁠Technologies evaluated
•⁠  ⁠Services evaluated
•⁠  ⁠Results
•⁠  ⁠Trade-offs
•⁠  ⁠Decision taken
•⁠  ⁠Remaining risks
•⁠  ⁠Recommendation

Outputs

•⁠  ⁠Technical POC folders
•⁠  ⁠"technical-decisions.md"

---

 9.⁠ ⁠Step 6+ — Feature Set Onion Loop

After the technical POCs, the method enters the main implementation loop.

The loop works as follows:

«Select a coherent feature set, then build that feature set from the outside in across all required layers. Once that feature set is complete, select the next feature set and repeat.»

This means The Onion Method does not build the whole product globally layer by layer.

It also does not build isolated features without architectural discipline.

It builds coherent feature sets through the layers required to make those features real.

---

9.1 Loop Step 1 — Select the Next Feature Set

Choose the next group of features to implement.

A feature set should be logically grouped.

It may be selected because:

•⁠  ⁠The features belong to the same user journey.
•⁠  ⁠The features share the same architecture.
•⁠  ⁠The features depend on the same providers.
•⁠  ⁠The features unlock later features.
•⁠  ⁠The features reduce major uncertainty.
•⁠  ⁠The features create the first valuable working slice.
•⁠  ⁠The features are foundational for the product.

The selected feature set should be small enough to execute, but meaningful enough to create a coherent working increment.

Output

"selected-feature-set.md"

This should include:

•⁠  ⁠Features included
•⁠  ⁠Features excluded
•⁠  ⁠Reason for selection
•⁠  ⁠Dependencies
•⁠  ⁠Target layers to implement
•⁠  ⁠Acceptance criteria
•⁠  ⁠Human review criteria

---

9.2 Loop Step 2 — Build the Selected Feature Set Layer by Layer

For the selected feature set, build inward through the product layers defined in the Experience & Solution Design Document.

For each required layer, execute the following process.

---

9.2.1 Define the Layer for This Feature Set

Clarify what this layer means for the selected features.

This should answer:

•⁠  ⁠What does this layer own?
•⁠  ⁠Which features does it support?
•⁠  ⁠Which prototype simulations does it replace?
•⁠  ⁠What logic, reasoning, integration, data, or process does it provide?
•⁠  ⁠How does it connect to the existing outer layer?
•⁠  ⁠How does it prepare for deeper layers?
•⁠  ⁠What does it not own?
•⁠  ⁠What does “done” mean for this layer?

Output

"layer-definition.md"

---

9.2.2 Define Providers and Services

Identify the providers, services, infrastructure, and external systems needed for this layer.

This may include:

•⁠  ⁠Cloud provider
•⁠  ⁠Database
•⁠  ⁠Model provider
•⁠  ⁠Vector store
•⁠  ⁠Queue
•⁠  ⁠Workflow engine
•⁠  ⁠API provider
•⁠  ⁠Authentication provider
•⁠  ⁠Observability provider
•⁠  ⁠MCP runtime
•⁠  ⁠CLI runtime
•⁠  ⁠Agent runtime
•⁠  ⁠Internal service
•⁠  ⁠External integration

This step should define what will be used and why.

Output

"providers-and-services.md"

---

9.2.3 Prepare Secrets Safely

Prepare the secrets required for this layer.

The key rule is:

«Raw secrets must never be shared with an LLM.»

Secrets should be stored in a secure secrets manager, such as:

•⁠  ⁠Google Secret Manager
•⁠  ⁠AWS Secrets Manager
•⁠  ⁠Azure Key Vault
•⁠  ⁠Vault
•⁠  ⁠Another approved secure provider

Methodology files may include:

•⁠  ⁠Secret name
•⁠  ⁠Purpose
•⁠  ⁠Provider
•⁠  ⁠Environment
•⁠  ⁠Feature or layer that uses it
•⁠  ⁠Storage reference
•⁠  ⁠Owner
•⁠  ⁠Status

Methodology files must never include:

•⁠  ⁠Raw API keys
•⁠  ⁠Raw tokens
•⁠  ⁠Raw passwords
•⁠  ⁠OAuth client secrets
•⁠  ⁠Signing secrets
•⁠  ⁠Private keys
•⁠  ⁠Webhook secrets
•⁠  ⁠Service account keys

Output

"safe-secrets-plan.md"

---

9.2.4 Write Implementation Issues

Before coding, create self-contained implementation issues.

Each issue should contain enough linked context for a human developer or AI coding agent to understand exactly what needs to be built.

Each issue should include:

•⁠  ⁠Issue title
•⁠  ⁠Feature set
•⁠  ⁠Feature
•⁠  ⁠Layer
•⁠  ⁠Objective
•⁠  ⁠User-facing outcome
•⁠  ⁠Technical scope
•⁠  ⁠Out of scope
•⁠  ⁠Dependencies
•⁠  ⁠Links to exact relevant sections of prior artifacts
•⁠  ⁠Related sequence diagrams
•⁠  ⁠Related prototype behavior
•⁠  ⁠Simulations being replaced
•⁠  ⁠Expected files or folders
•⁠  ⁠Required providers and services
•⁠  ⁠Required secret references
•⁠  ⁠Acceptance criteria
•⁠  ⁠Test plan
•⁠  ⁠Definition of done

Output

Implementation issues in Linear, GitHub, or the selected issue tracker.

---

9.2.5 Build, Code, and Test the Layer

Implement the layer for the selected feature set.

This includes:

•⁠  ⁠Writing code
•⁠  ⁠Connecting the layer to the existing outer layer
•⁠  ⁠Replacing simulated behavior with real functionality
•⁠  ⁠Implementing integrations
•⁠  ⁠Implementing data structures if needed
•⁠  ⁠Implementing backend, agentic, CLI, MCP, or API behavior
•⁠  ⁠Adding tests
•⁠  ⁠Running tests
•⁠  ⁠Fixing failures
•⁠  ⁠Verifying the layer independently
•⁠  ⁠Verifying the layer integrated with all previously built outer layers

The codebase should be organized by feature.

Each feature folder should contain the files needed to power that feature end-to-end, such as:

•⁠  ⁠Frontend
•⁠  ⁠Backend
•⁠  ⁠Agent logic
•⁠  ⁠MCP tools
•⁠  ⁠CLI commands
•⁠  ⁠API routes
•⁠  ⁠Data structures
•⁠  ⁠Deployment files
•⁠  ⁠Tests
•⁠  ⁠Documentation
•⁠  ⁠Observability configuration

The principle is:

«Organize code around product capabilities, not only around technical layers.»

Output

Implemented and tested layer for the selected feature set.

---

9.2.6 Human Review Checkpoint

A human reviews whether the layer works as expected.

The review should evaluate:

•⁠  ⁠Does the layer correctly power the selected features?
•⁠  ⁠Does the human experience still behave as intended?
•⁠  ⁠Are the right providers and services being used?
•⁠  ⁠Are secrets handled safely?
•⁠  ⁠Are tests passing?
•⁠  ⁠Is the implementation aligned with the Experience & Solution Design Document?
•⁠  ⁠Is it aligned with the prototype?
•⁠  ⁠Is it aligned with the technical POCs?
•⁠  ⁠Is it aligned with the layer plan?
•⁠  ⁠Is this layer complete enough to move deeper?
•⁠  ⁠Should anything be revised before continuing?

The checkpoint can result in:

•⁠  ⁠Approval to move to the next inner layer
•⁠  ⁠Feedback and another pass on the same layer
•⁠  ⁠Revisions to the layer definition
•⁠  ⁠New technical POCs if unexpected risks appear
•⁠  ⁠Changes to providers or services
•⁠  ⁠Changes to the implementation

Output

"human-review.md"

---

9.3 Complete All Required Layers for the Selected Feature Set

The selected feature set is complete only when it has been implemented through all required layers.

That means the features are no longer just experiential prototypes. They are real through the necessary depth of the system.

For that feature set, the system now has:

•⁠  ⁠Human experience
•⁠  ⁠Real logic or reasoning
•⁠  ⁠Real integrations, if needed
•⁠  ⁠Real provider usage
•⁠  ⁠Safe secret handling
•⁠  ⁠Real data or core process, if needed
•⁠  ⁠Passing tests
•⁠  ⁠Human-reviewed behavior

---

9.4 Select the Next Feature Set

Once one feature set is complete, select the next feature set and repeat the loop.

The rhythm is:

Feature Set A
  → Build required layers
  → Human review

Feature Set B
  → Build required layers
  → Human review

Feature Set C
  → Build required layers
  → Human review

Continue until all features from the Experience & Solution Design Document and prototype map are implemented through the required system layers.

---

10.⁠ ⁠Traceability Requirement

The Onion Method depends on strong traceability.

Every artifact should link to the relevant artifacts before and after it.

The system should be able to trace:

Constitution
→ Experience & Solution Design
→ Prototype
→ Risky Technical Assumptions
→ Technical POCs
→ Feature Set
→ Layer Definition
→ Providers and Services
→ Secrets Plan
→ Implementation Issues
→ Code
→ Tests
→ Human Review

This traceability allows AI coding agents and human reviewers to understand why something exists, what it supports, how it should behave, and how it should be validated.

---

11.⁠ ⁠Final Completion Criteria

The system is complete when:

•⁠  ⁠All required feature sets have been implemented.
•⁠  ⁠Each feature set has been built through its required inner layers.
•⁠  ⁠The experiential prototypes have been replaced by real functionality.
•⁠  ⁠The core data, process, logic, reasoning, or integration layers are complete where needed.
•⁠  ⁠Tests pass.
•⁠  ⁠Secrets are safely managed.
•⁠  ⁠Human review confirms the product works as intended.

---

12.⁠ ⁠Simplified Method Summary

Step| Name| Output
0| New Service Decision| "build-mode-decision.md"
1| Constitution| "constitution.md"
2| Experience & Solution Design| "experience-solution-design.md"
3| Fully Experiential Prototypes| Prototype(s), "prototype-feature-map.md", "prototype-simulation-map.md"
4| Riskiest Technical Assumptions| "risky-technical-assumptions.md"
5| Technical POCs| POCs + "technical-decisions.md"
6+| Feature Set Onion Loop| Feature set → layer → providers → secrets → issues → build/test → human review → repeat

---

13.⁠ ⁠One-Sentence Definition

The Onion Method is an AI-native development method that defines a new service through target audience and value proposition, designs the complete human-agent-system experience, builds a fully experiential outer layer, de-risks the technology, and then implements coherent feature sets from the outside in until the full system reaches its core.