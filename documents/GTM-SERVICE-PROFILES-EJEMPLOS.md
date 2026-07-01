# GTM — Ejemplos de Service Profiles para Simetrik

> Qué es un Service Profile, 3 ejemplos para Simetrik, y por qué conviene tenerlos
> separados (mismo Core, parámetros distintos).

---

## Recordatorio: qué es un Service Profile

Un perfil **delgado** con solo lo que cambia entre servicios: value prop, ICP, modelo de
precio, discovery propio, alcance y requisitos de cumplimiento. El **Core** (la maquinaria
comercial: calificar, contratar, asegurar, cobrar, disputar) es el mismo para todos; el
perfil solo **rellena los slots** de las secciones que dependen del servicio.

Regla para decidir si algo es un perfil aparte o una variante:

- **Perfil aparte** → si cambia el comprador (ICP), la propuesta de valor, el modelo de
  precio o el motion de venta. Es **comprable por separado**.
- **Misma perfil (variante)** → si solo cambian niveles/tiers/opciones del mismo servicio.

---

## Perfil A — Reconciliation Platform (SaaS)

```markdown
service-slug: reconciliation-platform
Feeds core sections: 01, 02, 03, 04, 09

value-prop: Plataforma no-code para automatizar la conciliación de transacciones y los
            controles financieros. Cierres más rápidos y menos descuadres, sin construir
            integraciones a mano.
ICP: fintechs, PSPs y bancos con >1M transacciones/mes. Comprador: Finance Ops /
     Controller / IT.
pricing-model: recurring
price: suscripción por tiers (desde ~USD 4,000/mes)
discovery-questions: volumen de transacciones, # de fuentes/sistemas, tiempo de cierre
     actual, herramientas hoy.
scope: acceso a la plataforma + connectors + soporte; el cliente construye y opera sus
     propios modelos (o con implementación).
compliance-reqs: SOC2, residencia de datos.
sales-motion: venta de valor product-led; revisión de seguridad pesada.
```

## Perfil B — Managed Reconciliation ("lo hacemos por ti" / outsourcing)

```markdown
service-slug: managed-reconciliation
Feeds core sections: 01, 02, 03, 04, 05, 09

value-prop: Simetrik opera la conciliación por ti — construimos, corremos y monitoreamos.
            Obtienes resultados sin necesitar un equipo interno de operaciones.
ICP: empresas sin capacidad operativa interna o que quieren tercerizar. Comprador:
     CFO / Head of Operations.
pricing-model: recurring (+ milestone de setup inicial)
price: fee mensual gestionado según volumen y alcance del SLA
discovery-questions: ¿tienes equipo interno de conciliación?, volúmenes, SLAs requeridos,
     manejo de excepciones.
scope: servicio gestionado con SLA, manejo de excepciones, reporte mensual. **La entrega
     la ejecuta el Implementation/Managed Services Agent** (handoff).
compliance-reqs: SOC2 + acuerdos de procesamiento de datos + SLAs operativos.
sales-motion: venta de servicios; negociación de SLA; scoping con ProServ.
```

## Perfil C — Regulatory & Management Reporting

```markdown
service-slug: regulatory-reporting
Feeds core sections: 01, 02, 03, 04, 05

value-prop: Automatiza el reporte regulatorio y de gestión a partir de datos ya
            conciliados. Listo para auditoría, con trazabilidad completa.
ICP: entidades reguladas (bancos, aseguradoras, fintechs reguladas). Comprador:
     Compliance / Risk / Controller.
pricing-model: consumption (por reporte/volumen) o recurring
price: según tipo y frecuencia de reportes
discovery-questions: ¿qué reguladores?, tipos de reporte, frecuencia, proceso actual.
scope: módulo de reporting + plantillas + audit trail.
compliance-reqs: específicos por regulador (más pesados).
sales-motion: dirigido por cumplimiento; stakeholders distintos (riesgo/compliance).
```

---

## Por qué deben estar separados

| Dimensión | A — Platform (SaaS) | B — Managed | C — Reporting |
|---|---|---|---|
| Comprador (ICP) | Finance Ops / IT | CFO / Head of Ops | Compliance / Risk |
| Propuesta de valor | Tú automatizas | Lo hacemos por ti | Reporte regulatorio listo |
| Modelo de precio | recurring | recurring + setup | consumption / recurring |
| Discovery | técnico/volumen | capacidad/SLA | reguladores/reportes |
| Entrega | cliente (o impl.) | Implementation Agent | módulo + plantillas |
| Motion de venta | product-led | servicios/SLA | compliance-driven |

Tres razones concretas para separarlos en perfiles (no en un solo perfil, ni en playbooks
completos distintos):

1. **Calificación correcta.** El agente debe darle la propuesta de valor y las preguntas
   de discovery correctas a cada comprador. Si los mezclas en un perfil, le ofrece "lo
   hacemos por ti" a quien quería licenciar software, y pierde el deal.
2. **Precio correcto.** Cada uno usa un modelo de precio distinto (recurring vs
   consumption vs setup+recurring). Un solo perfil no puede declarar tres modelos sin
   ambigüedad.
3. **Sin duplicar la maquinaria.** Calificar, contratar, asegurar, cobrar y disputar es
   **igual** para los tres → vive una sola vez en el Core. Hacer tres playbooks completos
   duplicaría todo eso y se desincronizaría. Tres perfiles + un Core = una sola fuente de
   verdad.

> Un comprador puede combinar varios (ej. Platform + Reporting); cada uno se vende con su
> propio perfil y el agente los coordina del lado de la demanda.
