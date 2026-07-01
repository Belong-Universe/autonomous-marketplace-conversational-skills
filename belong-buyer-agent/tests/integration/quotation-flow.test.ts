/**
 * Test de integración del quotation-flow con mocks. No usa el LLM.
 */
import { describe, it, expect, beforeEach } from "vitest";
import { runWorkflow } from "../helpers";
import { quotationFlow } from "../../src/mastra/workflows/quotation-flow";
import { playbookAuditLog, __resetAuditLog } from "../../src/mastra/tools/playbook";
import { BUYER_ID, PLAYBOOK_CONSTANTS } from "../../src/mastra/data/playbook-mock";
import * as mcp from "../../src/mastra/data/mcp-responses-mock";

const need = {
  description: "Desarrollo de app móvil en React Native",
  requirements: ["timeline", "stack", "equipo", "referencias", "propuesta"],
  deadline: "2026-09-30",
  budget: PLAYBOOK_CONSTANTS.budget_max_usd,
};

beforeEach(() => {
  mcp.__resetMockState();
  __resetAuditLog();
});

describe("integración: quotation-flow", () => {
  it("consulta rfp_rules y provider_preferences en el playbook", async () => {
    await runWorkflow(quotationFlow, { buyer_id: BUYER_ID, need });
    const consulted = playbookAuditLog.map((e) => e.section);
    expect(consulted).toContain("rfp_rules");
    expect(consulted).toContain("provider_preferences");
  });

  it("envía RFPs a exactamente 3 proveedores", async () => {
    const out = await runWorkflow(quotationFlow, { buyer_id: BUYER_ID, need });
    expect(out.providers).toHaveLength(3);
    expect(out.profiles).toHaveLength(3);
  });

  it("produce cotizaciones ordenadas por score (desc)", async () => {
    const out = await runWorkflow(quotationFlow, { buyer_id: BUYER_ID, need });
    const scores = out.comparison.ranking.map((r: any) => r.total_score);
    const sorted = [...scores].sort((a, b) => b - a);
    expect(scores).toEqual(sorted);
    expect(out.comparison.recommended_quote_id).toBe(
      out.comparison.ranking[0].quote_id,
    );
  });
});
