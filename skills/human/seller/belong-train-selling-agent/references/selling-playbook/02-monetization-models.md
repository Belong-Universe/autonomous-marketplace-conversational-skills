# Monetization Models

[Back to index](index.md) | Previous: [Value Proposition](01-value-proposition.md) | Next: [Legal And Contracts](03-legal-and-contracts.md)

This section defines how the Service makes money and how payment behavior should work in the marketplace.

## Source Signals

Look for pricing sheets, proposals, order forms, invoices, finance notes, and sales approval rules.

## Required Fields

- Pricing model (for phase 1 this is a fixed price)
- Fixed price (the currency is always USD)
- Seller-side platform fee awareness and seller net explanation
- Payment readiness assumptions
- Payment exception escalation path

In phase 1 there is one payment modality: escrow. The full amount is held when the
contract is signed and released to the seller when the buyer accepts the deliverable.
There is no starting price, no billing cycle, and no collections policy, because there
are no negotiations or discounts in this phase.

## Quality Bar

The section is `Done` when the Selling Agent can explain the fixed price in USD, the
escrow modality, the platform fee, and the seller net, and can escalate payment
exceptions before moving money outside authority.

## Guardrails

- Do not hide platform fees or merchant-of-record context.
- Do not let the Selling Agent invent discounts, payment plans, or refunds.
- Do not allow payment movement without linked contract, acceptance, exception approval, or audit path.

