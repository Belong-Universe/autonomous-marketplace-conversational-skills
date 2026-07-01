/**
 * MCP mockeado de Belong Universe expuesto como tools de Mastra.
 *
 * Cada tool valida su entrada/salida con Zod y delega la lógica a la capa de
 * servicio determinista (data/mcp-responses-mock.ts). Cero llamadas HTTP.
 * Son las 12 capacidades del buyer dentro del marketplace.
 */

import { createTool } from "@mastra/core/tools";
import { z } from "zod";
import * as mcp from "../data/mcp-responses-mock";

// --- Schemas reutilizables ------------------------------------------------

const providerSchema = z.object({
  id: z.string(),
  name: z.string(),
  rating: z.number(),
  location: z.string(),
  specialties: z.array(z.string()),
  hourly_rate: z.number(),
  availability: z.string(),
  experience_years: z.number(),
});

// --- 1. search_providers ---------------------------------------------------

export const searchProvidersTool = createTool({
  id: "search_providers",
  description:
    "Busca proveedores en Belong Universe filtrando por categoría, ubicación, rango de presupuesto y años de experiencia.",
  inputSchema: z.object({
    category: z.string().optional(),
    location: z.string().optional(),
    budget_range: z
      .object({ min: z.number(), max: z.number() })
      .optional(),
    experience_years: z.number().optional(),
  }),
  outputSchema: z.object({ providers: z.array(providerSchema) }),
  execute: async (inputData) => ({ providers: mcp.searchProviders(inputData) }),
});

// --- 2. get_provider_profile ----------------------------------------------

export const getProviderProfileTool = createTool({
  id: "get_provider_profile",
  description:
    "Obtiene el perfil completo de un proveedor: portfolio, equipo, stack, referencias, certificaciones y tiempo de respuesta.",
  inputSchema: z.object({ provider_id: z.string() }),
  outputSchema: z.object({ profile: z.any() }),
  execute: async (inputData) => ({
    profile: mcp.getProviderProfile(inputData.provider_id),
  }),
});

// --- 3. send_rfp -----------------------------------------------------------

export const sendRfpTool = createTool({
  id: "send_rfp",
  description:
    "Envía un RFP (solicitud de propuesta) a uno o varios proveedores y devuelve el rfp_id con la confirmación de envío.",
  inputSchema: z.object({
    provider_ids: z.array(z.string()),
    rfp: z.object({
      description: z.string(),
      requirements: z.array(z.string()),
      deadline: z.string(),
      budget: z.number(),
    }),
  }),
  outputSchema: z.object({
    rfp_id: z.string(),
    sent_to: z.array(
      z.object({
        provider_id: z.string(),
        status: z.literal("sent"),
        channel: z.string(),
      }),
    ),
    deadline: z.string(),
  }),
  execute: async (inputData) => mcp.sendRfp(inputData.provider_ids, inputData.rfp),
});

// --- 4. get_quotes ---------------------------------------------------------

const publicQuoteSchema = z.object({
  quote_id: z.string(),
  provider_id: z.string(),
  amount: z.number(),
  timeline_days: z.number(),
  payment_terms: z.string(),
  technical_proposal: z.string(),
  team_assigned: z.array(z.string()),
});

export const getQuotesTool = createTool({
  id: "get_quotes",
  description:
    "Obtiene las cotizaciones recibidas para un RFP, con monto, timeline, términos de pago, propuesta técnica y equipo asignado.",
  inputSchema: z.object({ rfp_id: z.string() }),
  outputSchema: z.object({ quotes: z.array(publicQuoteSchema) }),
  execute: async (inputData) => ({ quotes: mcp.getQuotes(inputData.rfp_id) }),
});

// --- 5. compare_quotes -----------------------------------------------------

export const compareQuotesTool = createTool({
  id: "compare_quotes",
  description:
    "Compara cotizaciones con scoring por criterio (precio, timeline, experiencia, propuesta técnica) y recomienda la mejor.",
  inputSchema: z.object({ quote_ids: z.array(z.string()) }),
  outputSchema: z.object({
    ranking: z.array(z.any()),
    recommended_quote_id: z.string(),
  }),
  execute: async (inputData) => mcp.compareQuotes(inputData.quote_ids),
});

// --- 6. send_counter_offer -------------------------------------------------

export const sendCounterOfferTool = createTool({
  id: "send_counter_offer",
  description:
    "Envía una contrapropuesta a una cotización y devuelve la respuesta del proveedor (accepted / counter / rejected).",
  inputSchema: z.object({
    quote_id: z.string(),
    counter: z.object({
      amount: z.number(),
      timeline_days: z.number(),
      terms: z.string(),
    }),
  }),
  outputSchema: z.object({
    status: z.enum(["accepted", "counter", "rejected"]),
    quote_id: z.string(),
    final_amount: z.number().optional(),
    counter_proposal: z
      .object({
        amount: z.number(),
        timeline_days: z.number(),
        terms: z.string(),
      })
      .optional(),
    message: z.string(),
  }),
  execute: async (inputData) =>
    mcp.sendCounterOffer(inputData.quote_id, inputData.counter),
});

// --- 7. get_contract -------------------------------------------------------

export const getContractTool = createTool({
  id: "get_contract",
  description:
    "Obtiene el contrato borrador de una cotización con todas las cláusulas, cronograma de pagos, entregables y penalidades.",
  inputSchema: z.object({ quote_id: z.string() }),
  outputSchema: z.object({ contract: z.any() }),
  execute: async (inputData) => ({
    contract: mcp.getContract(inputData.quote_id),
  }),
});

// --- 8. request_nda --------------------------------------------------------

export const requestNdaTool = createTool({
  id: "request_nda",
  description:
    "Solicita un NDA a un proveedor antes de compartir especificaciones. Devuelve nda_id y link de firma.",
  inputSchema: z.object({ provider_id: z.string() }),
  outputSchema: z.object({
    nda_id: z.string(),
    provider_id: z.string(),
    status: z.literal("pending_signature"),
    sign_url: z.string(),
  }),
  execute: async (inputData) => mcp.requestNda(inputData.provider_id),
});

// --- 9. sign_contract ------------------------------------------------------

export const signContractTool = createTool({
  id: "sign_contract",
  description:
    "Firma un contrato en nombre del buyer. Activa el escrow y devuelve la fecha de inicio.",
  inputSchema: z.object({ contract_id: z.string(), buyer_id: z.string() }),
  outputSchema: z.object({
    contract_id: z.string(),
    buyer_id: z.string(),
    status: z.literal("signed"),
    escrow_activated: z.boolean(),
    start_date: z.string(),
  }),
  execute: async (inputData) =>
    mcp.signContract(inputData.contract_id, inputData.buyer_id),
});

// --- 10. get_my_contracts --------------------------------------------------

export const getMyContractsTool = createTool({
  id: "get_my_contracts",
  description: "Lista los contratos activos e históricos del buyer.",
  inputSchema: z.object({ buyer_id: z.string() }),
  outputSchema: z.object({ contracts: z.array(z.any()) }),
  execute: async (inputData) => ({
    contracts: mcp.getMyContracts(inputData.buyer_id),
  }),
});

// --- 11. open_dispute ------------------------------------------------------

export const openDisputeTool = createTool({
  id: "open_dispute",
  description:
    "Abre una disputa sobre un contrato usando el mecanismo de Belong Universe (árbitro técnico externo).",
  inputSchema: z.object({
    contract_id: z.string(),
    reason: z.string(),
    evidence: z.string(),
  }),
  outputSchema: z.object({
    dispute_id: z.string(),
    contract_id: z.string(),
    status: z.literal("open"),
    arbiter: z.string(),
    message: z.string(),
  }),
  execute: async (inputData) =>
    mcp.openDispute(inputData.contract_id, inputData.reason, inputData.evidence),
});

// --- 12. get_notifications -------------------------------------------------

export const getNotificationsTool = createTool({
  id: "get_notifications",
  description:
    "Obtiene las notificaciones pendientes del buyer (cotizaciones recibidas, respuestas a contrapropuestas, etc.).",
  inputSchema: z.object({ buyer_id: z.string() }),
  outputSchema: z.object({ notifications: z.array(z.any()) }),
  execute: async (inputData) => ({
    notifications: mcp.getNotifications(inputData.buyer_id),
  }),
});

/** Todas las tools del MCP, listas para registrar en el agente. */
export const belongMcpTools = {
  search_providers: searchProvidersTool,
  get_provider_profile: getProviderProfileTool,
  send_rfp: sendRfpTool,
  get_quotes: getQuotesTool,
  compare_quotes: compareQuotesTool,
  send_counter_offer: sendCounterOfferTool,
  get_contract: getContractTool,
  request_nda: requestNdaTool,
  sign_contract: signContractTool,
  get_my_contracts: getMyContractsTool,
  open_dispute: openDisputeTool,
  get_notifications: getNotificationsTool,
};
