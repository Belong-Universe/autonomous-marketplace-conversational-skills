/**
 * Instancia principal de Mastra para el belong-buyer-agent.
 *
 * Registra el buyer agent y los 3 workflows (skills), y configura el logger
 * en modo desarrollo. Es el punto de entrada que usa `mastra dev`.
 */

import { Mastra } from "@mastra/core/mastra";
import { PinoLogger } from "@mastra/loggers";
import { buyerAgent } from "./agents/buyer-agent";
import { quotationFlow } from "./workflows/quotation-flow";
import { negotiationFlow } from "./workflows/negotiation-flow";
import { contractFlow } from "./workflows/contract-flow";

export const mastra = new Mastra({
  agents: { buyerAgent },
  workflows: {
    "quotation-flow": quotationFlow,
    "negotiation-flow": negotiationFlow,
    "contract-flow": contractFlow,
  },
  logger: new PinoLogger({ name: "belong-buyer-agent", level: "debug" }),
});
