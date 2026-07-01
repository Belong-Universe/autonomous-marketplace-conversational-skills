/**
 * Skill: flujo de contratos (contract-flow).
 *
 * Carga reglas legales y compuertas de aprobación, obtiene el borrador de
 * contrato, lo valida (NDA, penalidad, ley colombiana), y firma de forma
 * autónoma solo si el monto está por debajo del umbral de aprobación humana.
 */

import { createWorkflow, createStep } from "@mastra/core/workflows";
import { z } from "zod";
import * as mcp from "../data/mcp-responses-mock";
import { loadSection } from "../tools/playbook";
import { PLAYBOOK_CONSTANTS } from "../data/playbook-mock";

const APPROVAL_THRESHOLD = PLAYBOOK_CONSTANTS.human_approval_threshold_usd;

const contractState = z.object({
  buyer_id: z.string(),
  quote_id: z.string(),
  legal_rules: z.string().optional(),
  approval_gates: z.string().optional(),
  contract: z.any().optional(),
  validation: z
    .object({
      valid: z.boolean(),
      has_nda: z.boolean(),
      has_penalty_clause: z.boolean(),
      colombian_law: z.boolean(),
      issues: z.array(z.string()),
    })
    .optional(),
  requires_human_approval: z.boolean().optional(),
  result: z
    .object({
      status: z.enum(["contract_signed", "requires_approval", "rejected"]),
      contract_id: z.string(),
      amount: z.number(),
      reason: z.string(),
      signed: z.any().optional(),
    })
    .optional(),
});

type ContractState = z.infer<typeof contractState>;

// 1. Cargar reglas legales.
const loadLegalRules = createStep({
  id: "load_legal_rules",
  inputSchema: contractState,
  outputSchema: contractState,
  execute: async ({ inputData }) => ({
    ...inputData,
    legal_rules: loadSection("legal", inputData.buyer_id),
  }),
});

// 2. Cargar compuertas de aprobación.
const loadApprovalGates = createStep({
  id: "load_approval_gates",
  inputSchema: contractState,
  outputSchema: contractState,
  execute: async ({ inputData }) => ({
    ...inputData,
    approval_gates: loadSection("approval_gates", inputData.buyer_id),
  }),
});

// 3. Obtener el borrador de contrato.
const getContractStep = createStep({
  id: "get_contract",
  inputSchema: contractState,
  outputSchema: contractState,
  execute: async ({ inputData }) => ({
    ...inputData,
    contract: mcp.getContract(inputData.quote_id),
  }),
});

// 4. Validar que el contrato cumple las reglas legales del playbook.
const validateContract = createStep({
  id: "validate_contract",
  inputSchema: contractState,
  outputSchema: contractState,
  execute: async ({ inputData }) => {
    const c = inputData.contract;
    const clausesText = (c.clauses as string[]).join(" ").toLowerCase();

    const has_nda = c.nda_required === true || clausesText.includes("nda");
    const has_penalty_clause =
      Array.isArray(c.penalties) && c.penalties.length > 0;
    const colombian_law = /colomb/i.test(c.governing_law);

    const issues: string[] = [];
    if (!has_nda) issues.push("Falta cláusula/requisito de NDA.");
    if (!has_penalty_clause) issues.push("Falta cláusula de penalidad por retraso.");
    if (!colombian_law) issues.push("La ley aplicable no es la colombiana.");

    return {
      ...inputData,
      validation: {
        valid: issues.length === 0,
        has_nda,
        has_penalty_clause,
        colombian_law,
        issues,
      },
    };
  },
});

// 5. Determinar si se requiere aprobación humana (monto > umbral).
const checkApprovalNeeded = createStep({
  id: "check_approval_needed",
  inputSchema: contractState,
  outputSchema: contractState,
  execute: async ({ inputData }) => ({
    ...inputData,
    requires_human_approval: inputData.contract.amount > APPROVAL_THRESHOLD,
  }),
});

// 6. Firmar autónomamente o marcar para revisión humana, y 7. resolver.
const signOrFlag = createStep({
  id: "sign_or_flag",
  inputSchema: contractState,
  outputSchema: contractState,
  execute: async ({ inputData }) => {
    const c = inputData.contract;

    // Nunca firmar un contrato que no cumple las reglas legales.
    if (!inputData.validation?.valid) {
      return {
        ...inputData,
        result: {
          status: "rejected" as const,
          contract_id: c.contract_id,
          amount: c.amount,
          reason: `El contrato no cumple las reglas legales: ${inputData.validation?.issues.join(" ")}`,
        },
      };
    }

    // Por encima del umbral: marcar para aprobación humana, no firmar.
    if (inputData.requires_human_approval) {
      return {
        ...inputData,
        result: {
          status: "requires_approval" as const,
          contract_id: c.contract_id,
          amount: c.amount,
          reason: `El monto (USD ${c.amount.toLocaleString("en-US")}) supera el umbral de aprobación humana (USD ${APPROVAL_THRESHOLD.toLocaleString("en-US")}).`,
        },
      };
    }

    // Por debajo del umbral y válido: firmar de forma autónoma.
    const signed = mcp.signContract(c.contract_id, inputData.buyer_id);
    return {
      ...inputData,
      result: {
        status: "contract_signed" as const,
        contract_id: c.contract_id,
        amount: c.amount,
        reason: `Contrato firmado autónomamente: monto bajo el umbral y cláusulas válidas.`,
        signed,
      },
    };
  },
});

export const contractFlow = createWorkflow({
  id: "contract-flow",
  description:
    "Skill de contratos: obtiene el borrador, valida NDA/penalidad/ley " +
    "colombiana y firma autónomamente o marca para aprobación humana (>$30k).",
  inputSchema: contractState,
  outputSchema: contractState,
})
  .then(loadLegalRules)
  .then(loadApprovalGates)
  .then(getContractStep)
  .then(validateContract)
  .then(checkApprovalNeeded)
  .then(signOrFlag);

contractFlow.commit();

export type { ContractState };
