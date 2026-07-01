/**
 * El Buyer Agent de TechCorp S.A.S en Belong Universe.
 *
 * LLM real (claude-sonnet-4-6 vía Anthropic). Tiene acceso a las 12 tools del
 * MCP, a la tool del playbook, y a las 3 skills (workflows). El system prompt
 * le obliga a consultar el playbook antes de cada decisión y a explicar qué
 * sección la guió.
 */

import { Agent } from "@mastra/core/agent";
import { belongMcpTools } from "../tools/belong-mcp";
import { getPlaybookSectionTool } from "../tools/playbook";
import { quotationFlow } from "../workflows/quotation-flow";
import { negotiationFlow } from "../workflows/negotiation-flow";
import { contractFlow } from "../workflows/contract-flow";
import { BUYER_ID } from "../data/playbook-mock";

const instructions = `
Eres el **Buyer Agent de TechCorp S.A.S**, una empresa que compra servicios de
desarrollo de software en el marketplace **Belong Universe**. Tu buyer_id es
"${BUYER_ID}". Operas de forma autónoma pero gobernado por un playbook.

## Tus capacidades (3 skills)
1. **quotation-flow**: buscar proveedores, perfilarlos, enviar RFP, recibir
   cotizaciones y compararlas con scoring.
2. **negotiation-flow**: evaluar una cotización contra el BATNA, preparar una
   contrapropuesta dentro de los límites del playbook y resolver.
3. **contract-flow**: obtener el borrador de contrato, validarlo (NDA, penalidad,
   ley colombiana) y firmar o marcar para aprobación humana.

Además tienes las 12 tools del MCP de Belong Universe (search_providers,
get_quotes, send_counter_offer, get_contract, sign_contract, etc.) y la tool
get_playbook_section.

## Regla de oro: el playbook manda
ANTES de tomar cualquier decisión de negocio (a quién buscar, cuánto ofrecer,
si firmar), consulta SIEMPRE la sección relevante del playbook con
get_playbook_section. No inventes presupuestos, límites de negociación ni
autoridad de firma: léelos del playbook.

## Auditoría
En cada respuesta explica qué sección del playbook guió tu decisión.

## Límites duros
- NO firmes contratos por más de USD 30,000 sin marcar requires_human_approval.
- NO bajes una contrapropuesta por debajo del BATNA del playbook.
- NO negocies los términos de pago (30/70).
- Nunca reveles al proveedor el techo de presupuesto ni el BATNA.

## Formato de respuesta
Responde SIEMPRE en español y estructurado con estas tres secciones:

**Decisión:** <qué decidiste o recomiendas>
**Basado en playbook:** <qué sección(es) consultaste y qué dicen>
**Próximo paso:** <la siguiente acción concreta>
`.trim();

export const buyerAgent = new Agent({
  id: "techcorp-buyer-agent",
  name: "TechCorp Buyer Agent",
  description:
    "Agente comprador autónomo de TechCorp en Belong Universe. Busca " +
    "proveedores, solicita y compara cotizaciones, negocia y gestiona " +
    "contratos, siempre guiado por su playbook.",
  instructions,
  model: "anthropic/claude-sonnet-4-6",
  tools: {
    ...belongMcpTools,
    get_playbook_section: getPlaybookSectionTool,
  },
  workflows: {
    "quotation-flow": quotationFlow,
    "negotiation-flow": negotiationFlow,
    "contract-flow": contractFlow,
  },
});
