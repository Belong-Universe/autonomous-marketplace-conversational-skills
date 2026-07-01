/**
 * Playbook mockeado del buyer (TechCorp S.A.S).
 *
 * El playbook es el "contrato operativo" que le dice al Buyer Agent cómo
 * comprar: cómo presupuestar, qué proveedores califican, cómo negociar,
 * hasta dónde puede firmar y cuándo debe escalar a un humano.
 *
 * Una sola fuente de verdad: tanto la tool `get_playbook_section` como los
 * workflows leen de aquí. Todo es estático y determinista (sin red).
 */

/** Identificador del buyer dueño de este playbook. */
export const BUYER_ID = "buyer_techcorp_001";

/** Las 10 secciones canónicas del Buying Playbook de Belong Universe. */
export const PLAYBOOK_SECTIONS = [
  "goals",
  "budget",
  "provider_preferences",
  "rfp_rules",
  "negotiation",
  "legal",
  "escalation",
  "disputes",
  "optimization",
  "approval_gates",
] as const;

export type PlaybookSection = (typeof PLAYBOOK_SECTIONS)[number];

/**
 * Constantes de negocio derivadas del playbook. Se exportan aparte para que
 * los workflows y los tests no tengan que parsear texto libre y puedan razonar
 * con números (BATNA, techo de presupuesto, umbral de aprobación, etc.).
 */
export const PLAYBOOK_CONSTANTS = {
  /** Presupuesto máximo para este tipo de compra (USD). */
  budget_max_usd: 50_000,
  /** Mejor alternativa a un acuerdo negociado: equipo freelance propio. */
  batna_usd: 35_000,
  /** Margen máximo de concesión en precio (10%). */
  max_price_concession_pct: 0.1,
  /** Por encima de este monto, una cotización requiere aprobación humana. */
  human_approval_threshold_usd: 30_000,
  /** Si las cotizaciones superan el budget en este %, se escala al CTO. */
  escalation_over_budget_pct: 0.2,
  /** Diferencia de precio por debajo de la cual prima el time-to-market. */
  time_to_market_priority_pct: 0.15,
  /** Penalidad contractual por retraso (semanal). */
  late_penalty_weekly_pct: 0.02,
  /** Cantidad de proveedores a los que se envía el RFP en competencia. */
  rfp_target_providers: 3,
  /** Plazo de respuesta del RFP en días hábiles. */
  rfp_response_days: 5,
} as const;

/**
 * Contenido textual de cada sección del playbook. Es el texto que la tool
 * `get_playbook_section` devuelve al agente para guiar sus decisiones.
 */
export const PLAYBOOK_CONTENT: Record<PlaybookSection, string> = {
  goals: [
    "## Objetivo de compra",
    "Contratar el desarrollo de una aplicación móvil (iOS + Android) en React Native.",
    "- Alcance: app de cara al usuario final, con backend de soporte.",
    "- Timeline objetivo: entrega en 3 meses desde la firma del contrato.",
    "- Criterio de éxito: app publicada en tiendas, estable y mantenible.",
    "- Prioridad estratégica: time-to-market; salir al mercado rápido importa.",
  ].join("\n"),

  budget: [
    "## Presupuesto y pago",
    `- Presupuesto máximo: USD ${PLAYBOOK_CONSTANTS.budget_max_usd.toLocaleString("en-US")}.`,
    "- Estructura de pago: 30% de anticipo / 70% contra entrega.",
    "- Se aceptan hasta 3 cuotas para el 70% de entrega.",
    "- Los términos de pago NO son negociables (ver sección negotiation).",
    "- Toda cifra de presupuesto es interna; no se revela el techo al proveedor.",
  ].join("\n"),

  provider_preferences: [
    "## Preferencias de proveedor",
    "- Experiencia mínima: +3 años trabajando con React Native.",
    "- Referencias: mínimo 2 referencias verificables de proyectos similares.",
    "- Ubicación preferida: Colombia o LATAM (cercanía horaria y cultural).",
    "- Se valoran certificaciones y un equipo estable (baja rotación).",
    "- Proveedores bloqueados: ninguno por ahora.",
  ].join("\n"),

  rfp_rules: [
    "## Reglas de selección y RFP",
    "- Modo de sourcing: competitivo. Enviar el RFP a 3 proveedores.",
    "- El RFP debe incluir SIEMPRE: timeline, stack técnico, equipo asignado,",
    "  referencias verificables y propuesta económica.",
    `- Plazo de respuesta: ${PLAYBOOK_CONSTANTS.rfp_response_days} días hábiles.`,
    "- Las propuestas se comparan por: precio, timeline, experiencia y propuesta técnica.",
  ].join("\n"),

  negotiation: [
    "## Negociación",
    `- BATNA: contratar un equipo freelance propio por USD ${PLAYBOOK_CONSTANTS.batna_usd.toLocaleString("en-US")}.`,
    "  Nunca aceptar un acuerdo peor que el BATNA.",
    `- Concesión máxima en precio: ${(PLAYBOOK_CONSTANTS.max_price_concession_pct * 100).toFixed(0)}%,`,
    "  y solo si el proveedor acorta el timeline a cambio.",
    "- Los términos de pago (30/70) NO se negocian.",
    "- Palancas disponibles: alcance y timeline (no el pago).",
    `- Walk-away: si no hay zona de acuerdo por encima del BATNA (USD ${PLAYBOOK_CONSTANTS.batna_usd.toLocaleString("en-US")}), escalar.`,
    "- Disclosure: dar respuestas claras al proveedor sin revelar techo ni BATNA.",
  ].join("\n"),

  legal: [
    "## Legal y contratos",
    "- Requiere NDA firmado ANTES de compartir especificaciones detalladas.",
    "- Ley aplicable: legislación colombiana.",
    `- Cláusula de penalidad por retraso obligatoria: ${(PLAYBOOK_CONSTANTS.late_penalty_weekly_pct * 100).toFixed(0)}% semanal.`,
    "- El contrato debe incluir: cronograma de pagos, entregables y penalidades.",
    "- No se firma ningún contrato que carezca de cláusula de penalidad.",
  ].join("\n"),

  escalation: [
    "## Escalaciones",
    `- Si las cotizaciones superan el presupuesto en más del ${(PLAYBOOK_CONSTANTS.escalation_over_budget_pct * 100).toFixed(0)}%, escalar al CTO.`,
    "- Si no hay zona de acuerdo en negociación (todo por debajo del BATNA), escalar.",
    "- Cualquier término legal no estándar se escala al área legal.",
    "- Las escalaciones se registran con una Explicación de Decisión.",
  ].join("\n"),

  disputes: [
    "## Disputas y reputación",
    "- Usar el mecanismo de disputa de Belong Universe ante incumplimientos.",
    "- Árbitro técnico externo para resoluciones de fondo técnico.",
    "- Documentar siempre la evidencia (entregables, comunicaciones, hitos).",
    "- Calificar al proveedor tras cada contrato para alimentar reputación futura.",
  ].join("\n"),

  optimization: [
    "## Objetivo de optimización",
    `- Priorizar time-to-market sobre precio cuando la diferencia es < ${(PLAYBOOK_CONSTANTS.time_to_market_priority_pct * 100).toFixed(0)}%.`,
    "- Entre dos propuestas similares, gana la de menor timeline.",
    "- Equilibrio: calidad técnica primero, luego velocidad, luego precio.",
  ].join("\n"),

  approval_gates: [
    "## Compuertas de aprobación",
    `- Toda cotización por encima de USD ${PLAYBOOK_CONSTANTS.human_approval_threshold_usd.toLocaleString("en-US")} requiere aprobación humana antes de firmar.`,
    "- El agente puede firmar de forma autónoma por debajo de ese umbral",
    "  siempre que el contrato cumpla las reglas legales.",
    "- Ninguna excepción: el umbral de aprobación no se sube de forma autónoma.",
  ].join("\n"),
};

/**
 * Devuelve el contenido de una sección del playbook.
 * Lanza un error si la sección no existe (contrato del demo).
 */
export function getPlaybookSection(section: string): string {
  if (!isValidSection(section)) {
    throw new Error(
      `Sección de playbook inválida: "${section}". ` +
        `Válidas: ${PLAYBOOK_SECTIONS.join(", ")}.`,
    );
  }
  return PLAYBOOK_CONTENT[section];
}

/** Type guard: ¿es `section` una de las 10 secciones válidas? */
export function isValidSection(section: string): section is PlaybookSection {
  return (PLAYBOOK_SECTIONS as readonly string[]).includes(section);
}
