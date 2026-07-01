/**
 * Tests unitarios del playbook. No usan el LLM.
 */
import { describe, it, expect } from "vitest";
import {
  PLAYBOOK_SECTIONS,
  PLAYBOOK_CONTENT,
  PLAYBOOK_CONSTANTS,
  getPlaybookSection,
} from "../../src/mastra/data/playbook-mock";

describe("playbook: contenido", () => {
  it("tiene exactamente 10 secciones", () => {
    expect(PLAYBOOK_SECTIONS).toHaveLength(10);
  });

  it("todas las secciones tienen contenido no vacío", () => {
    for (const section of PLAYBOOK_SECTIONS) {
      expect(PLAYBOOK_CONTENT[section].trim().length).toBeGreaterThan(0);
    }
  });

  it("la sección negotiation contiene el monto del BATNA", () => {
    expect(getPlaybookSection("negotiation")).toContain(
      PLAYBOOK_CONSTANTS.batna_usd.toLocaleString("en-US"),
    );
  });

  it("la sección approval_gates contiene el umbral de $30k", () => {
    expect(getPlaybookSection("approval_gates")).toContain(
      PLAYBOOK_CONSTANTS.human_approval_threshold_usd.toLocaleString("en-US"),
    );
    expect(PLAYBOOK_CONSTANTS.human_approval_threshold_usd).toBe(30_000);
  });

  it("la sección budget contiene los términos de pago 30/70", () => {
    expect(getPlaybookSection("budget")).toContain("30%");
    expect(getPlaybookSection("budget")).toContain("70%");
  });

  it("getPlaybookSection lanza error para sección inválida", () => {
    expect(() => getPlaybookSection("no_existe")).toThrow(/inválida/i);
  });
});
