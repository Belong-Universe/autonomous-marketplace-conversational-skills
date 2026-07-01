# Arquitectura del GTM Playbook (Simetrik) — Orientación

> Documento de orientación para decidir cómo estructurar el playbook GTM completo y
> cómo se relaciona con los playbooks que ya existen en este repo (`selling-playbook`,
> `buying-playbook`). No reescribe nada todavía: te da el mapa y el siguiente paso.

---

## 1. Entendamos a profundidad el playbook que YA existe

Antes de decidir si hace falta un meta-playbook o extender el actual, hay que ver con
precisión qué es y qué **no** es el `selling-playbook` de hoy.

### 1.1 Qué es (en una frase)

El `selling-playbook` **no es un brochure de ventas**. Es el **contrato operativo** de
**un Selling Agent** que representa **un Service**. Define, en reglas cortas, cuatro cosas
por sección:

1. Qué puede hacer el agente **de forma autónoma**.
2. Qué **necesita aprobación humana**.
3. Qué **evidencia / objeto / audit trail** prueba que la acción ocurrió.
4. Qué pasa **cuando la realidad no encaja** con el camino normal (escalación).

La unidad es el Service: **1 Service = 1 Selling Agent = 1 Selling Playbook**. Si Simetrik
vende varios servicios separables, cada uno tiene su propio playbook y su propio agente.

### 1.2 Las 8 secciones actuales

| # | Sección | Qué captura | Equipo Simetrik más cercano |
|---|---------|-------------|-----------------------------|
| 1 | Value Proposition | Qué se vende, a quién, dolor/outcome, proof points, discovery, criterios de calificación | Marketing + SDR + AE |
| 2 | Monetization Models | Modelo de precio (fixed/hourly/milestone/recurring/consumption), precio, escrow, excepciones de pago | Finance (pricing) |
| 3 | Legal And Contracts | Términos del SOW, entregables, evidencia, criterios de aceptación, autoridad de firma | Legal |
| 4 | Way Of Work During An Active Service | Workflow de entrega tras firma: kickoff, milestones, fulfillment tasks, evidencia, aceptación | Professional / Managed Services |
| 5 | Human-To-Human Meetings | Cuándo proponer reunión, handshake Calendly agente↔agente, urgencia, contrapropuestas | Services Consultants (demos) + AE |
| 6 | Escalations | Umbrales de excepción, autorizaciones, pausa/resume, acciones "siempre humanas" (sign/deliver/payment/dispute) | Todos (define el límite de autonomía) |
| 7 | Disputes And Reputation Rules | Postura ante disputas, estándar de evidencia, refund/rework, rating, reputación | ProServ (disputas transaccionales) + Support |
| 8 | Capacity And Objective | Cuántos servicios activos en paralelo, lead time, qué optimiza el agente (win rate, margen, utilización) | Operaciones / liderazgo GTM |

Hay un gemelo simétrico del lado de la demanda: `buying-playbook` con 9 secciones
(goals, budget, provider preferences, selección/RFP, legal, escalations, disputes,
optimización, meetings).

### 1.3 Disciplinas transversales (aplican a TODA sección)

- **Source discipline:** el agente solo se prellena con fuentes que el humano designa
  explícitamente; nada de conocimiento ambiente. Lo que no se sabe queda como `TBD`.
- **Disclosure discipline:** cada sección define qué es **compartible con el comprador**
  vs **interno** (márgenes, límites de autoridad, capacidad, política). En duda → interno
  y escala.
- **Review discipline:** se aprueba **sección por sección** con gate explícito; no se
  avanza sin "aprobado".

### 1.4 Forma fija de cada archivo de sección

```markdown
# <Nombre de la sección>
[Back to index](index.md)
Status: Missing | Partial | Done
Approval: Not requested | Pending | Approved

## Playbook Rules        (las reglas que el agente debe seguir)
## Still Missing         (TBD o "-")
## Source Notes          (fuentes usadas)
```

Una sección está **`Done`** cuando el agente puede convertirla en comportamiento repetible
**sin adivinar**; **`Partial`** si da dirección pero deja huecos operativos; **`Missing`**
si el agente tendría que inventar política, autoridad, precio o pasos.

### 1.5 Ciclo de vida y "compilación" a runtime

`Setup → Training → Validation → Production`. Antes de activar se corre un
**Consistency Check** entre secciones (el runtime valida que existan campos, no que sean
coherentes entre sí).

El puente clave: cada sección **mapea a flags del runtime** (`runtime-mapping.md`). El
playbook es legible por humanos; el runtime mapping es lo ejecutable por la máquina. Ej.:
Value Proposition → `--service-name/--category/--discovery-questions`; Monetization →
`--pricing-model/--price`; Escalations → `--escalation-paths/--human-controlled-actions`.

### 1.6 El límite de autonomía (el corazón del modelo)

- **Frontera de autonomía:** `Playbook + Standing Authorization`.
- **Frontera del trabajo humano:** `Marketplace Inbox`.
- **Tres desenlaces de autoridad** por acción: (a) el agente ejecuta, (b) el agente
  escala para aprobación, (c) **siempre lo hace el humano** (Scenario B — solo elegible
  para `sign`, `deliver`, `payment`, `dispute`).

> **Conclusión del análisis:** el playbook actual es excelente como contrato operativo de
> **un agente de un servicio**, pero comprime **toda la organización GTM** (8 equipos) en
> 8 secciones de un solo agente. SDR, AE, demos, CS, Soporte (Zendesk/N3), Finance,
> ProServ/Managed y Security **no tienen lugar propio** — están implícitos o ausentes.
> Ese es exactamente el hueco que tu playbook GTM debe llenar.

---

## 2. Recomendación de arquitectura: meta-playbook + módulos por equipo

No es "o meta-playbook o extender": son **dos capas distintas y complementarias**. La
respuesta correcta a tu duda es **ambas, en este orden**:

```
NIVEL 0 — GTM Meta-Playbook ("playbook de playbooks")
          Orquesta el journey, el mapa de equipos, los handoffs y la autoridad.
          NO duplica reglas: referencia.
                │
NIVEL 1 — Playbooks por Equipo/Función (8 módulos)
          1 SDR/Marketing · 2 AE · 3 Services Consultants · 4 Legal
          5 CS & Support · 6 Finance · 7 ProServ/Managed · 8 Security
          Cada módulo: rol + autoridad + handoffs + escalación + KPIs.
                │
NIVEL 2 — Playbooks canónicos existentes (librería de "contrato operativo")
          selling-playbook (8 secciones) · buying-playbook (9 secciones)
          Aquí viven las reglas finas. Los módulos del Nivel 1 las REFERENCIAN.
```

Por qué así:

- **Extender el selling-playbook** sirve para profundizar reglas dentro de un agente
  (Nivel 2). No sirve para representar handoffs entre equipos ni el journey completo.
- **El meta-playbook** (Nivel 0) es lo que da la visión GTM end-to-end y permite que
  alguien que no es experto "sepa vender el servicio y tener las nociones de los
  diferentes equipos" — tu objetivo declarado.
- Elegiste organizar **por equipo/función** → ese es el Nivel 1.

---

## 3. Los 8 módulos por equipo (mapa del journey)

Orden = flujo del customer journey. Cada módulo declara de quién recibe y a quién entrega.

| # | Módulo (equipo) | Owns en el journey | Recibe de → Entrega a | Referencia canónica |
|---|-----------------|--------------------|-----------------------|---------------------|
| 1 | **Marketing & SDR** | Top of funnel, generación y calificación de demanda | (Inbound/Outbound) → AE | selling §1 (Value Prop, discovery) |
| 2 | **Account Executive** | Venta de valor de negocio, calificación profunda, propuesta | SDR → Services Consultant / Legal | selling §1, §2, §5 |
| 3 | **Services Consultants** | Demos, validación técnica/solución | AE → Legal | selling §5 (meetings), §1 |
| 4 | **Legal** | Contratos, SOW, firma, límites no negociables | AE/Consultant → Security/Finance | selling §3 |
| 5 | **Security** | Due diligence, cierre seguro del contrato | Legal → Finance/ProServ | buying §3/§4 (due diligence), selling §3 |
| 6 | **Finance** | Billing & collection, escrow, excepciones de pago | Legal → (recurrente con CS) | selling §2 |
| 7 | **Professional / Managed Services** | Implementación, "hacerle el trabajo al cliente", que lleguen los archivos, disputas transaccionales, outsourcing | Legal/Finance → CS | selling §4 (way of work), §7 (disputes) |
| 8 | **Customer Success & Support** | Realización de valor, alineación con el cliente; Soporte herramienta (Zendesk); N3 → Ingeniería | ProServ → (loop con Finance/ProServ) | selling §4, §7, §6 |

> Nota sobre Soporte: el módulo CS&Support debe separar **soporte de herramienta**
> (Zendesk, dudas de usuarios) de **soporte N3** que entra al equipo de ingeniería. En
> términos del modelo de autonomía, N3 es típicamente una **escalación humana** (no
> autónoma).

---

## 4. Qué necesita cada módulo de equipo para estar "completo"

Plantilla única para los 8 módulos (reutiliza la forma del Nivel 2 y le agrega lo de
journey). Un módulo está `Done` cuando un agente —o una persona nueva— puede ejecutar el
rol del equipo sin adivinar.

```markdown
# <Equipo> — GTM Module
[Back to GTM index](index.md) | Upstream: <equipo previo> | Downstream: <equipo siguiente>
Status: Missing | Partial | Done   ·   Approval: ...

## 1. Misión y alcance      → qué posee este equipo en el journey
## 2. Trigger de entrada     → qué evento/artefacto activa a este equipo
## 3. Inputs requeridos      → qué necesita recibir para operar
## 4. Outputs / Artefacto     → qué produce y entrega (el objeto que "viaja")
## 5. Handoff de salida      → a quién entrega, con qué criterio de "listo"
## 6. Autoridad y autonomía  → autónomo | requiere aprobación | siempre humano
## 7. Conocimiento / Reglas  → lo que el agente debe saber para vender/operar
## 8. Escalaciones           → umbrales + dueño de cada ruta (ej. N3 → Ingeniería)
## 9. Evidencia / Audit       → qué prueba que el trabajo se hizo
## 10. Disclosure boundary   → compartible con cliente vs interno
## 11. KPIs / Objetivo        → qué optimiza este equipo
## 12. Referencias            → links a selling/buying §X + flags runtime + tools marketplace
## Still Missing             → TBD o "-"
## Source Notes
```

Las secciones **6, 8 y 9** son las que conectan con el modelo de autonomía del repo y por
tanto las más críticas para que esto funcione como **managed agent**, no solo como
documento.

---

## 5. Cómo se referencian los archivos entre sí (lo que pediste)

Tres mecanismos, todos ya presentes en el repo y reutilizables:

1. **Navegación lineal en el header** (como hoy en `01-value-proposition.md`):
   `Upstream | index | Downstream`. Esto materializa la cadena del journey.
2. **Bloque "Referencias"** en cada módulo → enlaza a la(s) sección(es) canónica(s) de
   `selling-playbook` / `buying-playbook` en vez de copiar reglas. **Una sola fuente de
   verdad**; el módulo de equipo aporta el "quién/cuándo/handoff", la sección canónica
   aporta el "regla fina".
3. **Handoff Registry** en el `index.md` del meta-playbook: una tabla
   `Equipo → trigger → artefacto → equipo destino` que hace explícita toda la cadena y
   permite validar que no haya handoffs rotos (un output sin destino, o un trigger sin
   origen).

Regla de oro para evitar duplicación: **el módulo de equipo nunca redefine una regla que
ya vive en una sección canónica; la enlaza.** Si una regla aplica a varios equipos, vive
en el Nivel 2 y se referencia desde cada módulo.

---

## 6. El "playbook de playbooks" (Nivel 0) — qué contiene su index

- **Propósito y alcance** del GTM (qué servicio/s cubre).
- **Mapa del journey** (las 8 etapas/equipos) + diagrama.
- **Handoff Registry** (tabla de la sección 5).
- **Glosario compartido** (términos, acrónimos, codenames — clave para que un no-experto
  lo use).
- **Modelo de autoridad global**: el patrón ejecuta/escala/siempre-humano y dónde está la
  frontera (`Marketplace Inbox`).
- **Índice de módulos** (links a los 8) + **índice de canónicos** (selling/buying).
- **Estado de completitud** (tabla de checkpoints como ya usa el repo).

---

## 7. Del playbook al Managed Agent con tools del marketplace

El meta-playbook "compila" a un agente igual que hoy el selling-playbook compila a flags de
runtime. Cada módulo de equipo mapea a **tools del marketplace** según su rol:

| Módulo | Tools / runtime del marketplace (ejemplos) |
|--------|--------------------------------------------|
| Marketing & SDR | discovery, conversations, email, meetings (engagement feed) |
| AE | discovery questions, proposal, `--pricing-model/--price` |
| Services Consultants | meeting handshake (Calendly), evidencia de demo |
| Legal | contract/SOW, `--contract-terms/--scope-limits`, firma (`sign` = humano) |
| Security | due diligence docs, gating de cierre |
| Finance | payments/escrow, collection, `payment` = humano |
| ProServ/Managed | fulfillment tasks, active services, evidencia de entrega, `dispute` |
| CS & Support | inbox, Zendesk (tool support), N3 → escalación a ingeniería |

El **managed agent** carga el meta-playbook, **enruta por etapa del journey**, y en cada
etapa invoca el módulo correspondiente y sus tools. Las 4 acciones reservadas a humano
(`sign`, `deliver`, `payment`, `dispute`) siguen siendo el límite de autonomía
transversal.

---

## 8. Posicionamiento frente a Qualified.com

Qualified = **Piper, un AI SDR Agent**. Cubre **solo el primer módulo** del journey:
engancha leads inbound en web y email, los califica y **agenda la reunión**, luego hace
**handoff a un AE humano**. Es de un solo equipo (marketing/SDR) y termina en handoff
humano; su valor es velocidad y escala en top-of-funnel.

Lo que tú estás armando es **órdenes de magnitud más amplio**: el journey completo
**agente-a-agente** a través de los 8 equipos, con contratación, entrega, cobro y disputa
autónomos dentro de Standing Authorization. Qualified es una **excelente referencia para
el Módulo 1** (qué debe saber/hacer un agente SDR), pero no para los otros siete.

Lectura útil: si tuvieras que "comprar vs construir", Qualified valida que el módulo SDR
es viable y deseable hoy; el resto de tu playbook es lo diferencial de Simetrik/Belong.

---

## 9. Cómo continuar (siguiente paso concreto)

1. **Validar este mapa** (sección 3): ¿los 8 equipos y sus handoffs son correctos para
   Simetrik? Ajustar nombres/orden.
2. **Aprobar la plantilla de módulo** (sección 4): si te sirve, la congelamos.
3. **Scaffold del repo**: genero la carpeta del meta-playbook con los 8 módulos vacíos
   (Status: Missing, placeholders `TBD`, headers de navegación y bloque de Referencias ya
   cableado a las secciones canónicas) + el `index.md` con el Handoff Registry. Ruta
   propuesta:
   ```
   .belong/gtm-playbooks/simetrik/
     index.md
     01-marketing-sdr.md
     02-account-executive.md
     03-services-consultants.md
     04-legal.md
     05-security.md
     06-finance.md
     07-professional-managed-services.md
     08-customer-success-support.md
     handoff-registry.md
     authority-model.md
   ```
4. **Llenado guiado por equipo**, sección por sección, con los mismos gates de aprobación
   que ya usa el repo.
5. **Consistency check + runtime/tools mapping** → managed agent.
