# alejo-workflow.md

```xml
<?xml version="1.0" encoding="UTF-8"?>
<alejo_workflow stack="v2">
  <purpose>Describe how Alejo v2 moves from product clarity to production-ready Symphony handoffs.</purpose>
  <artifact_homes>
    <linear_project_documents>AGENTS.md, issue-tracker.md, triage-labels.md, alejo-workflow.md, WORKFLOW.md mirror, Q&amp;A.xml, CONTEXT.xml, PRD.xml, prototype.xml, SAD.xml, and ADR XML when published there.</linear_project_documents>
    <repo>Project code, repo WORKFLOW.md, tests, runtime commands, branches, PRs, and ADR XML when the repo owns ADRs.</repo>
    <linear_issues>Self-contained production-ready vertical-slice implementation contracts.</linear_issues>
    <doppler>Secret values and environment-backed runtime config.</doppler>
  </artifact_homes>
  <planning>
    <step order="1" skill="alejo-questions-v2">Clarify product experience, value proposition, domain language, and decisions. Publish Q&amp;A.xml and CONTEXT.xml.</step>
    <step order="2" skill="alejo-prd-v2">Create PRD.xml from Q&amp;A.xml and product context.</step>
    <step order="3" skill="alejo-prototype">Create prototype.xml when UI evidence helps.</step>
    <step order="4" skill="alejo-sad-v2">Create SAD.xml from PRD, Q&amp;A, CONTEXT, prototype, ADRs, provider questions, and repo architecture.</step>
    <step order="5" skill="alejo-issues-v2">Create vertical-slice Linear issues with self-contained XML run contracts.</step>
    <step order="6" skill="alejo-secrets-v2">Resolve provider resources and Doppler secret names before execution.</step>
    <step order="7" skill="alejo-consistency-propagation-v2">Read selected documents line by line, classify drift, and propagate approved changes.</step>
  </planning>
  <execution skill="alejo-run-v2">
    <step order="1">Read repo WORKFLOW.md, its Linear mirror, setup docs, ready issues, and Doppler names.</step>
    <step order="2">Preflight XML run contracts and secrets.</step>
    <step order="3">Move passing issues to Night Shift Queued without approval prompts.</step>
    <step order="4">Launch or resume Symphony from WORKFLOW.md.</step>
    <step order="5">Verify Symphony TDD handoff, run BDD real-surface checks, run alejo-review in a fresh subagent, repair gaps, and leave clean work in Ready for Human.</step>
  </execution>
  <review skill="alejo-review">Audit Ready for Human handoffs and the built repo against PRD, SAD, Q&amp;A, CONTEXT, prototype evidence, ADRs, and issue contracts. Only the human moves passing work to Done.</review>
</alejo_workflow>
```
