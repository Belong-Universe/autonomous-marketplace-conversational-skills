/**
 * Respuestas mockeadas del MCP de Belong Universe.
 *
 * Esta es la capa de "servicio": funciones puras y deterministas que simulan
 * el backend del marketplace. NO hay llamadas HTTP. Tanto las tools de Mastra
 * (belong-mcp.ts) como los workflows consumen estas funciones, de modo que el
 * comportamiento sea idéntico y testeable sin LLM ni red.
 *
 * Regla de oro: mismo input -> mismo output. Los datos son ficticios pero
 * verosímiles (empresas colombianas/LATAM, montos en USD).
 */

// ---------------------------------------------------------------------------
// Tipos del dominio
// ---------------------------------------------------------------------------

export interface Provider {
  id: string;
  name: string;
  rating: number;
  location: string;
  specialties: string[];
  hourly_rate: number; // USD/hora
  availability: string;
  experience_years: number;
}

export interface ProviderProfile extends Provider {
  portfolio: string[];
  team_size: number;
  tech_stack: string[];
  references: { client: string; project: string; verifiable: boolean }[];
  certifications: string[];
  response_time_avg_hours: number;
}

export interface Quote {
  quote_id: string;
  provider_id: string;
  amount: number; // USD
  timeline_days: number;
  payment_terms: string;
  technical_proposal: string;
  team_assigned: string[];
  /** Piso interno del proveedor (no se expone al buyer en respuestas reales). */
  seller_floor: number;
}

// ---------------------------------------------------------------------------
// Catálogo determinista de proveedores (LATAM)
// ---------------------------------------------------------------------------

const PROVIDER_CATALOG: Provider[] = [
  {
    id: "prov_001",
    name: "Nubox Studios",
    rating: 4.8,
    location: "Bogotá, Colombia",
    specialties: ["React Native", "Node.js", "Diseño UX"],
    hourly_rate: 45,
    availability: "Disponible en 2 semanas",
    experience_years: 5,
  },
  {
    id: "prov_002",
    name: "Tul Devs",
    rating: 4.6,
    location: "Medellín, Colombia",
    specialties: ["React Native", "Firebase", "QA Automation"],
    hourly_rate: 40,
    availability: "Disponible inmediato",
    experience_years: 4,
  },
  {
    id: "prov_003",
    name: "Cóndor Labs",
    rating: 4.9,
    location: "Bogotá, Colombia",
    specialties: ["React Native", "AWS", "DevOps"],
    hourly_rate: 55,
    availability: "Disponible en 1 mes",
    experience_years: 6,
  },
  {
    id: "prov_004",
    name: "Maguey Mobile",
    rating: 4.5,
    location: "Ciudad de México, México",
    specialties: ["React Native", "GraphQL"],
    hourly_rate: 38,
    availability: "Disponible en 3 semanas",
    experience_years: 3,
  },
  {
    id: "prov_005",
    name: "Pampa Squad",
    rating: 4.7,
    location: "Buenos Aires, Argentina",
    specialties: ["React Native", "Kotlin", "Swift"],
    hourly_rate: 60,
    availability: "Disponible en 2 semanas",
    experience_years: 7,
  },
];

const PROFILE_EXTRAS: Record<
  string,
  Omit<ProviderProfile, keyof Provider>
> = {
  prov_001: {
    portfolio: ["App de delivery NuboxEats", "Banca móvil para Banco Andino"],
    team_size: 8,
    tech_stack: ["React Native", "Expo", "Node.js", "PostgreSQL"],
    references: [
      { client: "Banco Andino", project: "Banca móvil", verifiable: true },
      { client: "NuboxEats", project: "App de delivery", verifiable: true },
    ],
    certifications: ["AWS Certified Developer", "ISO 27001"],
    response_time_avg_hours: 4,
  },
  prov_002: {
    portfolio: ["Marketplace agro Tul", "App de logística última milla"],
    team_size: 5,
    tech_stack: ["React Native", "Firebase", "TypeScript"],
    references: [
      { client: "Tul", project: "Marketplace agro", verifiable: true },
      { client: "RappiCargo", project: "Logística", verifiable: true },
    ],
    certifications: ["Google Associate Cloud Engineer"],
    response_time_avg_hours: 6,
  },
  prov_003: {
    portfolio: ["Super app fintech", "Plataforma de salud digital"],
    team_size: 12,
    tech_stack: ["React Native", "AWS", "Terraform", "GraphQL"],
    references: [
      { client: "Bold", project: "Super app fintech", verifiable: true },
      { client: "1DOC3", project: "Salud digital", verifiable: true },
      { client: "Rappi", project: "Módulo de pagos", verifiable: true },
    ],
    certifications: ["AWS Solutions Architect", "ISO 27001", "SOC 2"],
    response_time_avg_hours: 3,
  },
  prov_004: {
    portfolio: ["App de movilidad", "E-commerce moda"],
    team_size: 6,
    tech_stack: ["React Native", "GraphQL", "Hasura"],
    references: [
      { client: "Kavak", project: "App de movilidad", verifiable: true },
      { client: "Liverpool", project: "E-commerce", verifiable: false },
    ],
    certifications: ["Scrum Master"],
    response_time_avg_hours: 8,
  },
  prov_005: {
    portfolio: ["App de banca regional", "Plataforma de streaming"],
    team_size: 15,
    tech_stack: ["React Native", "Kotlin", "Swift", "Kubernetes"],
    references: [
      { client: "Banco Galicia", project: "Banca regional", verifiable: true },
      { client: "Flow", project: "Streaming", verifiable: true },
    ],
    certifications: ["AWS Solutions Architect", "CMMI Nivel 3"],
    response_time_avg_hours: 5,
  },
};

// ---------------------------------------------------------------------------
// Registro determinista de cotizaciones
// ---------------------------------------------------------------------------

/**
 * Cotizaciones fijas por `quote_id`. Las primeras 5 corresponden a los
 * proveedores del catálogo; las demás son escenarios pensados para los tests
 * (firma automática, aprobación humana, negociación, sin acuerdo).
 */
const QUOTE_REGISTRY: Record<string, Quote> = {
  quote_prov_001: {
    quote_id: "quote_prov_001",
    provider_id: "prov_001",
    amount: 38_000,
    timeline_days: 95,
    payment_terms: "30/70 (anticipo/entrega)",
    technical_proposal:
      "Arquitectura React Native + Expo, backend Node.js, CI/CD y pruebas E2E.",
    team_assigned: ["1 Tech Lead", "3 devs RN", "1 QA"],
    seller_floor: 36_000,
  },
  quote_prov_002: {
    quote_id: "quote_prov_002",
    provider_id: "prov_002",
    amount: 44_000,
    timeline_days: 80,
    payment_terms: "30/70 (anticipo/entrega)",
    technical_proposal:
      "React Native + Firebase, enfoque en time-to-market y QA automation.",
    team_assigned: ["1 Tech Lead", "2 devs RN", "1 QA"],
    seller_floor: 42_000,
  },
  quote_prov_003: {
    quote_id: "quote_prov_003",
    provider_id: "prov_003",
    amount: 52_000,
    timeline_days: 70,
    payment_terms: "30/70 (anticipo/entrega)",
    technical_proposal:
      "React Native + AWS, equipo senior, observabilidad y escalabilidad.",
    team_assigned: ["1 Arquitecto", "1 Tech Lead", "3 devs RN", "1 DevOps"],
    seller_floor: 50_000,
  },
  quote_prov_004: {
    quote_id: "quote_prov_004",
    provider_id: "prov_004",
    amount: 33_000,
    timeline_days: 110,
    payment_terms: "50/50 (anticipo/entrega)",
    technical_proposal: "React Native + GraphQL, propuesta económica ajustada.",
    team_assigned: ["1 Tech Lead", "2 devs RN"],
    seller_floor: 31_000,
  },
  quote_prov_005: {
    quote_id: "quote_prov_005",
    provider_id: "prov_005",
    amount: 61_000,
    timeline_days: 65,
    payment_terms: "40/60 (anticipo/entrega)",
    technical_proposal:
      "Equipo grande multiplataforma, entrega muy rápida, costo premium.",
    team_assigned: ["1 Arquitecto", "2 Tech Leads", "4 devs", "1 QA"],
    seller_floor: 58_000,
  },
  // --- Escenarios para tests ---
  quote_test_25k: {
    quote_id: "quote_test_25k",
    provider_id: "prov_002",
    amount: 25_000,
    timeline_days: 90,
    payment_terms: "30/70 (anticipo/entrega)",
    technical_proposal: "MVP React Native acotado, alcance reducido.",
    team_assigned: ["1 Tech Lead", "1 dev RN"],
    seller_floor: 24_000,
  },
  quote_test_45k: {
    quote_id: "quote_test_45k",
    provider_id: "prov_001",
    amount: 45_000,
    timeline_days: 80,
    payment_terms: "30/70 (anticipo/entrega)",
    technical_proposal: "App completa React Native con backend.",
    team_assigned: ["1 Tech Lead", "3 devs RN", "1 QA"],
    seller_floor: 43_000,
  },
  quote_over_budget: {
    quote_id: "quote_over_budget",
    provider_id: "prov_001",
    amount: 48_000,
    timeline_days: 90,
    payment_terms: "30/70 (anticipo/entrega)",
    technical_proposal: "App completa, cotización por encima del presupuesto.",
    team_assigned: ["1 Tech Lead", "3 devs RN", "1 QA"],
    seller_floor: 45_000,
  },
  quote_no_deal: {
    quote_id: "quote_no_deal",
    provider_id: "prov_005",
    amount: 70_000,
    timeline_days: 60,
    payment_terms: "40/60 (anticipo/entrega)",
    technical_proposal: "Propuesta premium muy por encima del presupuesto.",
    team_assigned: ["1 Arquitecto", "5 devs"],
    seller_floor: 70_000,
  },
};

/** Quotes que devuelve get_quotes para un RFP estándar (los 3 mejor calificados). */
const DEFAULT_RFP_QUOTE_IDS = ["quote_prov_003", "quote_prov_001", "quote_prov_002"];

// ---------------------------------------------------------------------------
// Utilidades
// ---------------------------------------------------------------------------

/** Hash determinista simple (djb2) para generar ids estables sin azar. */
function stableHash(input: string): string {
  let hash = 5381;
  for (let i = 0; i < input.length; i++) {
    hash = (hash * 33) ^ input.charCodeAt(i);
  }
  return (hash >>> 0).toString(16);
}

/** Mapa en memoria rfp_id -> provider_ids, poblado por send_rfp. */
const RFP_PROVIDERS = new Map<string, string[]>();

/** Devuelve una copia profunda para evitar mutaciones accidentales del mock. */
function clone<T>(value: T): T {
  return JSON.parse(JSON.stringify(value));
}

// ---------------------------------------------------------------------------
// Funciones del MCP (12 tools)
// ---------------------------------------------------------------------------

export interface SearchFilters {
  category?: string;
  location?: string;
  budget_range?: { min: number; max: number };
  experience_years?: number;
}

/** search_providers: filtra el catálogo por experiencia y ubicación. */
export function searchProviders(filters: SearchFilters): Provider[] {
  const minExp = filters.experience_years ?? 0;
  const location = filters.location?.toLowerCase();

  const matched = PROVIDER_CATALOG.filter((p) => {
    if (p.experience_years < minExp) return false;
    if (location && !p.location.toLowerCase().includes(location)) return false;
    return true;
  });

  // Orden determinista: mejor rating primero, desempate por id.
  return clone(
    matched.sort((a, b) => b.rating - a.rating || a.id.localeCompare(b.id)),
  );
}

/** get_provider_profile: perfil completo de un proveedor. */
export function getProviderProfile(providerId: string): ProviderProfile {
  const base = PROVIDER_CATALOG.find((p) => p.id === providerId);
  const extra = PROFILE_EXTRAS[providerId];
  if (!base || !extra) {
    throw new Error(`Proveedor no encontrado: ${providerId}`);
  }
  return clone({ ...base, ...extra });
}

export interface Rfp {
  description: string;
  requirements: string[];
  deadline: string;
  budget: number;
}

export interface SendRfpResult {
  rfp_id: string;
  sent_to: { provider_id: string; status: "sent"; channel: string }[];
  deadline: string;
}

/** send_rfp: envía el RFP a varios proveedores y registra el mapeo. */
export function sendRfp(providerIds: string[], rfp: Rfp): SendRfpResult {
  const sorted = [...providerIds].sort();
  const rfpId = `rfp_${stableHash(sorted.join("|") + rfp.deadline)}`;
  RFP_PROVIDERS.set(rfpId, sorted);
  return {
    rfp_id: rfpId,
    sent_to: providerIds.map((id) => ({
      provider_id: id,
      status: "sent" as const,
      channel: "Belong Universe Inbox",
    })),
    deadline: rfp.deadline,
  };
}

/** Versión pública de una cotización: oculta el piso interno del proveedor. */
export type PublicQuote = Omit<Quote, "seller_floor">;

function toPublicQuote(quote: Quote): PublicQuote {
  const { seller_floor: _omit, ...rest } = quote;
  return clone(rest);
}

/** get_quotes: cotizaciones recibidas para un RFP. */
export function getQuotes(rfpId: string): PublicQuote[] {
  const providerIds = RFP_PROVIDERS.get(rfpId);
  const quoteIds = providerIds
    ? providerIds.map((pid) => `quote_${pid}`).filter((qid) => QUOTE_REGISTRY[qid])
    : DEFAULT_RFP_QUOTE_IDS;
  return quoteIds.map((qid) => toPublicQuote(QUOTE_REGISTRY[qid]));
}

/** Lookup interno de una cotización completa (incluye piso) por id. */
export function getQuoteById(quoteId: string): Quote {
  const quote = QUOTE_REGISTRY[quoteId];
  if (!quote) throw new Error(`Cotización no encontrada: ${quoteId}`);
  return clone(quote);
}

export interface QuoteComparison {
  ranking: {
    quote_id: string;
    provider_id: string;
    amount: number;
    timeline_days: number;
    scores: {
      precio: number;
      timeline: number;
      experiencia: number;
      propuesta_tecnica: number;
    };
    total_score: number;
  }[];
  recommended_quote_id: string;
}

/** compare_quotes: scoring comparativo por criterio (0-100), ordenado. */
export function compareQuotes(quoteIds: string[]): QuoteComparison {
  const quotes = quoteIds.map((id) => getQuoteById(id));

  const minAmount = Math.min(...quotes.map((q) => q.amount));
  const minTimeline = Math.min(...quotes.map((q) => q.timeline_days));

  const ranking = quotes
    .map((q) => {
      const provider = PROVIDER_CATALOG.find((p) => p.id === q.provider_id)!;
      // Cada criterio se normaliza a 0-100 (más alto = mejor).
      const precio = Math.round((minAmount / q.amount) * 100);
      const timeline = Math.round((minTimeline / q.timeline_days) * 100);
      const experiencia = Math.round((provider.experience_years / 7) * 100);
      const propuesta_tecnica = Math.round((provider.rating / 5) * 100);
      // Pesos: precio 30%, timeline 30%, experiencia 20%, técnica 20%.
      const total_score = Math.round(
        precio * 0.3 +
          timeline * 0.3 +
          experiencia * 0.2 +
          propuesta_tecnica * 0.2,
      );
      return {
        quote_id: q.quote_id,
        provider_id: q.provider_id,
        amount: q.amount,
        timeline_days: q.timeline_days,
        scores: { precio, timeline, experiencia, propuesta_tecnica },
        total_score,
      };
    })
    .sort((a, b) => b.total_score - a.total_score);

  return { ranking, recommended_quote_id: ranking[0].quote_id };
}

export interface CounterOffer {
  amount: number;
  timeline_days: number;
  terms: string;
}

export interface CounterOfferResult {
  status: "accepted" | "counter" | "rejected";
  quote_id: string;
  final_amount?: number;
  counter_proposal?: { amount: number; timeline_days: number; terms: string };
  message: string;
}

/**
 * send_counter_offer: respuesta determinista del proveedor según su piso.
 * - counter >= piso          -> aceptado
 * - piso*0.9 <= counter < piso -> el proveedor contraoferta a su piso
 * - counter < piso*0.9       -> rechazado
 */
export function sendCounterOffer(
  quoteId: string,
  counter: CounterOffer,
): CounterOfferResult {
  const quote = getQuoteById(quoteId);
  const floor = quote.seller_floor;

  if (counter.amount >= floor) {
    return {
      status: "accepted",
      quote_id: quoteId,
      final_amount: counter.amount,
      message: "El proveedor acepta tu contrapropuesta.",
    };
  }
  if (counter.amount >= floor * 0.9) {
    return {
      status: "counter",
      quote_id: quoteId,
      counter_proposal: {
        amount: floor,
        timeline_days: counter.timeline_days,
        terms: counter.terms,
      },
      message: "El proveedor contraoferta cerca de su mínimo.",
    };
  }
  return {
    status: "rejected",
    quote_id: quoteId,
    message: "El proveedor rechaza la contrapropuesta por estar muy por debajo.",
  };
}

export interface Contract {
  contract_id: string;
  quote_id: string;
  provider_id: string;
  amount: number;
  governing_law: string;
  clauses: string[];
  payment_schedule: { milestone: string; pct: number; amount: number }[];
  deliverables: string[];
  penalties: { type: string; rate_weekly_pct: number; description: string }[];
  nda_required: boolean;
}

/** get_contract: borrador de contrato derivado de la cotización. */
export function getContract(quoteId: string): Contract {
  const quote = getQuoteById(quoteId);
  const contractId = `contract_${stableHash(quoteId)}`;
  return {
    contract_id: contractId,
    quote_id: quoteId,
    provider_id: quote.provider_id,
    amount: quote.amount,
    governing_law: "República de Colombia",
    clauses: [
      "NDA firmado previo a compartir especificaciones detalladas.",
      "Ley aplicable: legislación colombiana.",
      "Cláusula de penalidad por retraso: 2% semanal sobre el valor pendiente.",
      "Propiedad intelectual transferida al buyer contra pago final.",
    ],
    payment_schedule: [
      { milestone: "Anticipo", pct: 30, amount: Math.round(quote.amount * 0.3) },
      { milestone: "Entrega", pct: 70, amount: Math.round(quote.amount * 0.7) },
    ],
    deliverables: [
      "Código fuente en repositorio privado",
      "App publicada en App Store y Google Play",
      "Documentación técnica y de despliegue",
    ],
    penalties: [
      {
        type: "retraso",
        rate_weekly_pct: 2,
        description: "2% semanal sobre el valor pendiente por cada semana de retraso.",
      },
    ],
    nda_required: true,
  };
}

export interface NdaResult {
  nda_id: string;
  provider_id: string;
  status: "pending_signature";
  sign_url: string;
}

/** request_nda: genera un NDA mockeado con link de firma. */
export function requestNda(providerId: string): NdaResult {
  return {
    nda_id: `nda_${stableHash(providerId)}`,
    provider_id: providerId,
    status: "pending_signature",
    sign_url: `https://belong.universe/mock/nda/${stableHash(providerId)}`,
  };
}

export interface SignContractResult {
  contract_id: string;
  buyer_id: string;
  status: "signed";
  escrow_activated: boolean;
  start_date: string;
}

/** sign_contract: confirma firma y activa escrow (mock). */
export function signContract(
  contractId: string,
  buyerId: string,
): SignContractResult {
  return {
    contract_id: contractId,
    buyer_id: buyerId,
    status: "signed",
    escrow_activated: true,
    // Fecha fija y determinista (sin Date.now para mantener tests estables).
    start_date: "2026-07-01",
  };
}

export interface ContractSummary {
  contract_id: string;
  provider_name: string;
  amount: number;
  status: "active" | "completed";
}

/** get_my_contracts: contratos activos e históricos del buyer. */
export function getMyContracts(_buyerId: string): ContractSummary[] {
  return [
    {
      contract_id: "contract_hist_001",
      provider_name: "Cóndor Labs",
      amount: 28_000,
      status: "completed",
    },
    {
      contract_id: "contract_active_001",
      provider_name: "Nubox Studios",
      amount: 45_000,
      status: "active",
    },
  ];
}

export interface DisputeResult {
  dispute_id: string;
  contract_id: string;
  status: "open";
  arbiter: string;
  message: string;
}

/** open_dispute: abre una disputa con árbitro técnico externo (mock). */
export function openDispute(
  contractId: string,
  reason: string,
  _evidence: string,
): DisputeResult {
  return {
    dispute_id: `dispute_${stableHash(contractId + reason)}`,
    contract_id: contractId,
    status: "open",
    arbiter: "Árbitro técnico externo de Belong Universe",
    message: "Disputa registrada. Un árbitro técnico revisará la evidencia.",
  };
}

export interface Notification {
  id: string;
  type: "quote_received" | "counter_offer" | "contract_update" | "dispute_update";
  message: string;
  created_at: string;
}

/** get_notifications: notificaciones pendientes del buyer. */
export function getNotifications(_buyerId: string): Notification[] {
  return [
    {
      id: "notif_001",
      type: "quote_received",
      message: "Cóndor Labs envió una cotización para tu RFP de app móvil.",
      created_at: "2026-06-24T09:00:00Z",
    },
    {
      id: "notif_002",
      type: "counter_offer",
      message: "Nubox Studios respondió a tu contrapropuesta.",
      created_at: "2026-06-24T11:30:00Z",
    },
  ];
}

/** Solo para tests: reinicia el estado en memoria de RFPs. */
export function __resetMockState(): void {
  RFP_PROVIDERS.clear();
}
