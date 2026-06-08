# issue-tracker.md

```xml
<?xml version="1.0" encoding="UTF-8"?>
<linear_issue_setup stack="alejo-v2">
  <purpose>Tell Alejo v2 where planning documents live, where implementation issues are created, and how ready issues reach Symphony.</purpose>
  <configured_project name="A2A Marketplace v1" url="https://linear.app/alejobelonguniverse/project/a2a-marketplace-v1-99f423f95889">
    <team name="Belonguniverse" key="BEL" />
    <access_method>Linear connector/MCP</access_method>
  </configured_project>
  <project_documents>
    <document name="AGENTS.md" purpose="Source-of-truth map." />
    <document name="issue-tracker.md" purpose="Linear issue and handoff setup." />
    <document name="triage-labels.md" purpose="Statuses and labels." />
    <document name="alejo-workflow.md" purpose="Alejo lifecycle." />
    <document name="WORKFLOW.md" purpose="Mirror of repo Symphony contract." />
    <document name="Q&amp;A.xml" purpose="Questions, decisions, and product snapshot." />
    <document name="CONTEXT.xml" purpose="Domain language and relationships." />
    <document name="PRD.xml" purpose="Product intent and functional requirements." />
    <document name="prototype.xml" purpose="UX evidence and prototype HTML." />
    <document name="SAD.xml" alternate="SAT.xml" purpose="Architecture, providers, deployment, and code structure." />
  </project_documents>
  <issue_contract>
    <format>XML</format>
    <required_fields>observable behavior, source refs, providers, Doppler secret names, dependencies, preconditions, acceptance criteria, surface, BDD budget, representative prompts/actions, Playwright expectations, provider evidence, latency/timeout expectations, production constraints, and feature-owned code organization</required_fields>
    <invalid>mocks, fake providers, stubbed SDK responses, placeholder code, skipped tests, disabled branches, NotImplemented, TODO-only paths, and unwired UI</invalid>
  </issue_contract>
  <symphony_handoff>
    <status role="source" name="Ready for Agent" />
    <status role="execution" name="Night Shift Queued" />
    <status role="running" name="In Night Shift" />
    <status role="handoff" name="Ready for Human" />
    <status role="human_done" name="Done" />
    <rule>alejo-run-v2 moves passing issues into Symphony without approval prompts, verifies the handoff, and leaves clean work in Ready for Human. Only a human moves work to Done.</rule>
  </symphony_handoff>
  <source_of_truth>Linear Project Documents own setup and planning. Repo WORKFLOW.md owns the runtime contract and is mirrored to Linear. Linear issue state owns implementation readiness.</source_of_truth>
</linear_issue_setup>
```
