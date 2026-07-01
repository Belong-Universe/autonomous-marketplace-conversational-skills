/**
 * Tool de consulta del playbook del buyer.
 *
 * El agente DEBE consultar la sección relevante antes de tomar cualquier
 * decisión de negocio. Cada consulta se loggea para dejar rastro de auditoría
 * (qué sección guió cada decisión).
 */

import { createTool } from "@mastra/core/tools";
import { z } from "zod";
import {
  PLAYBOOK_SECTIONS,
  getPlaybookSection,
} from "../data/playbook-mock";

/** Registro en memoria de las consultas al playbook (auditoría del demo). */
export const playbookAuditLog: { section: string; buyer_id: string }[] = [];

/**
 * Carga una sección del playbook dejando rastro de auditoría.
 * Lo usan tanto la tool como los workflows para compartir el mismo log.
 */
export function loadSection(section: string, buyer_id: string): string {
  playbookAuditLog.push({ section, buyer_id });
  console.log(`[playbook] buyer=${buyer_id} consultó la sección "${section}"`);
  return getPlaybookSection(section);
}

/** Solo para tests: limpia el log de auditoría. */
export function __resetAuditLog(): void {
  playbookAuditLog.length = 0;
}

export const getPlaybookSectionTool = createTool({
  id: "get_playbook_section",
  description:
    "Consulta una sección del playbook del buyer para guiar decisiones. " +
    "Úsala SIEMPRE antes de buscar proveedores, negociar o firmar.",
  inputSchema: z.object({
    section: z.enum(PLAYBOOK_SECTIONS),
    buyer_id: z.string(),
  }),
  outputSchema: z.object({
    section: z.string(),
    content: z.string(),
  }),
  execute: async (inputData) => {
    const { section, buyer_id } = inputData;
    // Auditoría compartida con los workflows (ver loadSection).
    return { section, content: loadSection(section, buyer_id) };
  },
});
