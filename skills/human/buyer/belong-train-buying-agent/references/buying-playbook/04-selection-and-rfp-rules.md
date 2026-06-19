# Selection And RFP Rules

Capture when to go direct versus competitive, how to structure a Buying Request and RFP, the questions sellers must answer, ranking and weighting criteria, and proposal comparison rules for scoring seller-signed Service Contract/SOW proposals. For an individual or simple purchase this often collapses to direct buying; mark RFP and competitive selection as Not applicable with the reason, and confirm that assumption with the human.

## Provider Due Diligence

Provider identity KYC (legal identity, sanctions/AML, baseline financial checks) is
already done by Stripe at the provider's setup, so this gate never re-runs KYC; it only
checks the extra verification documents the buyer asked for. Capture the due diligence gate
the Buying Agent runs before awarding work, reusing the extra documents defined in Provider
Preferences. Define the journey:

- Trigger: when due diligence applies, for example above a spend threshold or for any new
  provider. Skip it for an already-approved or recurring provider. The human sets the
  threshold.
- Required documents: the extra documents the human marked in Provider Preferences for
  this kind of purchase (KYC is already covered by Stripe, so it is not requested again).
- How the agent collects them: through the seller-led Discovery Questionnaire the provider
  already answers before contract, so no new step is added; the files are retained with the
  Active Service for later dispute access.
- Outcome: if the provider passes, the agent may award; if a document is missing, it
  escalates to the human through the Marketplace Inbox; if a hard requirement fails (for
  example a blocked provider or no mandatory insurance), it does not award.

For an individual or simple purchase, due diligence usually collapses to Not applicable
with the reason; surface that assumption and confirm it with the human.
