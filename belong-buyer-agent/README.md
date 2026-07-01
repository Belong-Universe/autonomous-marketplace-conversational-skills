# belong-buyer-agent

Demostración completa de la arquitectura de un **buyer agent autónomo** para el
marketplace **Belong Universe**, construida con [Mastra](https://mastra.ai),
TypeScript y Anthropic `claude-sonnet-4-6`.

El agente puede **buscar proveedores, solicitar cotizaciones, negociar y obtener
contratos**, todo guiado por su **playbook** personal y usando el **MCP de Belong
Universe**. Todo el MCP está **mockeado** con respuestas deterministas y
verosímiles; el **LLM es real**.

## Qué demuestra

Las cuatro capas de un agente de marketplace y cómo se conectan:

1. **MCP (tools)** — las 12 capacidades del buyer en Belong Universe.
2. **Skills (workflows)** — flujos reutilizables que orquestan varias tools.
3. **Playbook** — las reglas de negocio que gobiernan cada decisión.
4. **Agent** — el LLM que razona, consulta el playbook y usa tools + skills.

## Arquitectura

```
                ┌──────────────────────────────────────────────┐
                │            TechCorp Buyer Agent (LLM)          │
                │            claude-sonnet-4-6 (real)            │
                │                                                │
                │  "Antes de decidir, consulta el playbook"      │
                └───────┬───────────────┬───────────────┬───────┘
                        │               │               │
            consulta    │       usa     │      ejecuta  │
                        ▼               ▼               ▼
            ┌───────────────┐   ┌──────────────┐  ┌──────────────────┐
            │   PLAYBOOK    │   │  MCP TOOLS   │  │  SKILLS (3)      │
            │  (10 secciones)│  │  (12 tools)  │  │  = workflows     │
            │               │   │              │  │                  │
            │ goals         │   │ search_      │  │ quotation-flow   │
            │ budget        │   │  providers   │  │ negotiation-flow │
            │ provider_pref │   │ get_quotes   │  │ contract-flow    │
            │ rfp_rules     │   │ send_rfp     │  │                  │
            │ negotiation   │   │ compare_     │  │ (cada skill      │
            │ legal         │   │  quotes      │  │  encadena tools  │
            │ escalation    │   │ send_counter │  │  + playbook)     │
            │ disputes      │   │ get_contract │  │                  │
            │ optimization  │   │ sign_        │  └────────┬─────────┘
            │ approval_gates│   │  contract... │           │
            └───────┬───────┘   └──────┬───────┘           │
                    │                  │                   │
                    └──────────────────┴───────────────────┘
                                       │
                                       ▼
                        ┌────────────────────────────┐
                        │  Capa de servicio mock      │
                        │  (data/, 100% determinista, │
                        │   cero HTTP)                │
                        └────────────────────────────┘
```

Las skills (workflows) y las tools comparten **la misma capa de servicio
mockeada** y **el mismo log de auditoría del playbook**, de modo que el
comportamiento es idéntico tanto si el agente llama una tool suelta como si
ejecuta una skill completa.

## Instalación y configuración

Lo único que necesitas es una `ANTHROPIC_API_KEY`.

```bash
npm install
cp .env.example .env   # pega tu clave de https://console.anthropic.com/
```

`.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
```

## Correr los tests

Los tests **unit** e **integration** son deterministas y **no llaman al LLM**.
El test **e2e** sí usa el modelo real (necesita la API key).

```bash
npm run test              # todo
npm run test:unit         # solo unit (tools, workflows, playbook)
npm run test:integration  # solo integration (workflows de punta a punta)
npm run test:e2e          # solo e2e (LLM real, ~60s)
```

Si no hay `ANTHROPIC_API_KEY`, el bloque e2e se salta automáticamente
(`describe.skip`) y el resto pasa igual.

## Correr el agente interactivo

```bash
npm run dev        # abre el playground de Mastra (mastra dev)
```

Allí puedes chatear con el **TechCorp Buyer Agent**, ver las tools, invocar las
skills (workflows) y observar el rastro de auditoría del playbook.

## Conectar a la app de Claude (MCP)

Puedes exponer TODO el sistema como un servidor MCP y conectarlo a **Claude
Desktop**. Desde Claude verás y podrás invocar:

- las 12 tools del marketplace + `get_playbook_section`,
- las 3 skills como tools: `run_quotation-flow`, `run_negotiation-flow`,
  `run_contract-flow` (deterministas, no usan API key),
- el agente completo: `ask_buyerAgent` (usa el LLM real → necesita la API key).

### 1. Probar el servidor MCP en local

```bash
npm run mcp     # arranca el servidor MCP por stdio
```

Para una verificación rápida sin Claude (lista las tools expuestas):

```bash
printf '%s\n%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke","version":"1.0"}}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | npm run -s mcp
```

### 2. Conectarlo a Claude Desktop

Edita la config de Claude Desktop (macOS):
`~/Library/Application Support/Claude/claude_desktop_config.json`
y añade el bloque de [`claude_desktop_config.example.json`](./claude_desktop_config.example.json)
(ajusta la ruta absoluta y pega tu `ANTHROPIC_API_KEY`):

```json
{
  "mcpServers": {
    "belong-buyer-agent": {
      "command": "npx",
      "args": ["tsx", "/ruta/absoluta/.../belong-buyer-agent/src/mcp-server.ts"],
      "env": { "ANTHROPIC_API_KEY": "sk-ant-..." }
    }
  }
}
```

Reinicia Claude Desktop. Verás "belong-buyer-agent" en el ícono de
herramientas. Ya puedes pedirle, por ejemplo:

> "Usa `ask_buyerAgent`: necesito una app móvil, busca proveedores y recomiéndame uno."

o invocar una skill directamente:

> "Corre `run_contract-flow` con quote_id `quote_test_45k`."

Todo lo que pase (llamadas a tools, resultados de skills, respuesta del agente)
queda visible dentro de la app de Claude.

> Nota: `run_*` y las tools del marketplace son deterministas y NO requieren API
> key. Solo `ask_buyerAgent` la usa, porque dispara el LLM interno del agente.

## Las capas en detalle

### MCP → `src/mastra/tools/belong-mcp.ts`
Las 12 tools del buyer (`search_providers`, `get_quotes`, `send_counter_offer`,
`get_contract`, `sign_contract`, etc.). Cada una valida entrada/salida con Zod y
delega en la capa de servicio determinista (`src/mastra/data/`).

### Skills → `src/mastra/workflows/`
Tres workflows que encadenan tools + playbook en flujos reutilizables:

- **quotation-flow**: reglas RFP → preferencias → buscar → perfilar → enviar RFP
  → recibir cotizaciones → comparar y recomendar.
- **negotiation-flow**: reglas de negociación → presupuesto → analizar vs BATNA →
  preparar contrapropuesta (dentro de límites) → enviar → resolver
  (aceptado / rechazado / escalar).
- **contract-flow**: reglas legales → compuertas de aprobación → obtener contrato
  → validar (NDA, penalidad, ley colombiana) → firmar o marcar para aprobación
  humana (umbral $30k).

### Playbook → `src/mastra/data/playbook-mock.ts` + `tools/playbook.ts`
Diez secciones de reglas durables (presupuesto, BATNA, límites de negociación,
autoridad de firma, escalaciones…). La tool `get_playbook_section` las expone al
agente y **registra cada consulta** para auditoría.

### Agent → `src/mastra/agents/buyer-agent.ts`
El LLM real con un system prompt que le obliga a **consultar el playbook antes de
cada decisión**, respetar los límites duros (no firmar > $30k sin aprobación, no
bajar del BATNA, no negociar términos de pago) y responder con el formato
**Decisión / Basado en playbook / Próximo paso**.

## Estructura del proyecto

```
src/
├── mcp-server.ts             # servidor MCP (stdio) para Claude Desktop
└── mastra/
├── index.ts                  # instancia de Mastra (agente + 3 workflows + logger)
├── agents/buyer-agent.ts     # el agente principal (LLM real)
├── tools/
│   ├── belong-mcp.ts         # MCP mockeado (12 tools)
│   └── playbook.ts           # tool get_playbook_section + auditoría
├── workflows/
│   ├── quotation-flow.ts     # skill: cotización
│   ├── negotiation-flow.ts   # skill: negociación
│   └── contract-flow.ts      # skill: contratos
└── data/
    ├── playbook-mock.ts      # playbook del buyer (10 secciones)
    └── mcp-responses-mock.ts # capa de servicio determinista del MCP
tests/
├── unit/                     # tools, workflows, playbook (sin LLM)
├── integration/              # workflows de punta a punta (sin LLM)
└── e2e/                      # buyer agent con LLM real
```

## Restricciones de diseño

- **Todo el MCP es mock**: cero llamadas HTTP reales.
- **El LLM sí es real**: usa `ANTHROPIC_API_KEY`.
- **unit/integration nunca llaman al LLM**; solo **e2e**.
- Comentarios y textos en **español**; código (variables/funciones) en **inglés**.
- Mocks **deterministas**: mismo input → mismo output.
