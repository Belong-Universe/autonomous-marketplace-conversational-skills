# Way Of Work During An Active Service

[Back to index](index.md) | Previous: [Legal And Contracts](03-legal-and-contracts.md) | Next: [Human-To-Human Meetings](05-human-to-human-meetings.md)

This section defines how delivery runs after buyer signature creates an Active Service.

## Source Signals

Look for delivery SOPs, onboarding checklists, kickoff decks, project plans, status templates, QA checklists, deliverable templates, acceptance forms, and support notes.

## Required Fields

- Kickoff process
- Delivery milestones and sequencing
- Fulfillment Tasks owned by provider humans or teams
- Selling Agent responsibilities during delivery
- Buyer information needed during delivery
- Deliverable Evidence Package contents
- Evidence mapping to acceptance criteria
- Evidence approach per deliverable type: when the deliverable is sufficient on its own and when to attach optional supporting evidence (for example transcript, recording, or photo for a live session)
- Revision, rejection, and acceptance workflow
- Payment ledger expectations tied to delivery and acceptance
- Audit requirements
- Completion and handoff process

## Deliverable / evidence types (Belong marketplace)

Every deliverable the Selling Agent submits is one of two Belong marketplace kinds (closed set):

- **External URL** (`external_url`): a link to work hosted off-platform. Requires an `https` URL (no credentials, no private/metadata IPs), a description, and a `sha256:` content hash computed off-marketplace.
- **Platform file** (`platform_file`): a file uploaded to Belong's storage. Belong computes the `sha256` server-side, records its content type and size (up to 5 GiB), and runs an antivirus scan; only a `clean` file is accepted. No URL is attached.

Both kinds always carry a content hash as the non-repudiation anchor. Supporting material (for example a transcript, recording, or photo) is attached using these same two kinds — it is not a separate type.

## Quality Bar

The section is `Done` when the Selling Agent can coordinate ordinary delivery, request provider work, submit evidence, support acceptance, and keep payment and audit state coherent.

## Guardrails

- Do not let the Selling Agent fabricate evidence.
- Do not release or collect payment without the required contract, evidence, acceptance, or approved exception.
- Do not treat provider human tasks as completed until the provider confirms or evidence proves completion.
- Keep every file and any submitted evidence retained with the Active Service for dispute readiness.

