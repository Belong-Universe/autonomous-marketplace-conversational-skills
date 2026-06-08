---
name: belong-check-payments
description: Human-facing read/check payment and bank view for the mocked Belong marketplace. Use for bank readiness, transactions, payment ledger, authorizations, charges, holds, releases, refunds, collections, seller-side platform fees, seller net, merchant-of-record context, and Stripe Payment Stack mock visibility.
---

# Belong Check Payments

Use this when a Service Provider human or buyer-side human asks about bank setup, transactions, payment status, collections, refunds, holds, platform fees, seller net, or the Stripe Payment Stack mock.

This is a read/check skill. It must not directly move money, authorize payments, charge, release, refund, collect, sign contracts, approve Change Orders, or change payment rules.

## Guided Flow

Run runtime `payments` with the relevant owner role and optional Active Service ID.

Show:

- Bank/payment readiness
- Payment transactions
- Active Service payment ledger
- Gross amount, seller-side platform fee, seller net
- Authorization, charge, hold, release, refund, and collection state
- Merchant-of-record distinction
- Linked Service Contract/SOW, Change Order, Active Service, and Audit Log path

## Route Actions

- Payment exception or operational approval: `$belong-inbox`
- Durable payment rule or collections change: `$belong-train-buying-agent` or `$belong-train-selling-agent`
- Temporary preference about payment handling inside current authority: `$belong-steer-buying-agent` or `$belong-steer-selling-agent`
- Delivery context: `$belong-check-active-services`
