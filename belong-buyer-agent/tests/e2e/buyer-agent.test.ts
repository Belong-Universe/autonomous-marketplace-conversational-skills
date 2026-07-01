/**
 * Test end-to-end del buyer agent con LLM REAL (claude-sonnet-4-6).
 *
 * Requiere ANTHROPIC_API_KEY en .env. Es el único test que llama al modelo.
 * Verifica comportamiento de alto nivel: que consulta el playbook, que respeta
 * el presupuesto/BATNA y que responde con el formato estructurado pedido.
 */
import { describe, it, expect, beforeEach } from "vitest";
import { buyerAgent } from "../../src/mastra/agents/buyer-agent";
import {
  playbookAuditLog,
  __resetAuditLog,
} from "../../src/mastra/tools/playbook";
import * as mcp from "../../src/mastra/data/mcp-responses-mock";

const hasKey = !!process.env.ANTHROPIC_API_KEY;
const d = hasKey ? describe : describe.skip;

// Comprueba que el texto trae las 3 secciones del formato de respuesta.
function hasStructuredFormat(text: string): boolean {
  const t = text.toLowerCase();
  return (
    t.includes("decisión") &&
    t.includes("basado en playbook") &&
    t.includes("próximo paso")
  );
}

beforeEach(() => {
  mcp.__resetMockState();
  __resetAuditLog();
});

d("e2e: buyer agent (LLM real)", () => {
  it(
    "busca, cotiza y recomienda consultando el playbook",
    async () => {
      const res = await buyerAgent.generate(
        "Necesito contratar desarrollo de una app móvil. Busca providers, " +
          "solicita cotizaciones y dime cuál recomiendas.",
        { maxSteps: 14 },
      );

      // Consultó el playbook al menos una vez.
      expect(playbookAuditLog.length).toBeGreaterThanOrEqual(1);
      // Respondió con el formato estructurado.
      expect(hasStructuredFormat(res.text)).toBe(true);
      // Demostró conciencia del presupuesto: no recomienda por encima del techo
      // sin marcarlo (menciona el presupuesto y/o la necesidad de negociar/aprobar).
      const t = res.text.toLowerCase();
      expect(t).toMatch(/presupuesto|50[.,]?000|negociar|aprobaci/);
      // La opción premium fuera de presupuesto (Pampa Squad / $61k) no es la ganadora.
      expect(t).not.toMatch(/decisión[^]*recomendar a \**pampa squad/);
    },
    60_000,
  );

  it(
    "negocia una cotización sobre presupuesto respetando el BATNA",
    async () => {
      const res = await buyerAgent.generate(
        "Tengo esta cotización: DevCo propone $48k, 90 días, pago 50/50. " +
          "Negocia según mi playbook.",
        { maxSteps: 14 },
      );

      const t = res.text.toLowerCase();
      // Identificó que está sobre presupuesto.
      expect(t).toMatch(/presupuesto|sobre el|excede|48/);
      // Mencionó el BATNA en su razonamiento.
      expect(t).toMatch(/batna|35\.?000|35,000|alternativa/);
      // Mantuvo el formato estructurado.
      expect(hasStructuredFormat(res.text)).toBe(true);
    },
    60_000,
  );
});
