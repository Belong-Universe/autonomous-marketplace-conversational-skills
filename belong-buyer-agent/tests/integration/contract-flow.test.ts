/**
 * Test de integración del contract-flow con mocks. No usa el LLM.
 */
import { describe, it, expect, beforeEach } from "vitest";
import { runWorkflow } from "../helpers";
import { contractFlow } from "../../src/mastra/workflows/contract-flow";
import { BUYER_ID } from "../../src/mastra/data/playbook-mock";
import * as mcp from "../../src/mastra/data/mcp-responses-mock";

beforeEach(() => mcp.__resetMockState());

describe("integración: contract-flow", () => {
  it("contrato de $25k -> firma automáticamente", async () => {
    const out = await runWorkflow(contractFlow, {
      buyer_id: BUYER_ID,
      quote_id: "quote_test_25k",
    });
    expect(out.result.status).toBe("contract_signed");
    expect(out.result.signed.escrow_activated).toBe(true);
  });

  it("contrato de $45k -> requiere aprobación humana", async () => {
    const out = await runWorkflow(contractFlow, {
      buyer_id: BUYER_ID,
      quote_id: "quote_test_45k",
    });
    expect(out.result.status).toBe("requires_approval");
    expect(out.result.amount).toBe(45_000);
  });

  it("valida la cláusula de penalidad y la ley colombiana", async () => {
    const out = await runWorkflow(contractFlow, {
      buyer_id: BUYER_ID,
      quote_id: "quote_test_25k",
    });
    expect(out.validation.has_penalty_clause).toBe(true);
    expect(out.validation.colombian_law).toBe(true);
    expect(out.validation.has_nda).toBe(true);
  });
});
