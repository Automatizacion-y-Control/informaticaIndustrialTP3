# Fase IV — Explotación de datos y reportes industriales (Consulta)

Requisitos de los Pasos 7, 8 y 9 del enunciado. Cada consulta lleva la necesidad que resuelve, el código SQL en texto plano y la captura de su resultado.

## Paso 7 — Consultas de selección y filtrado básico

- **R7.1** **Tres (3) consultas** con `SELECT`, `WHERE`, `ORDER BY` y operadores lógicos (`AND`, `OR`, `NOT`, `BETWEEN`, `IN`…), cada una pensada para una necesidad del supervisor de planta.
- **R7.2** Para GMAO se incluyen los ejemplos del enunciado:
  1. **Fallas ocurridas entre dos fechas.**
  2. **Repuestos con stock crítico.**
  3. **Órdenes de trabajo correctivas que siguen abiertas.**

**Evidencia en el informe:** código SQL de los `SELECT` con filtros y capturas de los resultados.

## Paso 8 — Consultas de agrupación y estadísticas

- **R8.1** **Dos (2) consultas** con funciones de agregación (`COUNT`, `SUM`, `AVG`, `MAX`) combinadas con `GROUP BY`.
- **R8.2** Para GMAO:
  1. **Cantidad de fallas por máquina, para identificar el activo más crítico** (ejemplo del enunciado).
  2. **Horas-hombre y cantidad de órdenes por tipo de mantenimiento.**

**Evidencia en el informe:** código SQL de las consultas con `GROUP BY` y las estadísticas obtenidas.

## Paso 9 — Consultas de integración de tablas (JOINs)

- **R9.1** **Dos (2) consultas** con `INNER JOIN` (o `LEFT JOIN`) que crucen varias tablas y muestren **nombres legibles en lugar de IDs**: el operador de planta no lee códigos numéricos.
- **R9.2** Para GMAO:
  1. **Órdenes de trabajo con el nombre de la máquina, la descripción de la falla y el nombre del técnico asignado** (ejemplo obligatorio del enunciado). Con el modelo de la Fase II, la falla se vincula con `LEFT JOIN fallas ON fallas.id_ot = ordenes_trabajo.id_ot`; para las preventivas se muestra la tarea del plan.
  2. **Repuestos consumidos por orden de trabajo, con la máquina y el costo.**

**Evidencia en el informe:** código SQL usando `JOIN` para vincular datos relacionales y capturas de los resultados.

## Criterios de aceptación de la fase

- [ ] 3 consultas de filtrado con `WHERE`, `ORDER BY` y operadores lógicos.
- [ ] 2 consultas con funciones de agregación y `GROUP BY`.
- [ ] 2 consultas con `JOIN`, incluida la de órdenes de trabajo con máquina, falla y técnico.
- [ ] Cada consulta con su captura de resultado, que no está vacío.
- [ ] Todas las consultas están en el `.sql` de respaldo, en el mismo orden que en el informe.
