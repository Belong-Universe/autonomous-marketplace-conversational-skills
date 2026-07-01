# Examples

[Back to index](index.md) | Previous: [Generated Playbook Folder](generated-playbook-folder.md)

This page contains exactly one example of how to do it and one example of how not to do it.

## How To Do It

**Section:** Negotiations

**Chat checkpoint**

- Source-backed: Expected budget for this category is around 1,500; hard ceiling is 1,800.
- Source-backed: Net-30 is standard; upfront payment requires finance approval.
- Human-provided: Prefer quality over price at a 60/40 weighting.

**Proposed section fill**

- The Buying Agent opens at 1,400 and concedes in steps of 150, up to 3 autonomous rounds.
- The Buying Agent may trade timeline and payment terms (net-30) before conceding more price.
- It uses perceived signals — competing quotes available, buyer urgency, seller eagerness, reputation — to decide whether to press or concede.
- Disclosure: it may say "we're near our limit for this," but never reveals the 1,800 ceiling or the 60/40 weighting.
- Walk-away / no-ZOPA: if the seller's floor exceeds 1,800, the agent does not raise the ceiling. It escalates to the Marketplace Inbox with a Decision Explanation asking whether to raise the ceiling, reduce scope, or move to another provider.

**Still missing**

- Cumulative exposure limit across active purchases
- Named finance approver for upfront payment

**Approval gate**

Approve this section so we can continue to Legal And Contracts, or tell me what to change.

## How Not To Do It

**Section:** Negotiations

The agent should get the best price it can, be flexible, and escalate if the deal feels too expensive.

**Why this fails**

- No opening offer or concession ladder
- No ceiling or walk-away point
- No disclosure boundary, so the agent might reveal the real budget
- No no-ZOPA rule, so the agent could keep looping or overcommit
- Forces the Buying Agent to guess what "best price" and "too expensive" mean
