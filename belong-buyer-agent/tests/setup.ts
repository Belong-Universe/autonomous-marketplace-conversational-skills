/**
 * Setup global de Vitest: carga las variables de entorno desde .env.
 * Necesario para los tests e2e, que usan el LLM real (ANTHROPIC_API_KEY).
 */
import "dotenv/config";
