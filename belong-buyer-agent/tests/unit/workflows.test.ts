/**
 * Tests unitarios de los workflows (skills). No usan el LLM.
 */
import { describe, it, expect, beforeEach } from "vitest";
import { runWorkflow } from "../helpers";
import { quotationFlow } from "../../src/mastra/workflows/quotation-flow";
import { negotiationFlow } from "../../src/mastra/workflows/negotiation-flow";
import { contractFlow } from "../../src/mastra/workflows/contract-flow";
import { BUYER_ID, PLAYBOOK_CONSTANTS } from "../../src/mastra/data/playbook-mock";
import * as mcp from "../../src/mastra/data/mcp-responses-mock";

const need = {
  description: "Desarrollo de app móvil en React Native",
  requirements: ["timeline", "stack", "equipo", "referencias", "propuesta"],
  deadline: "2026-09-30",
  budget: PLAYBOOK_CONSTANTS.budget_max_usd,
};

beforeEach(() => mcp.__resetMockState());

describe("quotation-flow", () => {
  it("completa todos los steps y produce una recomendación", async () => {
    const out = await runWorkflow(quotationFlow, { buyer_id: BUYER_ID, need });
    expect(out.rfp_rules).toBeTruthy();
    expect(out.provider_prefs).toBeTruthy();
    expect(out.rfp_id).toBeTruthy();
    expect(out.comparison.ranking.length).toBeGreaterThan(0);
    expect(out.recommendation).toBeTruthy();
  });
});

describe("negotiation-flow", () => {
  it("respeta el BATNA: la contrapropuesta nunca baja de $35k", async () => {
    const out = await runWorkflow(negotiationFlow, {
      buyer_id: BUYER_ID,
      quote_id: "quote_prov_001", // 38k -> counter debe quedar en el BATNA
    });
    expect(out.counter.amount).toBeGreaterThanOrEqual(
      PLAYBOOK_CONSTANTS.batna_usd,
    );
  });

  it("escala cuando no hay zona de acuerdo (proveedor rechaza)", async () => {
    const out = await runWorkflow(negotiationFlow, {
      buyer_id: BUYER_ID,
      quote_id: "quote_no_deal",
    });
    expect(out.result.status).toBe("escalate");
  });
});

describe("contract-flow", () => {
  it("firma automáticamente cuando el monto < $30k", async () => {
    const out = await runWorkflow(contractFlow, {
      buyer_id: BUYER_ID,
      quote_id: "quote_test_25k",
    });
    expect(out.requires_human_approval).toBe(false);
    expect(out.result.status).toBe("contract_signed");
  });

  it("marca requires_human_approval cuando el monto > $30k", async () => {
    const out = await runWorkflow(contractFlow, {
      buyer_id: BUYER_ID,
      quote_id: "quote_test_45k",
    });
    expect(out.requires_human_approval).toBe(true);
    expect(out.result.status).toBe("requires_approval");
  });

  it("verifica la presencia de la cláusula de penalidad", async () => {
    const out = await runWorkflow(contractFlow, {
      buyer_id: BUYER_ID,
      quote_id: "quote_test_25k",
    });
    expect(out.validation.has_penalty_clause).toBe(true);
  });
});
