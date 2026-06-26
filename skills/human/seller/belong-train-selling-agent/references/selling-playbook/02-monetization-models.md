# Monetization Models

[Back to index](index.md) | Previous: [Value Proposition](01-value-proposition.md) | Next: [Legal And Contracts](03-legal-and-contracts.md)

This section defines how the Service makes money and how payment behavior should work in the marketplace.

## Source Signals

Look for pricing sheets, proposals, order forms, invoices, finance notes, and sales approval rules.

## Required Fields

- Pricing model: one of the five Belong marketplace models (closed set) — `fixed`, `hourly`, `milestone`, `recurring`, `consumption`. This is declared on the Service/Listing as the *shape* of the price; no amount ever lives on the Listing.
- Fixed price (the currency is always USD)
- For a `recurring` model, the billing cycle (`monthly`, `quarterly`, or `annual`)
- Seller-side platform fee awareness and seller net explanation
- Payment readiness assumptions
- Payment exception escalation path

The pricing model declares how the Service intends to charge, mirroring the real
marketplace's closed set. Today the only model Belong authors end-to-end (priced offer
through payment) is `fixed` with escrow: the full amount is held when the contract is
signed and released to the seller when the buyer accepts the deliverable. The other
models (`hourly`, `milestone`, `recurring`, `consumption`) — and the billing cycle a
`recurring` model carries — are declarable now but not yet driven through the
offer/payment flow, so do not promise a buyer a billing cycle or usage-based charge the
marketplace cannot execute yet.

## Quality Bar

The section is `Done` when the Selling Agent can explain the fixed price in USD, the
escrow modality, the platform fee, and the seller net, and can escalate payment
exceptions before moving money outside authority.

## Guardrails

- Do not hide platform fees or merchant-of-record context.
- Do not let the Selling Agent invent discounts, payment plans, or refunds.
- Do not allow payment movement without linked contract, acceptance, exception approval, or audit path.

