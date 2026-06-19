# Provider Preferences

Capture preferred providers or attributes, blocked providers, required certifications or constraints, and how much weight to give existing relationships versus new providers.

Provider identity KYC is already handled by Stripe when the provider connects it at setup
(legal identity, sanctions/AML screening, and baseline financial checks), so the buyer
never re-collects that. Here, capture only any extra documents the buyer wants to verify a
seller for this kind of purchase, beyond the KYC Stripe already did: references or case
studies, certifications (for example ISO, SOC 2, or security attestations), insurance or
liability coverage, and, for data services, privacy or data-processing terms (DPA). Make
clear to the human that identity and AML KYC is already covered by Stripe. These extra
documents feed the §4 due diligence gate. For an individual or a recurring,
already-approved provider, most extra documents collapse to Not applicable with the
reason; confirm that with the human.
