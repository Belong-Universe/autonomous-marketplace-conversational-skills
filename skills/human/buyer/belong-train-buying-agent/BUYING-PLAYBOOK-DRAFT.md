# Buying Playbook — Mapa y guía rápida

> Punto de entrada para entender el playbook del comprador de un vistazo.
> El detalle operativo de cada sección vive en la wiki: [`references/buying-playbook/index.md`](references/buying-playbook/index.md).
> Foco del playbook: **el pre-contrato (cotización + regateo)**. Lo posterior a la firma
> (delivery, evidencia, aceptación, pagos) ya está cubierto del lado del seller y se reusa.

---

## La idea en una frase

El Buying Playbook es el **reglamento durable** que deja a un Buying Agent comprar solo
(buscar, pedir cotizaciones, comparar, negociar, firmar) dentro de la Standing
Authorization, y escalar al Marketplace Inbox lo que se salga de ahí.

## Las dos capas (lo más importante)

El playbook funciona en dos capas. Mantenerlas separadas es el diseño central:
**se entrena una vez, y por cada compra solo se alimentan unos pocos valores.**

- **Capa 1 — Playbook estático (se entrena 1 vez).** Las 10 secciones son política durable:
  describen *cómo* compra el agente. No cambian entre compras.
- **Capa 2 — Buying Request dinámico (por cada compra).** Un puñado de valores que entran
  vía `start-buying-request` (o se ajustan con `$belong-steer-buying-agent`), nunca se
  reescriben en el playbook: la necesidad concreta, el deadline, el presupuesto y el
  techo (`max_spend`), y constraints puntuales.

Por eso **solo las secciones 1 y 2 se sienten dinámicas**: son las únicas que reciben
valores por compra. Las secciones 3–10 son política estática pura.

```
PLAYBOOK (estático, 1 vez)              BUYING REQUEST (dinámico, por compra)
└── 10 secciones de política     ◄────  necesidad · deadline · budget · max_spend · constraints
```

---

## Las 10 secciones del playbook

| # | Sección | Para qué sirve | Capa |
| --- | --- | --- | --- |
| 1 | [Buying Goals And Needs](references/buying-playbook/01-buying-goals-and-needs.md) | *Cómo* defino qué necesito, alcance, criterio de éxito y plazo. La necesidad concreta entra por compra. | **Dinámica** |
| 2 | [Budget And Payment](references/buying-playbook/02-budget-and-payment.md) | Mi postura de pago y mi regla de techo. El presupuesto y el `max_spend` de cada compra entran por compra. | **Dinámica** |
| 3 | [Provider Preferences](references/buying-playbook/03-provider-preferences.md) | Mis criterios sobre proveedores: seguridad, certificaciones (ISO 27001, ISO 9001, SOC 2), años de experiencia, reputación, jurisdicción. Distingue *requisitos duros* de *preferencias*. | Estática |
| 4 | [Selection And RFP Rules](references/buying-playbook/04-selection-and-rfp-rules.md) | Directo vs competitivo, cómo armo el RFP y la rúbrica para comparar cotizaciones (más allá del precio). | Estática |
| 5 | [Negotiations](references/buying-playbook/05-negotiations.md) | *Cómo* regateo: oferta inicial, escalera de concesiones, señales que leo, walk-away, y el no-ZOPA. | Estática |
| 6 | [Legal And Contracts](references/buying-playbook/06-legal-and-contracts.md) | Hasta cuánto firma solo el agente, términos obligatorios, criterios de aceptación. | Estática |
| 7 | [Escalations](references/buying-playbook/07-escalations.md) | Qué decisiones frenan para un humano, por qué canal, y quién las dueña. | Estática |
| 8 | [Disputes And Reputation](references/buying-playbook/08-disputes-and-reputation.md) | Postura ante delivery contestado y cómo califico proveedores. | Estática |
| 9 | [Optimization Objective](references/buying-playbook/09-optimization-objective.md) | Mi **norte**: qué priorizo (costo/calidad/velocidad/relación) y la regla de desempate. Las secciones 4 y 5 heredan sus pesos de aquí. | Estática |
| 10 | [Human-To-Human Meetings](references/buying-playbook/10-human-to-human-meetings.md) | Cuándo me reúno con un proveedor, mis horarios/timezone y la autoridad de agenda (Calendly). | Estática |

## Las páginas sin número (el *proceso*, no el playbook)

Estas no son secciones del playbook: son las herramientas que rodean su creación.

| Página | Para qué sirve |
| --- | --- |
| [Source Prefill](references/buying-playbook/source-prefill.md) | Antes de redactar: minar fuentes existentes (política de compras, RFPs viejos, vendor lists) y prerellenar el playbook para no interrogar al humano. |
| [Checkpoints And Approval](references/buying-playbook/checkpoints-and-approval.md) | Entre secciones: tabla de progreso (%) y el gate de aprobación que impide avanzar sin OK del humano. Re-confirma en vivo los campos de autoridad antes de activar. |
| [Consistency Check](references/buying-playbook/consistency-check.md) | Antes de activar: 8 chequeos cruzados para que las secciones no se contradigan (ej: que el regateo no supere el techo, que un proveedor bloqueado no pueda ganar). |
| [Generated Playbook Folder](references/buying-playbook/generated-playbook-folder.md) | Define los archivos markdown que se generan durante el entrenamiento en `.belong/buying-playbooks/<org-slug>/`. |
| [Examples](references/buying-playbook/examples.md) | Exactamente un ejemplo bien hecho y uno mal hecho de una sección (Negotiations, con el caso $1.800). |

---

## El flujo de cotización (dónde se usan las secciones)

```
start-buying-request   ── necesidad + presupuesto + techo (sec. 1, 2) ──►
   search / engage     ── filtra por criterios de proveedor (sec. 3) ───►
        ◄── discovery questionnaire (el seller pregunta para cotizar) ──
   answer-discovery     ─────────────────────────────────────────────►
        ◄── create-proposals: cotización firmada por el seller ────────
   compare-proposals    ── rúbrica + norte (sec. 4, 9) ─────────────────
   negotiate            ── regateo por señales (sec. 5) ◄──────────────►
        ¿hay ZOPA?
          sí → sign      ── dentro de autoridad (sec. 6) ───────────────
          no → escalar al Marketplace Inbox (sec. 5 no-ZOPA, sec. 7)
```

Los humanos no se conectan; **sus agentes sí**, en este intercambio. El buyer playbook
llena el lado del comprador; el seller playbook (ya existente) llena el del vendedor.

## Ejemplo del regateo (techo $1.800 vs piso $2.000)

Está trabajado paso a paso en
[`examples.md`](references/buying-playbook/examples.md). El punto clave es el **no-ZOPA**:
cuando el piso del vendedor supera mi techo, el agente **no sube el techo solo** — escala
al Inbox con un Decision Explanation. Reparto: la *decisión* es política del playbook
(sección 5); la *detección y el enforcement* son del runtime de negociación.

## Preguntas abiertas

1. **Señales de percepción:** ¿qué señales expone hoy `belong_mock.py` (competencia,
   reputación, urgencia)? De eso depende que `perceived_signals` sea real o aspiracional.
2. **No-ZOPA en runtime:** confirmar dónde se implementa la detección `floor > ceiling`.
3. **Constraints por compra vs criterios durables:** afinar cuándo un requisito puntual
   (sección 3) viaja en el Buying Request (`--constraints`) en lugar del playbook.
