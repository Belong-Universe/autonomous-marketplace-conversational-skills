/**
 * Test de integración del negotiation-flow con mocks. No usa el LLM.
 */
import { describe, it, expect, beforeEach } from "vitest";
import { runWorkflow } from "../helpers";
import { negotiationFlow } from "../../src/mastra/workflows/negotiation-flow";
import { BUYER_ID, PLAYBOOK_CONSTANTS } from "../../src/mastra/data/playbook-mock";
import * as mcp from "../../src/mastra/data/mcp-responses-mock";

beforeEach(() => mcp.__resetMockState());

describe("integración: negotiation-flow", () => {
  it("negocia un quote sobre presupuesto sin bajar del BATNA", async () => {
    const out = await runWorkflow(negotiationFlow, {
      buyer_id: BUYER_ID,
      quote_id: "quote_over_budget", // 48k
    });
    // La contrapropuesta respeta el BATNA y no toca términos de pago.
    expect(out.counter.amount).toBeGreaterThanOrEqual(PLAYBOOK_CONSTANTS.batna_usd);
    expect(out.counter.terms).toMatch(/no negociable/i);
    // Termina dentro de presupuesto.
    if (out.result.status === "accepted") {
      expect(out.result.final_amount).toBeLessThanOrEqual(
        PLAYBOOK_CONSTANTS.budget_max_usd,
      );
    }
  });

  it("retorna 'escalate' cuando el proveedor rechaza (sin acuerdo)", async () => {
    const out = await runWorkflow(negotiationFlow, {
      buyer_id: BUYER_ID,
      quote_id: "quote_no_deal", // 70k, piso 70k
    });
    expect(out.seller_response.status).toBe("rejected");
    expect(out.result.status).toBe("escalate");
  });
});
