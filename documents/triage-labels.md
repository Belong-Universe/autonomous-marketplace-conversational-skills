# triage-labels.md

```xml
<?xml version="1.0" encoding="UTF-8"?>
<linear_statuses_and_labels stack="alejo-v2">
  <purpose>Give Alejo v2 one shared vocabulary for issue readiness, Symphony execution, handoff, and follow-up classification.</purpose>
  <workflow_statuses>
    <status role="needs-triage" name="Needs Triage" />
    <status role="needs-info" name="Needs Info" />
    <status role="ready-for-human" name="Ready for Human" />
    <status role="ready-for-agent" name="Ready for Agent" />
    <status role="symphony-execution" name="Night Shift Queued" />
    <status role="in-symphony" name="In Night Shift" />
    <status role="done" name="Done" />
    <status role="wontfix" name="Won't Fix" />
  </workflow_statuses>
  <issue_labels>
    <label>vertical-slice</label>
    <label>hitl</label>
    <label>sad-follow-up</label>
    <label>surface:api</label>
    <label>surface:ui</label>
    <label>surface:cli</label>
    <label>surface:mcp</label>
    <label>secrets-required</label>
  </issue_labels>
  <rules>
    <rule>Labels classify Linear issues only.</rule>
    <rule>Planning artifacts live in Linear Project Documents, not issues.</rule>
    <rule>Only humans move issues to Done.</rule>
  </rules>
</linear_statuses_and_labels>
```
