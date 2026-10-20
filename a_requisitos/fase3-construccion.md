# Fase III — Implementación y carga de datos mediante SQL (Construcción)

Requisitos de los Pasos 5 y 6 del enunciado. Cada paso lleva justificación teórica, descripción del procedimiento y capturas legibles. Parten del modelo validado en la Fase II: 7 tablas (`maquinas`, `tecnicos`, `planes_preventivos`, `ordenes_trabajo`, `fallas`, `repuestos`, `ot_repuestos`).

## Paso 5 — Scripts de creación de tablas (DDL)

- **R5.1** Una sentencia `CREATE TABLE` por cada tabla diseñada en la Fase II, escrita a mano.
- **R5.2** Restricciones de integridad explícitas: `NOT NULL`, `PRIMARY KEY` y `FOREIGN KEY … REFERENCES`, más `UNIQUE` y `CHECK` donde el Paso 3 los define.
- **R5.3** El orden de creación respeta las dependencias: `maquinas`, `tecnicos`, `repuestos`, `planes_preventivos`, `ordenes_trabajo`, `fallas`, `ot_repuestos`.
- **R5.4** El script empieza con `PRAGMA foreign_keys = ON;` para que SQLite verifique las claves foráneas.
- **R5.5** Reglas del proceso definidas en el Paso 4:
  - `CHECK` de tabla en `ordenes_trabajo`: la preventiva tiene `id_plan` y la correctiva no.
  - *Trigger* en `ordenes_trabajo` (al insertar y al modificar): la OT preventiva es de la misma máquina que su plan.
  - *Trigger* en `fallas` (al insertar y al modificar `id_ot`): la falla solo se asigna a una OT correctiva de la misma máquina.
- **R5.6** Captura del código **ejecutado con éxito** en DB Browser (mensaje sin errores) y de la estructura resultante (pestaña *Estructura de la base de datos*), que además completa la evidencia del Paso 4.

**Evidencia en el informe:** capturas de pantalla y código de los `CREATE TABLE` ejecutados.

## Paso 6 — Script de inserción de datos de planta (DML)

- **R6.1** Sentencias `INSERT INTO` con un **mínimo de cinco (5) registros por tabla**.
- **R6.2** Datos simulados pero realistas: nombres y modelos de máquinas reales, marcas de tiempo, nombres de técnicos, códigos de repuestos y de planes, números de orden.
- **R6.3** Orden de carga compatible con las FK y los *triggers*: `maquinas`, `tecnicos`, `repuestos`, `planes_preventivos`, `ordenes_trabajo`, `fallas`, `ot_repuestos`.
- **R6.4** Datos coherentes entre tablas que **permitan que las consultas de la Fase IV devuelvan resultados significativos**:
  - fallas en distintas fechas y una máquina con más fallas que el resto;
  - al menos una falla **pendiente** (sin OT) y una OT que agrupe **dos fallas**;
  - OT preventivas generadas desde planes por días y por horas;
  - OT correctivas y preventivas en los tres estados (`PENDIENTE`, `EN CURSO`, `CERRADA`);
  - al menos un repuesto con stock por debajo del mínimo.
- **R6.5** Captura de cada tabla poblada (pestaña *Hojear datos*).
- **R6.6** Opcional, como evidencia de la integridad: captura de un `INSERT` inválido rechazado por la base (por ejemplo, una OT preventiva sin plan).

**Evidencia en el informe:** capturas de pantalla y código de los `INSERT INTO` con los datos cargados.

## Criterios de aceptación de la fase

- [ ] `CREATE TABLE` con `NOT NULL`, `PRIMARY KEY` y `FOREIGN KEY … REFERENCES`, y captura de la ejecución exitosa.
- [ ] `CHECK` y *triggers* de las reglas del Paso 4 implementados y probados.
- [ ] ≥ 5 registros por tabla, realistas y coherentes entre tablas.
- [ ] Captura de cada tabla poblada.
- [ ] El DDL y el DML se ejecutan de corrido sobre una base vacía sin errores.
