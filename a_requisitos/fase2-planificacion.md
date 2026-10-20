# Fase II — Diseño conceptual y modelado (Planificación)

Requisitos de los Pasos 3 y 4 del enunciado. Cada paso lleva justificación teórica, descripción del procedimiento y capturas o figuras legibles.

## Paso 3 — Identificación de entidades y atributos

- **R3.1** Mínimo **cuatro (4) entidades** (tablas). Para GMAO tienen que quedar representados los conceptos que nombra el enunciado: **activos (máquinas), historial de fallas, órdenes de trabajo (correctivas/preventivas), repuestos utilizados y técnicos asignados**.
- **R3.1b** El correctivo y el preventivo tienen orígenes distintos, como en los gestores reales (ver `b_investigacion/gmao-sistemas-reales.md`): la OT correctiva atiende fallas y la OT preventiva nace de un **plan preventivo** (tarea y frecuencia por días u horas de operación). Modelo resultante: 7 tablas.
- **R3.2** Para cada tabla, listar sus atributos y **justificar el tipo de dato** elegido. Por ejemplo: `INTEGER` para identificadores, `VARCHAR` para textos, `REAL`/`FLOAT` para variables analógicas (horas, temperaturas, costos), `DATETIME` para marcas de tiempo.
- **R3.3** Explicar cómo SQLite trata los tipos declarados (afinidad de tipos) y el formato de fecha adoptado (ISO 8601, `AAAA-MM-DD HH:MM:SS`).

**Evidencia en el informe:** tabla con la estructura de campos y tipos de datos elegidos.

## Paso 4 — Construcción del modelo relacional

- **R4.1** Diagrama del modelo relacional (DER) con las **PK y FK claramente visibles** y las relaciones con su cardinalidad.
- **R4.2** Las relaciones muchos a muchos (por ejemplo órdenes de trabajo ↔ repuestos) se resuelven con una tabla intermedia.
- **R4.3** Diagrama dibujado como SVG para el informe (`c_prototipado/generar-der.py`; Mermaid no lo dejaba legible en A4), más la captura de la vista de estructura de DB Browser una vez creadas las tablas.

- **R4.4** Reglas que relacionan el tipo de OT con su origen, con el mecanismo que las hace cumplir (`CHECK` o *trigger*).
- **R4.5** El modelo se verifica con un prototipo en SQLite (`c_prototipado/prueba-modelo.py`): casos válidos aceptados y casos inválidos rechazados.

**Evidencia en el informe:** imagen clara del modelo relacional con las llaves PK/FK visibles.

## Criterios de aceptación de la fase

- [ ] ≥ 4 entidades que cubren máquinas, fallas, órdenes de trabajo, repuestos y técnicos, más el plan preventivo como origen de las OT preventivas.
- [ ] Cada atributo con su tipo de dato justificado.
- [ ] DER legible con PK, FK y cardinalidades.
- [ ] Reglas de origen de la OT definidas y verificadas en el prototipo.
