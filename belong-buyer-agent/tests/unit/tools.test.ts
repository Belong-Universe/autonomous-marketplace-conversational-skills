/**
 * Tests unitarios de las tools (MCP + playbook). No usan el LLM.
 */
import { describe, it, expect, beforeEach } from "vitest";
import {
  searchProvidersTool,
  getProviderProfileTool,
  sendRfpTool,
  getQuotesTool,
  compareQuotesTool,
  sendCounterOfferTool,
  getContractTool,
  signContractTool,
} from "../../src/mastra/tools/belong-mcp";
import { getPlaybookSectionTool } from "../../src/mastra/tools/playbook";
import {
  PLAYBOOK_SECTIONS,
  BUYER_ID,
  getPlaybookSection,
} from "../../src/mastra/data/playbook-mock";
import * as mcp from "../../src/mastra/data/mcp-responses-mock";

// Helper: invoca el execute de una tool (ignora el contexto, no usado en mocks).
const call = (tool: any, input: any) => tool.execute(input, {} as any);

beforeEach(() => mcp.__resetMockState());

describe("MCP tools: schema de salida", () => {
  it("search_providers retorna proveedores válidos", async () => {
    const out = await call(searchProvidersTool, { experience_years: 3 });
    expect(out.providers.length).toBeGreaterThanOrEqual(3);
    for (const p of out.providers) {
      expect(p).toMatchObject({
        id: expect.any(String),
        name: expect.any(String),
        rating: expect.any(Number),
      });
    }
  });

  it("get_provider_profile retorna un perfil completo", async () => {
    const out = await call(getProviderProfileTool, { provider_id: "prov_001" });
    expect(out.profile.references.length).toBeGreaterThanOrEqual(2);
    expect(out.profile.tech_stack).toContain("React Native");
  });

  it("send_rfp confirma envío a cada proveedor", async () => {
    const out = await call(sendRfpTool, {
      provider_ids: ["prov_001", "prov_002", "prov_003"],
      rfp: {
        description: "App móvil",
        requirements: ["timeline", "stack", "equipo"],
        deadline: "2026-07-15",
        budget: 50_000,
      },
    });
    expect(out.rfp_id).toBeTruthy();
    expect(out.sent_to).toHaveLength(3);
    expect(out.sent_to[0].status).toBe("sent");
  });

  it("get_quotes oculta el piso interno del proveedor", async () => {
    const out = await call(getQuotesTool, { rfp_id: "rfp_inexistente" });
    expect(out.quotes.length).toBeGreaterThan(0);
    for (const q of out.quotes) {
      expect(q).not.toHaveProperty("seller_floor");
    }
  });

  it("compare_quotes ordena por score y recomienda", async () => {
    const out = await call(compareQuotesTool, {
      quote_ids: ["quote_prov_001", "quote_prov_002", "quote_prov_003"],
    });
    expect(out.ranking[0].total_score).toBeGreaterThanOrEqual(
      out.ranking[1].total_score,
    );
    expect(out.recommended_quote_id).toBe(out.ranking[0].quote_id);
  });

  it("send_counter_offer responde accepted/counter/rejected", async () => {
    const accepted = await call(sendCounterOfferTool, {
      quote_id: "quote_prov_001",
      counter: { amount: 40_000, timeline_days: 90, terms: "30/70" },
    });
    expect(accepted.status).toBe("accepted");

    const rejected = await call(sendCounterOfferTool, {
      quote_id: "quote_prov_001",
      counter: { amount: 10_000, timeline_days: 90, terms: "30/70" },
    });
    expect(rejected.status).toBe("rejected");
  });

  it("get_contract incluye penalidad y ley colombiana", async () => {
    const out = await call(getContractTool, { quote_id: "quote_test_25k" });
    expect(out.contract.governing_law).toMatch(/colomb/i);
    expect(out.contract.penalties.length).toBeGreaterThan(0);
  });

  it("sign_contract activa escrow", async () => {
    const out = await call(signContractTool, {
      contract_id: "contract_x",
      buyer_id: BUYER_ID,
    });
    expect(out.status).toBe("signed");
    expect(out.escrow_activated).toBe(true);
  });
});

describe("playbook tool", () => {
  it("retorna contenido para cada sección válida", async () => {
    for (const section of PLAYBOOK_SECTIONS) {
      const out = await call(getPlaybookSectionTool, {
        section,
        buyer_id: BUYER_ID,
      });
      expect(out.section).toBe(section);
      expect(out.content.length).toBeGreaterThan(0);
    }
  });

  it("lanza error para una sección inválida", () => {
    expect(() => getPlaybookSection("no_existe")).toThrow(/inválida/i);
  });
});

describe("determinismo de los mocks", () => {
  it("search_providers: mismo input -> mismo output", () => {
    const a = mcp.searchProviders({ experience_years: 3 });
    const b = mcp.searchProviders({ experience_years: 3 });
    expect(a).toEqual(b);
  });

  it("get_provider_profile: mismo input -> mismo output", () => {
    const a = mcp.getProviderProfile("prov_003");
    const b = mcp.getProviderProfile("prov_003");
    expect(a).toEqual(b);
  });

  it("compare_quotes: mismo input -> mismo output", () => {
    const ids = ["quote_prov_001", "quote_prov_002", "quote_prov_003"];
    expect(mcp.compareQuotes(ids)).toEqual(mcp.compareQuotes(ids));
  });
});
