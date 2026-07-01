# GTM — Dónde vive cada cosa, estructura de archivos y ejemplos

> Responde: ¿qué es "conocimiento del núcleo" y "capacidad del agente"? ¿es el system
> prompt? ¿cómo luce un Service Profile y una sección del Core? ¿cómo se conectan?

---

## 1. Dónde vive cada cosa (lo más importante)

En esta arquitectura de skill-pack, un "agente" = un host (Claude/Codex) + **skills**
instaladas + **playbook** (markdown) que el agente lee como contexto. El **system prompt
es delgado**: casi no contiene lógica; solo enruta y dice "carga estas skills y este
playbook". La sustancia vive en archivos.

| Concepto que te confunde | Qué es en realidad | Dónde vive (archivo) |
|---|---|---|
| **Capacidad del agente** | Lo que sabe **HACER** (verbos): prospectar, correr discovery, enviar propuesta, cobrar, escalar | **Skills** → `SKILL.md` (uno por capacidad) |
| **Conocimiento del núcleo** | Lo que **SABE / sus reglas**, compartido entre todos los servicios: posicionamiento, cómo califica, reglas comerciales, autoridad | **GTM Core Playbook** → archivos `.md` |
| **Parámetros por servicio** | Lo específico de cada servicio: value prop, precio, ICP, alcance | **Service Profile** → archivos `.md` |
| **Acciones del marketplace** | Publicar, proponer, firmar, cobrar, disputar | **Runtime / tools** (no markdown) |
| **System prompt** | Mínimo: enruta por rol/fase y manda a cargar skills + playbook | No es donde vive la lógica |

Regla mental: **capacidad = skill (verbo)**, **conocimiento = playbook (sustantivo /
regla)**, **service profile = los valores que rellenan ese conocimiento para un servicio**.
Nada de esto es "el system prompt"; son archivos que el agente lee.

---

## 2. Estructura de carpetas propuesta

```text
.belong/gtm-playbooks/simetrik/
├── core/                          # GTM Core Playbook (conocimiento compartido)
│   ├── index.md
│   ├── 01-positioning-and-value.md
│   ├── 02-qualification.md
│   ├── 03-monetization-rules.md
│   ├── 04-legal-and-contracts.md
│   ├── 05-security-and-diligence.md
│   ├── 06-meetings.md
│   ├── 07-escalations-and-authority.md
│   ├── 08-disputes-and-reputation.md
│   ├── 09-capacity-and-objective.md
│   └── interfaces/                # contratos de handoff hacia lo externo
│       ├── implementation-agent.md
│       └── support-n3.md
└── services/                      # Service Profiles (parámetros por servicio)
    ├── reconciliacion-saas/
    │   └── profile.md
    └── managed-reconciliation/
        └── profile.md
```

Las **capacidades (skills)** viven aparte, en el directorio de skills del host (como hoy:
`skills/.../SKILL.md`). El playbook de arriba es solo el **conocimiento**.

---

## 3. Cómo luce un Service Profile (ejemplo)

Un perfil es **delgado**: solo lo que cambia entre servicios. Un archivo `profile.md`:

```markdown
# Service Profile — Reconciliación SaaS
Status: Done   ·   Aplica core: all

## Identidad
- service-slug: reconciliacion-saas
- category: financial-operations / reconciliation
- pricing-model: recurring        # uno de los modelos permitidos por el core §03
- price: USD 4,000 / mes

## Value Proposition
- Qué es: plataforma SaaS de conciliación automática de transacciones.
- ICP: fintechs y bancos con > 1M transacciones/mes.
- Dolor / outcome: cierres contables lentos y descuadres → conciliación en horas.
- Proof points: <casos, métricas>.

## Discovery (específico del servicio)
- Preguntas de calificación propias de este servicio.
- Casos a evitar (mal fit).

## Alcance y límites
- Qué incluye / qué no incluye este servicio.
- Frontera con implementación (qué entrega el Implementation Agent).

## Overrides del core (si aplica)
- Excepciones puntuales a una regla del core para este servicio. Si no hay: "ninguno".
```

Lo que **no** va en el profile: cómo se califica en general, reglas legales, autoridad,
escalación... eso es del **core** y es igual para todos.

---

## 4. Cómo luce un ítem del GTM Core Playbook (ejemplo)

Misma forma que ya usa el repo, pero a **nivel compañía** y con **slots** que el profile
rellena. Ejemplo `02-qualification.md`:

```markdown
# Qualification (Core)
[index](index.md) | Prev: 01-positioning | Next: 03-monetization
Status: Done

## Playbook Rules (aplican a TODOS los servicios)
- Calificar siempre por: presupuesto, autoridad, necesidad, tiempo.
- Si no hay fit con NINGÚN servicio del catálogo → declinar y registrar motivo.
- Las preguntas de discovery específicas salen del Service Profile activo → `discovery`.

## Slots que rellena el Service Profile
- {ICP}            ← services/<slug>/profile.md
- {discovery-questions}
- {casos-a-evitar}

## Disclosure boundary
- Compartible: criterios generales de fit. Interno: umbrales exactos.
```

Fíjate en la línea clave: el core dice "las preguntas salen del **Service Profile
activo**". Ahí está la conexión.

---

## 5. Cómo se conecta el Core con los Service Profiles

Piénsalo como **plantilla + valores**:

- El **Core** es la plantilla con la maquinaria y los **slots** (`{ICP}`, `{price}`,
  `{value-prop}`, `{discovery-questions}`).
- El **Service Profile** son los **valores** que rellenan esos slots para un servicio.

En ejecución, el GTM Agent **carga el Core completo + UN Service Profile** (el del servicio
en juego). Resultado: el mismo agente, con las mismas reglas, vendiendo cualquier servicio
con solo cambiar el perfil cargado. Un servicio nuevo = un `profile.md` nuevo, **cero
cambios al core**.

---

## 6. Las secciones del GTM Core Playbook

Sí: es **el mismo playbook de este repo, redefinido** — subido de per-servicio a
per-compañía, y con la sección 4 (implementación) convertida en interfaz. Las secciones:

| Core | Viene de la sección actual | Cambio |
|---|---|---|
| 01 Positioning & Value | 01 Value Proposition | A nivel compañía; el value prop concreto baja al profile |
| 02 Qualification | 01 (discovery) | Filosofía de calificación compartida |
| 03 Monetization rules | 02 Monetization | Modelos permitidos y guardrails; precio baja al profile |
| 04 Legal & Contracts | 03 Legal | Igual, nivel compañía |
| 05 Security & Diligence | (nuevo) | Gate de security/cumplimiento |
| 06 Meetings | 05 Human-to-Human Meetings | Igual |
| 07 Escalations & Authority | 06 Escalations | Incluye acciones siempre-humanas |
| 08 Disputes & Reputation | 07 Disputes & Reputation | Igual |
| 09 Capacity & Objective | 08 Capacity & Objective | Igual |
| interfaces/ | 04 Way of Work | **Encogida** a handoff hacia el Implementation Agent |

---

## 7. El diagrama que estás dibujando: cómo se llama

Lo que dibujaste es un **diagrama de árbol** (tree diagram), también llamado **diagrama
de jerarquía** o **árbol de descomposición** (en gestión, una *breakdown structure*; si
fuera radial, un *mind map*). Un nodo raíz que se descompone en componentes y
subcomponentes. Tu estilo (a mano, fondo oscuro) es de **Excalidraw**.

Para que sea **simple**: un árbol no debe llevar flechas cruzadas ni entidades de runtime
(eso fue lo que sobre-compliqué antes). Solo **raíz → ramas → hojas**. Versión completada:

```text
GTM Agent
├── Capacidades (Skills)            ← lo que sabe HACER
│   ├── Prospectar / Discovery
│   ├── Proponer / Contratar
│   ├── Cobrar
│   └── CS / Soporte
├── GTM Core Playbook               ← lo que SABE (compartido)
│   ├── 01 Positioning & Value
│   ├── 02 Qualification
│   ├── 03 Monetization rules
│   ├── 04 Legal & Contracts
│   ├── 05 Security & Diligence
│   ├── 06 Meetings
│   ├── 07 Escalations & Authority
│   ├── 08 Disputes & Reputation
│   └── 09 Capacity & Objective
├── Service Profiles (N)            ← parámetros por servicio
│   └── Service Profile
│       ├── Value Prop
│       ├── ICP
│       ├── Pricing
│       └── Scope
└── Interfaces / Handoffs           ← lo que USA por fuera
    ├── Implementation Agent
    └── Support N3 → Ingeniería
```

El archivo Mermaid de este árbol está en
`documents/diagrams/gtm-arbol-simple.mermaid` (se puede recrear igual en Excalidraw).
