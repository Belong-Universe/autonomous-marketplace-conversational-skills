# GTM — Cómo se instancian y conectan las secciones, los profiles y el plugin

> Responde: ¿el GTM Agent qué es respecto al Belong Marketplace? ¿cómo se instancia cada
> sección del playbook y cómo se "llaman" entre sí (la wiki de carpetas)? ¿cómo se conecta
> cada sección del Core con el Service Profile?

---

## 1. El modelo refinado (con tu aclaración)

- **GTM Agent = puente / orquestador.** No contiene las capacidades; las **invoca**. Es
  el intermediario entre el **usuario** y el **Belong Marketplace**.
- **Belong Marketplace Plugin = el paquete que guarda, instancia y corre** tres cosas:
  - **Skills** → capacidades (verbos): prospectar, discovery, proponer, cobrar, escalar.
  - **Tools** → las **acciones del marketplace** (publicar Service, enviar Proposal,
    firmar, cobrar, abrir disputa).
  - **Connectors** → integraciones externas (CRM, Zendesk, Calendly…).
- **Playbook = conocimiento** que el GTM Agent **lee** para saber cómo comportarse:
  **Core** (compartido) + **Service Profiles** (parámetros por servicio).

Dicho simple: el Playbook le dice al GTM Agent **cómo** actuar; el Plugin le da **con qué**
actuar. El GTM Agent junta ambos frente al usuario.

---

## 2. Instanciación: plantilla (wiki) vs instancia (carpeta generada)

Hay dos capas, y esto resuelve el "¿cómo se instancia cada sección?":

| Capa | Qué es | Dónde vive | Estado |
|---|---|---|---|
| **Plantilla / wiki** | La estructura canónica: qué necesita cada sección, sus slots, su quality bar | Dentro del **plugin** (`references/...`), **read-only** | Fija |
| **Instancia / generada** | El playbook lleno para Simetrik: Core (1) + Profiles (N) | En la cuenta (`.belong/gtm-playbooks/simetrik/`) | Missing→Partial→Done |

El flujo: una skill de setup/train **instancia** el playbook → copia la estructura de la
wiki, crea los archivos de sección con `Status: Missing` + `TBD`, y los va llenando con
gates de aprobación. **La wiki define; la instancia se llena.** Una instancia de Core por
compañía; N instancias de Profile (una por servicio).

---

## 3. Cómo se "llaman" las secciones entre sí (la wiki de carpetas)

Las secciones **no se ejecutan** unas a otras: se **enlazan** estilo wiki. Tres mecanismos
(los mismos que ya usa el repo, así que es probado):

1. **Índice + navegación lineal:** `index.md` con tabla de secciones, y en cada archivo
   `Back to index | Prev | Next`. Así el agente carga solo la página que necesita.
2. **Bloque "Relacionadas":** enlaces cruzados cuando una sección depende de otra. Ej.:
   `03 Monetization` enlaza a `07 Authority` (excepciones de pago), `08 Disputes` enlaza a
   `04 Legal` (evidencia/aceptación).
3. **Carga selectiva:** el agente abre `index.md`, decide qué sección le aplica al momento
   (ej.: en negociación → `03 Monetization`), y carga esa + sus relacionadas. No carga
   todo el playbook siempre.

**Mi opinión / recomendación:** conservar este patrón wiki (es el que ya funciona) y
**agregar un encabezado de binding** en cada sección (`Reads from profile:`) para que la
conexión con el service profile sea explícita y verificable. Eso es lo de la sección 4.

Mini-mapa de dependencias entre secciones (quién enlaza a quién):

```text
01 Positioning ──┐
02 Qualification ─┤→ (base para todo)
03 Monetization ──→ 07 Authority (excepciones de pago)
04 Legal ─────────→ 07 Authority (quién firma)
05 Security ──────→ 04 Legal (gating de cierre)
06 Meetings ──────→ 07 Authority (autoridad para agendar)
08 Disputes ──────→ 04 Legal (evidencia/aceptación)
09 Capacity ──────→ 03 Monetization (precio según demanda)
```

---

## 4. Conexión sección Core ↔ Service Profile (binding por slots)

Aquí está lo que pediste: cómo cada sección se conecta con el profile. **No todas las
secciones se conectan** — solo las que tienen algo específico del servicio. El mecanismo es
**binding por slot con nombre**: la sección declara qué campo del profile consume; el
profile provee ese campo.

| Core (sección) | ¿Lee del profile? | Campo(s) del Service Profile |
|---|---|---|
| 01 Positioning & Value | Sí | `value-prop`, `proof-points` |
| 02 Qualification | Sí | `ICP`, `discovery-questions`, `casos-a-evitar` |
| 03 Monetization rules | Sí | `pricing-model`, `price` (dentro de modelos permitidos por el core) |
| 04 Legal & Contracts | Sí | `scope`, `deliverables` |
| 05 Security & Diligence | Opcional | `compliance-reqs` (si el servicio tiene requisitos propios) |
| 06 Meetings | No | — (puro core) |
| 07 Escalations & Authority | No* | — (*salvo `authority-overrides` por servicio) |
| 08 Disputes & Reputation | No | — (puro core) |
| 09 Capacity & Objective | Sí | `availability`, `lead-time` por servicio |

Cómo se ve en los archivos:

```markdown
# 02 Qualification (Core)
Reads from profile: {ICP}, {discovery-questions}, {casos-a-evitar}

## Playbook Rules
- Calificar por presupuesto, autoridad, necesidad, tiempo.
- Las preguntas concretas vienen del profile activo (slots de arriba).
```

```markdown
# Service Profile — Reconciliación SaaS
Feeds core sections: 01, 02, 03, 04, 09

ICP: fintechs y bancos con >1M transacciones/mes
discovery-questions: [...]
pricing-model: recurring
price: USD 4,000 / mes
scope: [...]
```

El binding es **bidireccional y declarado**: la sección dice qué lee, el profile dice a qué
secciones alimenta. Si falta un slot, es detectable (validación). Para casos raros, el
profile puede traer un `overrides` que pisa una regla del core solo para ese servicio.

En ejecución: el GTM Agent **carga Core (todas las secciones que aplican) + UN Profile**, y
resuelve los slots. Servicio nuevo = un `profile.md` nuevo; **cero cambios al core**.

---

## 5. Cómo todo se concatena (arquitectura)

```text
            ┌─────────── Belong Marketplace Plugin ───────────┐
            │   Skills        Tools         Connectors          │
            └───────────────────▲────────────────────────────--┘
                                 │ usa (invoca)
   Usuario  ⇄  GTM Agent  ───────┤
                                 │ lee (conocimiento)
                  ┌──────────────┴───────────────┐
                  │                              │
            GTM Core Playbook            Service Profiles (N)
            (9 secciones, compartido)    cada uno: value-prop, ICP,
                  │  ▲                    pricing, scope, ...
                  │  │ binding por slots         │
                  └──┴────────────────────────---┘
```

Diagramas fuente:
- `documents/diagrams/gtm-arquitectura.mermaid` — vista general (la que concatenaste).
- `documents/diagrams/gtm-binding-secciones-profile.mermaid` — qué sección se conecta con
  qué campo del profile.
