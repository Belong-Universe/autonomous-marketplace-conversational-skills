/**
 * Skill: flujo de cotización (quotation-flow).
 *
 * Orquesta el pre-contrato: cargar reglas del playbook -> buscar proveedores
 * -> perfilar -> enviar RFP -> recibir cotizaciones -> comparar y recomendar.
 * Todo determinista y sin LLM: la inteligencia vive en el playbook y los mocks.
 */

import { createWorkflow, createStep } from "@mastra/core/workflows";
import { z } from "zod";
import * as mcp from "../data/mcp-responses-mock";
import { loadSection } from "../tools/playbook";
import { PLAYBOOK_CONSTANTS } from "../data/playbook-mock";

// Estado que se acumula a lo largo del flujo. Cada step lo enriquece.
const quotationState = z.object({
  buyer_id: z.string(),
  need: z.object({
    description: z.string(),
    requirements: z.array(z.string()),
    deadline: z.string(),
    budget: z.number(),
  }),
  rfp_rules: z.string().optional(),
  provider_prefs: z.string().optional(),
  providers: z.array(z.any()).optional(),
  profiles: z.array(z.any()).optional(),
  rfp_id: z.string().optional(),
  quotes: z.array(z.any()).optional(),
  comparison: z.any().optional(),
  recommendation: z.string().optional(),
});

type QuotationState = z.infer<typeof quotationState>;

// 1. Cargar reglas de RFP desde el playbook.
const loadRfpRules = createStep({
  id: "load_rfp_rules",
  inputSchema: quotationState,
  outputSchema: quotationState,
  execute: async ({ inputData }) => ({
    ...inputData,
    rfp_rules: loadSection("rfp_rules", inputData.buyer_id),
  }),
});

// 2. Cargar preferencias de proveedor desde el playbook.
const loadProviderPrefs = createStep({
  id: "load_provider_prefs",
  inputSchema: quotationState,
  outputSchema: quotationState,
  execute: async ({ inputData }) => ({
    ...inputData,
    provider_prefs: loadSection("provider_preferences", inputData.buyer_id),
  }),
});

// 3. Buscar proveedores usando las preferencias (mín. 3 años de experiencia).
const searchProvidersStep = createStep({
  id: "search_providers",
  inputSchema: quotationState,
  outputSchema: quotationState,
  execute: async ({ inputData }) => ({
    ...inputData,
    providers: mcp.searchProviders({
      category: "desarrollo_movil",
      experience_years: 3,
      budget_range: { min: 0, max: inputData.need.budget },
    }),
  }),
});

// 4. Obtener el perfil completo de los 3 mejor calificados.
const getProviderProfiles = createStep({
  id: "get_provider_profiles",
  inputSchema: quotationState,
  outputSchema: quotationState,
  execute: async ({ inputData }) => {
    const top3 = (inputData.providers ?? []).slice(0, 3);
    return {
      ...inputData,
      providers: top3,
      profiles: top3.map((p: any) => mcp.getProviderProfile(p.id)),
    };
  },
});

// 5. Enviar el RFP a los 3 proveedores seleccionados.
const sendRfpStep = createStep({
  id: "send_rfp",
  inputSchema: quotationState,
  outputSchema: quotationState,
  execute: async ({ inputData }) => {
    const providerIds = (inputData.providers ?? []).map((p: any) => p.id);
    const result = mcp.sendRfp(providerIds, {
      description: inputData.need.description,
      requirements: inputData.need.requirements,
      deadline: inputData.need.deadline,
      budget: inputData.need.budget,
    });
    return { ...inputData, rfp_id: result.rfp_id };
  },
});

// 6. Esperar/recoger las cotizaciones del RFP.
const waitForQuotes = createStep({
  id: "wait_for_quotes",
  inputSchema: quotationState,
  outputSchema: quotationState,
  execute: async ({ inputData }) => ({
    ...inputData,
    quotes: mcp.getQuotes(inputData.rfp_id!),
  }),
});

// 7. Comparar las cotizaciones y 8. recomendar la mejor.
const compareAndRecommend = createStep({
  id: "compare_quotes",
  inputSchema: quotationState,
  outputSchema: quotationState,
  execute: async ({ inputData }) => {
    const quoteIds = (inputData.quotes ?? []).map((q: any) => q.quote_id);
    const comparison = mcp.compareQuotes(quoteIds);
    const best = comparison.ranking[0];
    const overBudget = best.amount > inputData.need.budget;
    const recommendation = overBudget
      ? `Recomiendo ${best.provider_id} (score ${best.total_score}), ` +
        `pero supera el presupuesto: requiere revisión. ` +
        `Prioriza time-to-market si la diferencia es < ${(
          PLAYBOOK_CONSTANTS.time_to_market_priority_pct * 100
        ).toFixed(0)}%.`
      : `Recomiendo la cotización ${best.quote_id} de ${best.provider_id} ` +
        `(score ${best.total_score}, USD ${best.amount.toLocaleString("en-US")}, ` +
        `${best.timeline_days} días). Cumple presupuesto y preferencias.`;
    return { ...inputData, comparison, recommendation };
  },
});

export const quotationFlow = createWorkflow({
  id: "quotation-flow",
  description:
    "Skill de cotización: carga reglas del playbook, busca y perfila " +
    "proveedores, envía el RFP, recibe cotizaciones y recomienda la mejor.",
  inputSchema: quotationState,
  outputSchema: quotationState,
})
  .then(loadRfpRules)
  .then(loadProviderPrefs)
  .then(searchProvidersStep)
  .then(getProviderProfiles)
  .then(sendRfpStep)
  .then(waitForQuotes)
  .then(compareAndRecommend);

quotationFlow.commit();

export type { QuotationState };
