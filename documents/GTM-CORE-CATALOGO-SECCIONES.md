# GTM Core Playbook — Catálogo de secciones

> Cada sección con: **qué es** (para que el agente sepa para qué sirve y navegue la wiki
> autónomamente), **referencias internas** (a qué otras secciones apunta, más allá de
> Next/Prev) y **lee del profile** (qué slots toma del Service Profile activo).
> Esto reemplaza el "mapa de dependencias" rústico del doc anterior.

Hay **dos tipos de relación** entre secciones:

- **Lineal** (`Prev` / `Next`): el orden de lectura durante setup/entrenamiento.
- **Referencias internas** (*see-also*): enlaces a secciones **no adyacentes** que el
  agente consulta según la situación. No es un orden de carga; es para que **sepa a dónde
  ir** cuando opera.

---

## 01 · Positioning & Value
**Qué es:** el posicionamiento de Simetrik a nivel compañía y el marco de valor que aplica
a cualquier servicio. El value prop concreto baja del profile.
**Referencias internas:** 02 Qualification · 03 Monetization rules
**Lee del profile:** `value-prop`, `proof-points`

## 02 · Qualification
**Qué es:** filosofía y criterios de calificación de fit (presupuesto, autoridad,
necesidad, tiempo); cuándo declinar.
**Referencias internas:** 01 Positioning · 06 Meetings · 09 Capacity & Objective
**Lee del profile:** `ICP`, `discovery-questions`, `casos-a-evitar`

## 03 · Monetization rules
**Qué es:** modelos de precio permitidos, guardrails comerciales, escrow y cuándo una
excepción de pago necesita aprobación.
**Referencias internas:** 07 Escalations & Authority · 04 Legal & Contracts · 09 Capacity
**Lee del profile:** `pricing-model`, `price`

## 04 · Legal & Contracts
**Qué es:** términos del Contrato/SOW, entregables, evidencia, criterios de aceptación y
autoridad de firma.
**Referencias internas:** 05 Security & Diligence · 07 Authority · 08 Disputes ·
Interfaces/Implementation
**Lee del profile:** `scope`, `deliverables`

## 05 · Security & Diligence
**Qué es:** el gate de seguridad/cumplimiento que debe pasar antes de cerrar.
**Referencias internas:** 04 Legal & Contracts · 07 Escalations & Authority
**Lee del profile:** `compliance-reqs` (opcional)

## 06 · Meetings
**Qué es:** cuándo proponer/aceptar reuniones humano-a-humano y el handshake de agenda
(Calendly).
**Referencias internas:** 07 Authority (autoridad para agendar) · 02 Qualification
**Lee del profile:** — (puro core)

## 07 · Escalations & Authority
**Qué es:** el modelo de autoridad transversal — qué hace el agente solo, qué escala y qué
es **siempre humano** (`sign`, `deliver`, `payment`, `dispute`).
**Referencias internas:** la referencian 03 · 04 · 05 · 06 · 08 (es la sección eje)
**Lee del profile:** `authority-overrides` (opcional, por servicio)

## 08 · Disputes & Reputation
**Qué es:** postura ante disputas, estándar de evidencia, reembolso/rework y reputación.
**Referencias internas:** 04 Legal & Contracts · 07 Authority · Interfaces/Implementation
**Lee del profile:** — (puro core)

## 09 · Capacity & Objective
**Qué es:** capacidad de entrega (cuántos servicios en paralelo, lead time) y qué optimiza
el agente (win rate, margen, utilización).
**Referencias internas:** 02 Qualification · 03 Monetization rules
**Lee del profile:** `availability`, `lead-time`

---

## Interfaces (handoffs hacia lo externo)

### interfaces/implementation-agent
**Qué es:** el handoff de entrega hacia el Implementation Agent (qué se le pasa, qué se
espera de vuelta para confirmar aceptación/cobro).
**Referencias internas:** 04 Legal (qué se entrega) · 08 Disputes (disputas de entrega)

### interfaces/support-n3
**Qué es:** la escalación de soporte nivel 3 hacia el equipo de Ingeniería.
**Referencias internas:** 07 Escalations & Authority · 08 Disputes

---

## Matriz de referencias (vista compacta)

| Sección | Referencia a → | ¿Lee profile? |
|---|---|---|
| 01 Positioning | 02, 03 | sí |
| 02 Qualification | 01, 06, 09 | sí |
| 03 Monetization | 07, 04, 09 | sí |
| 04 Legal | 05, 07, 08, Impl | sí |
| 05 Security | 04, 07 | opcional |
| 06 Meetings | 07, 02 | no |
| 07 Authority | (eje, referenciada por casi todas) | opcional |
| 08 Disputes | 04, 07, Impl | no |
| 09 Capacity | 02, 03 | sí |

El `index.md` lleva esta misma descripción de una línea por sección, de modo que el agente
sabe **para qué sirve cada una** y puede saltar a la correcta sin cargar todo el playbook.
