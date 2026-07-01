/**
 * Utilidades compartidas por los tests. Ejecutar un workflow de Mastra y
 * devolver su resultado final, fallando con un mensaje claro si no tiene éxito.
 */

export async function runWorkflow<T = any>(
  workflow: any,
  inputData: Record<string, unknown>,
): Promise<T> {
  const run = await workflow.createRun();
  const result = await run.start({ inputData });
  if (result.status !== "success") {
    throw new Error(
      `Workflow "${workflow.id}" no terminó en éxito: ${JSON.stringify(result)}`,
    );
  }
  return result.result as T;
}
