/**
 * Skill: flujo de negociación (negotiation-flow).
 *
 * Evalúa una cotización contra el BATNA del playbook, prepara una
 * contrapropuesta dentro de los límites permitidos (concesión máxima, nunca
 * por debajo del BATNA, sin tocar los términos de pago) y resuelve el
 * resultado: aceptado, rechazado o escalar.
 */

import { createWorkflow, createStep } from "@mastra/core/workflows";
import { z } from "zod";
import * as mcp from "../data/mcp-responses-mock";
import { loadSection } from "../tools/playbook";
import { PLAYBOOK_CONSTANTS } from "../data/playbook-mock";

const resultSchema = z
  .object({
    status: z.enum(["accepted", "rejected", "escalate"]),
    final_amount: z.number().optional(),
    reason: z.string(),
  })
  .optional();

const negotiationState = z.object({
  buyer_id: z.string(),
  quote_id: z.string(),
  negotiation_rules: z.string().optional(),
  budget_rules: z.string().optional(),
  quote: z.any().optional(),
  analysis: z
    .object({ decision: z.enum(["accept_as_is", "negotiate"]), reason: z.string() })
    .optional(),
  counter: z
    .object({
      amount: z.number(),
      timeline_days: z.number(),
      terms: z.string(),
    })
    .optional(),
  seller_response: z.any().optional(),
  result: resultSchema,
});

type NegotiationState = z.infer<typeof negotiationState>;

const BATNA = PLAYBOOK_CONSTANTS.batna_usd;
const BUDGET_MAX = PLAYBOOK_CONSTANTS.budget_max_usd;
const MAX_CONCESSION = PLAYBOOK_CONSTANTS.max_price_concession_pct;

// 1. Cargar reglas de negociación.
const loadNegotiationRules = createStep({
  id: "load_negotiation_rules",
  inputSchema: negotiationState,
  outputSchema: negotiationState,
  execute: async ({ inputData }) => ({
    ...inputData,
    negotiation_rules: loadSection("negotiation", inputData.buyer_id),
  }),
});

// 2. Cargar reglas de presupuesto.
const loadBudget = createStep({
  id: "load_budget",
  inputSchema: negotiationState,
  outputSchema: negotiationState,
  execute: async ({ inputData }) => ({
    ...inputData,
    budget_rules: loadSection("budget", inputData.buyer_id),
  }),
});

// 3. Analizar la cotización contra el BATNA.
const analyzeQuote = createStep({
  id: "analyze_quote",
  inputSchema: negotiationState,
  outputSchema: negotiationState,
  execute: async ({ inputData }) => {
    const quote = mcp.getQuoteById(inputData.quote_id);
    const analysis =
      quote.amount <= BATNA
        ? {
            decision: "accept_as_is" as const,
            reason: `La cotización (USD ${quote.amount.toLocaleString("en-US")}) ya es mejor que el BATNA (USD ${BATNA.toLocaleString("en-US")}). Conviene aceptar.`,
          }
        : {
            decision: "negotiate" as const,
            reason: `La cotización (USD ${quote.amount.toLocaleString("en-US")}) supera el BATNA (USD ${BATNA.toLocaleString("en-US")}). Negociar a la baja.`,
          };
    return { ...inputData, quote, analysis };
  },
});

// 4. Preparar la contrapropuesta respetando los límites del playbook.
const prepareCounter = createStep({
  id: "prepare_counter",
  inputSchema: negotiationState,
  outputSchema: negotiationState,
  execute: async ({ inputData }) => {
    const quote = inputData.quote;
    if (inputData.analysis?.decision === "accept_as_is") {
      return {
        ...inputData,
        result: {
          status: "accepted" as const,
          final_amount: quote.amount,
          reason: inputData.analysis.reason,
        },
      };
    }
    // Pedir hasta la concesión máxima, sin superar el presupuesto...
    const desired = Math.min(
      Math.round(quote.amount * (1 - MAX_CONCESSION)),
      BUDGET_MAX,
    );
    // ...pero NUNCA por debajo del BATNA.
    const counterAmount = Math.max(desired, BATNA);
    return {
      ...inputData,
      counter: {
        amount: counterAmount,
        timeline_days: Math.max(quote.timeline_days - 10, 30),
        terms: "Pago 30/70 (no negociable)",
      },
    };
  },
});

// 5. Enviar la contrapropuesta al proveedor.
const sendCounter = createStep({
  id: "send_counter",
  inputSchema: negotiationState,
  outputSchema: negotiationState,
  execute: async ({ inputData }) => {
    if (inputData.result || !inputData.counter) return inputData; // ya resuelto
    return {
      ...inputData,
      seller_response: mcp.sendCounterOffer(inputData.quote_id, inputData.counter),
    };
  },
});

// 6. Evaluar la respuesta del proveedor y 7. resolver.
const evaluateResponse = createStep({
  id: "evaluate_response",
  inputSchema: negotiationState,
  outputSchema: negotiationState,
  execute: async ({ inputData }) => {
    if (inputData.result) return inputData; // accept_as_is

    const sr = inputData.seller_response;
    if (sr.status === "accepted") {
      return {
        ...inputData,
        result: {
          status: "accepted" as const,
          final_amount: sr.final_amount,
          reason: "El proveedor aceptó la contrapropuesta dentro de límites.",
        },
      };
    }
    if (sr.status === "counter") {
      const cp = sr.counter_proposal;
      const withinBudget = cp.amount <= BUDGET_MAX && cp.amount >= BATNA;
      return {
        ...inputData,
        result: withinBudget
          ? {
              status: "accepted" as const,
              final_amount: cp.amount,
              reason: `Aceptamos la contraoferta del proveedor (USD ${cp.amount.toLocaleString("en-US")}): dentro de presupuesto y por encima del BATNA.`,
            }
          : {
              status: "escalate" as const,
              reason: `La contraoferta (USD ${cp.amount.toLocaleString("en-US")}) excede el presupuesto o cae bajo el BATNA. Escalar al CTO.`,
            },
      };
    }
    // rejected
    return {
      ...inputData,
      result: {
        status: "escalate" as const,
        reason:
          "El proveedor rechazó la contrapropuesta. No hay zona de acuerdo sobre el BATNA: escalar al CTO.",
      },
    };
  },
});

export const negotiationFlow = createWorkflow({
  id: "negotiation-flow",
  description:
    "Skill de negociación: evalúa una cotización contra el BATNA, prepara una " +
    "contrapropuesta dentro de los límites del playbook y resuelve " +
    "(aceptado/rechazado/escalar).",
  inputSchema: negotiationState,
  outputSchema: negotiationState,
})
  .then(loadNegotiationRules)
  .then(loadBudget)
  .then(analyzeQuote)
  .then(prepareCounter)
  .then(sendCounter)
  .then(evaluateResponse);

negotiationFlow.commit();

export type { NegotiationState };
