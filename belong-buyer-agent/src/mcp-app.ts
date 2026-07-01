/**
 * Configuración compartida del servidor MCP del belong-buyer-agent.
 *
 * Lo usan los dos entrypoints: stdio (mcp-server.ts, para Claude Desktop local)
 * y HTTP (mcp-server-http.ts, para el conector custom de la app de Claude).
 *
 * Expone: las 12 tools del MCP de Belong Universe + get_playbook_section, el
 * agente completo (ask_buyerAgent, usa el LLM real) y las 3 skills como tools
 * (run_quotation-flow, run_negotiation-flow, run_contract-flow).
 */

import { MCPServer } from "@mastra/mcp";
import { belongMcpTools } from "./mastra/tools/belong-mcp";
import { getPlaybookSectionTool } from "./mastra/tools/playbook";
import { buyerAgent } from "./mastra/agents/buyer-agent";
import { quotationFlow } from "./mastra/workflows/quotation-flow";
import { negotiationFlow } from "./mastra/workflows/negotiation-flow";
import { contractFlow } from "./mastra/workflows/contract-flow";

export function buildMcpServer(): MCPServer {
  return new MCPServer({
    name: "belong-buyer-agent",
    version: "1.0.0",
    description:
      "Buyer agent de TechCorp en Belong Universe: tools del marketplace, " +
      "playbook, skills (cotización/negociación/contratos) y el agente completo.",
    tools: {
      ...belongMcpTools,
      get_playbook_section: getPlaybookSectionTool,
    },
    agents: { buyerAgent },
    workflows: {
      "quotation-flow": quotationFlow,
      "negotiation-flow": negotiationFlow,
      "contract-flow": contractFlow,
    },
  });
}
