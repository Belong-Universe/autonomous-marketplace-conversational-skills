import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    // Carga ANTHROPIC_API_KEY desde .env para los tests e2e (LLM real).
    setupFiles: ["./tests/setup.ts"],
    // El LLM real es lento: timeout amplio. Unit/integration son rápidos.
    testTimeout: 60_000,
    hookTimeout: 60_000,
  },
});
