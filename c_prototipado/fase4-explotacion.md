# Fase IV — Explotación de datos y reportes industriales (La Consulta)

Con la base construida y cargada, en esta fase se la consulta para responder preguntas concretas del supervisor de planta. Se escribieron siete consultas `SELECT`, en orden de complejidad creciente: filtrado sobre una sola tabla (Paso 7), estadísticas con funciones de agregación (Paso 8) y cruce de varias tablas para mostrar nombres legibles en lugar de identificadores (Paso 9). Todas se ejecutaron en DB Browser for SQLite sobre `gmao.db` y están en el script `fase4-consultas.sql`, en el mismo orden que en este informe.

## Paso 7 — Consultas de selección y filtrado básico

### Justificación teórica

La sentencia `SELECT` es la parte del DML que lee datos sin modificarlos. Su forma básica es:

```sql
SELECT columnas FROM tabla WHERE condicion ORDER BY columna [ASC | DESC];
```

- `SELECT` elige las columnas a mostrar. También acepta expresiones calculadas, a las que se les da un nombre con `AS` (alias).
- `FROM` indica la tabla de origen.
- `WHERE` filtra las filas: solo pasan las que cumplen la condición.
- `ORDER BY` ordena el resultado. Por defecto es ascendente (`ASC`); `DESC` invierte el orden.

Aunque se escribe en ese orden, el motor la evalúa en otro: primero `FROM`, después `WHERE`, luego `SELECT` y al final `ORDER BY`. Por eso un alias definido en el `SELECT` se puede usar en el `ORDER BY` pero no en el `WHERE`.

La condición del `WHERE` se arma con operadores de comparación y operadores lógicos:

| Operador | Significado | Uso en las consultas |
|---|---|---|
| `=`, `<>`, `<`, `<=`, `>`, `>=` | Comparación | `stock_actual <= stock_minimo` |
| `AND` | Se cumplen las dos condiciones | Rango de fechas y severidad |
| `OR` | Se cumple al menos una | Equivale a una lista de `IN` |
| `NOT` | Niega la condición | `NOT estado = 'CERRADA'` |
| `BETWEEN a AND b` | Rango, con los dos extremos incluidos | Fechas de las fallas |
| `IN (…)` | El valor está en la lista | `severidad IN ('ALTA', 'MEDIA')` |

Las fechas se guardaron como texto en formato ISO 8601 (`AAAA-MM-DD HH:MM:SS`). En ese formato el orden alfabético coincide con el cronológico, de modo que `BETWEEN` y `ORDER BY` funcionan sobre las fechas sin necesidad de convertirlas.

### Procedimiento

1. Se abrió `gmao.db` en DB Browser for SQLite y se pasó a la pestaña **Ejecutar SQL**.
2. Se escribió cada consulta, se la seleccionó y se ejecutó con **Ejecutar todo** (`F5`): con texto seleccionado, DB Browser ejecuta solo la selección.
3. Se revisó el resultado en la grilla inferior y la cantidad de filas en el panel de mensajes.
4. Como las consultas solo leen, no hubo cambios que guardar.

### Consulta 7.1 — Fallas entre dos fechas

**Necesidad:** el supervisor revisa las fallas importantes de un período, por ejemplo para la reunión mensual de mantenimiento. Se combinan `BETWEEN` para el rango de fechas, `IN` para la severidad y `AND` para exigir las dos condiciones.

```sql
-- ---------------------------------------------------------------------
-- Consulta 7.1 — Fallas entre dos fechas
-- Fallas de severidad ALTA o MEDIA registradas entre el 15/09 y el 10/10.
-- ---------------------------------------------------------------------
SELECT id_falla, fecha_hora, id_maquina, descripcion, tipo_falla,
       severidad, horas_parada
FROM fallas
WHERE fecha_hora BETWEEN '2026-09-15 00:00:00' AND '2026-10-10 23:59:59'
  AND severidad IN ('ALTA', 'MEDIA')
ORDER BY fecha_hora;
```

<!-- CAPTURA paso7_01: Ejecutar SQL con la consulta 7.1 y su resultado (5 filas) -->

**Resultado:** cinco fallas entre el 15/09 y el 10/10. La falla de severidad baja de la inyectora (12/10) queda afuera por la fecha y por la severidad.

### Consulta 7.2 — Repuestos con stock crítico

**Necesidad:** el pañol tiene que saber qué repuestos reponer antes de que una falla deje una máquina parada esperando una pieza. Un repuesto está en estado crítico cuando su stock llega al mínimo (punto de reposición). La columna calculada `faltante` ordena la lista por urgencia.

```sql
-- ---------------------------------------------------------------------
-- Consulta 7.2 — Repuestos con stock crítico
-- Repuestos en el punto de reposición o por debajo. Primero los que
-- más faltan.
-- ---------------------------------------------------------------------
SELECT codigo, descripcion, stock_actual, stock_minimo,
       stock_minimo - stock_actual AS faltante
FROM repuestos
WHERE stock_actual <= stock_minimo
ORDER BY faltante DESC, codigo;
```

<!-- CAPTURA paso7_02: Ejecutar SQL con la consulta 7.2 y su resultado (4 filas) -->

**Resultado:** cuatro repuestos. El filtro del compresor (faltan 2) y la placa SMB del robot (stock 0) están por debajo del mínimo; la correa del torno y el kit de sellos de la prensa están justo en el mínimo.

### Consulta 7.3 — Órdenes correctivas abiertas

**Necesidad:** las correctivas abiertas son máquinas con una falla sin resolver; el supervisor las sigue a diario. Se usa `NOT` para excluir las cerradas, lo que equivale a `estado IN ('PENDIENTE', 'EN CURSO')`.

```sql
-- ---------------------------------------------------------------------
-- Consulta 7.3 — Órdenes correctivas abiertas
-- Correctivas que no están cerradas, de la más antigua a la más nueva.
-- ---------------------------------------------------------------------
SELECT nro_ot, fecha_emision, id_maquina, id_tecnico, estado, tarea
FROM ordenes_trabajo
WHERE tipo = 'CORRECTIVA'
  AND NOT estado = 'CERRADA'
ORDER BY fecha_emision;
```

<!-- CAPTURA paso7_03: Ejecutar SQL con la consulta 7.3 y su resultado (2 filas) -->

**Resultado:** dos órdenes abiertas: el cambio de rodamiento del torno CNC (en curso desde el 07/10) y el diagnóstico del cambiador de herramientas del centro de mecanizado (pendiente). Las órdenes preventivas abiertas no aparecen porque el filtro pide solo correctivas.

## Paso 8 — Consultas de agrupación y estadísticas

### Justificación teórica

Las **funciones de agregación** resumen un conjunto de filas en un solo valor:

| Función | Devuelve |
|---|---|
| `COUNT(*)` | Cantidad de filas |
| `SUM(columna)` | Suma de los valores |
| `AVG(columna)` | Promedio de los valores |
| `MAX(columna)` / `MIN(columna)` | Valor máximo / mínimo |

Con `GROUP BY` el cálculo se hace por grupos: las filas que comparten el valor de la columna indicada forman un grupo y cada grupo da una fila del resultado. En el `SELECT` solo pueden ir las columnas del `GROUP BY` y funciones de agregación. Si hace falta filtrar grupos (por ejemplo, máquinas con más de dos fallas) se usa `HAVING`, porque `WHERE` filtra filas antes de agrupar.

Las funciones de agregación **ignoran los `NULL`**, salvo `COUNT(*)`, que cuenta filas. Esto importa en las horas-hombre: las órdenes pendientes todavía no tienen horas cargadas, cuentan como órdenes pero no entran en la suma ni en el promedio.

### Procedimiento

Se siguió el mismo procedimiento que en el Paso 7: cada consulta se ejecutó sola en la pestaña **Ejecutar SQL** y se revisó la grilla de resultados.

### Consulta 8.1 — Fallas por máquina (activo más crítico)

**Necesidad:** identificar el activo que más falla para priorizar su mantenimiento y revisar su plan preventivo. Se cuentan las fallas de cada máquina y se suman sus horas de parada, que son las que miden el impacto en la producción.

```sql
-- ---------------------------------------------------------------------
-- Consulta 8.1 — Fallas por máquina (activo más crítico)
-- Cantidad de fallas y horas de parada acumuladas por máquina.
-- ---------------------------------------------------------------------
SELECT id_maquina,
       COUNT(*)          AS cantidad_fallas,
       SUM(horas_parada) AS horas_parada_total,
       MAX(fecha_hora)   AS ultima_falla
FROM fallas
GROUP BY id_maquina
ORDER BY cantidad_fallas DESC, horas_parada_total DESC;
```

<!-- CAPTURA paso8_01: Ejecutar SQL con la consulta 8.1 y su resultado (6 filas) -->

**Resultado:** la máquina 1, el torno CNC, es el activo más crítico: 3 fallas y 10,5 horas de parada, todas mecánicas en el husillo. Le siguen la prensa hidráulica (máquina 5) y el robot de soldadura (máquina 4), con 2 fallas cada uno; la prensa queda primero por tener más horas de parada (6 contra 5). El resultado muestra el identificador de la máquina: en el Paso 9 se resuelve el nombre con un `JOIN`.

### Consulta 8.2 — Horas-hombre por tipo de mantenimiento

**Necesidad:** comparar el esfuerzo dedicado al mantenimiento correctivo y al preventivo. Una planta con mucho correctivo trabaja apagando incendios; el objetivo es desplazar horas hacia el preventivo.

```sql
-- ---------------------------------------------------------------------
-- Consulta 8.2 — Horas-hombre por tipo de mantenimiento
-- Órdenes emitidas y horas-hombre registradas, correctivo vs preventivo.
-- ---------------------------------------------------------------------
SELECT tipo,
       COUNT(*)                    AS cantidad_ot,
       SUM(horas_hombre)           AS horas_hombre_total,
       ROUND(AVG(horas_hombre), 2) AS horas_hombre_promedio,
       MAX(horas_hombre)           AS horas_hombre_maxima
FROM ordenes_trabajo
GROUP BY tipo
ORDER BY horas_hombre_total DESC;
```

<!-- CAPTURA paso8_02: Ejecutar SQL con la consulta 8.2 y su resultado (2 filas) -->

**Resultado:** el correctivo concentra 8 órdenes y 23,25 horas-hombre, el 77,5 % de las 30 horas registradas; el preventivo, 5 órdenes y 6,75 horas. El promedio por orden correctiva (3,32 h) duplica al de la preventiva (1,69 h). Los promedios se calculan sobre las órdenes con horas cargadas: 7 de las 8 correctivas y 4 de las 5 preventivas, porque las dos pendientes tienen `horas_hombre` en `NULL`.

## Paso 9 — Consultas de integración de tablas (JOINs)

### Justificación teórica

En un modelo normalizado cada dato está en una sola tabla y las demás lo referencian por su clave. Una orden de trabajo guarda `id_maquina = 1`, no el texto «Torno CNC». Para mostrar la información completa hay que **reunir** las tablas siguiendo las relaciones PK–FK del DER, con `JOIN … ON`:

- `INNER JOIN` devuelve solo las filas que tienen pareja en las dos tablas.
- `LEFT JOIN` devuelve todas las filas de la tabla de la izquierda; si no tienen pareja, las columnas de la derecha quedan en `NULL`.

Los **alias** de tabla (`ordenes_trabajo AS ot`) acortan el código e indican de qué tabla sale cada columna cuando dos tablas tienen columnas con el mismo nombre, como `id_maquina`. El operador `||` concatena texto y `COALESCE(a, b)` devuelve el primer valor que no sea `NULL`.

### Procedimiento

Se siguió el mismo procedimiento que en los Pasos 7 y 8. Antes de escribir cada consulta se tomó del DER el camino de claves entre las tablas a cruzar.

### Consulta 9.1 — Órdenes con máquina, falla y técnico

**Necesidad:** el listado de órdenes que lee el personal de planta, con el nombre de la máquina, el motivo de la orden y el técnico asignado en lugar de los identificadores.

Máquina y técnico son obligatorios en toda orden, por eso se unen con `INNER JOIN`. La falla y el plan, en cambio, dependen del tipo de orden: la correctiva tiene falla y no tiene plan, y la preventiva al revés. Con `INNER JOIN fallas` desaparecerían las 5 órdenes preventivas; con `LEFT JOIN` se conservan todas y `COALESCE` muestra, en una sola columna, la descripción de la falla o la tarea del plan.

```sql
-- ---------------------------------------------------------------------
-- Consulta 9.1 — Órdenes con máquina, falla y técnico
-- Para las correctivas se muestra la falla y para las preventivas, la
-- tarea del plan. Una OT que atiende dos fallas aparece dos veces.
-- ---------------------------------------------------------------------
SELECT ot.nro_ot,
       ot.tipo,
       m.nombre                            AS maquina,
       COALESCE(f.descripcion,
                'Plan ' || p.codigo || ': ' || p.tarea) AS motivo,
       t.apellido || ', ' || t.nombre      AS tecnico,
       ot.estado
FROM ordenes_trabajo AS ot
INNER JOIN maquinas AS m           ON m.id_maquina = ot.id_maquina
INNER JOIN tecnicos AS t           ON t.id_tecnico = ot.id_tecnico
LEFT JOIN fallas AS f              ON f.id_ot = ot.id_ot
LEFT JOIN planes_preventivos AS p  ON p.id_plan = ot.id_plan
ORDER BY ot.nro_ot, f.fecha_hora;
```

<!-- CAPTURA paso9_01: Ejecutar SQL con la consulta 9.1 y su resultado (14 filas) -->

**Resultado:** 14 filas para las 13 órdenes, porque la OT-2026-0107 atiende dos fallas de la prensa hidráulica (pérdida de presión y fuga en el sello) y aparece una vez por cada una. La falla pendiente de la inyectora no figura porque todavía no tiene orden: la consulta parte de las órdenes.

### Consulta 9.2 — Repuestos consumidos por orden de trabajo

**Necesidad:** conocer el costo en repuestos de cada intervención, para imputarlo a la máquina y controlar el gasto de mantenimiento. La consulta parte de la tabla intermedia `ot_repuestos`, que resuelve la relación N:M, y la une con la orden, la máquina y el repuesto. El costo de cada consumo se calcula como cantidad por costo unitario.

```sql
-- ---------------------------------------------------------------------
-- Consulta 9.2 — Repuestos consumidos por orden de trabajo
-- Con la máquina, la cantidad y el costo de cada consumo.
-- ---------------------------------------------------------------------
SELECT ot.nro_ot,
       m.nombre                        AS maquina,
       r.descripcion                   AS repuesto,
       otr.cantidad,
       r.costo_unitario,
       otr.cantidad * r.costo_unitario AS costo_total
FROM ot_repuestos AS otr
INNER JOIN ordenes_trabajo AS ot ON ot.id_ot = otr.id_ot
INNER JOIN maquinas AS m         ON m.id_maquina = ot.id_maquina
INNER JOIN repuestos AS r        ON r.id_repuesto = otr.id_repuesto
ORDER BY ot.nro_ot, r.descripcion;
```

<!-- CAPTURA paso9_02: Ejecutar SQL con la consulta 9.2 y su resultado (6 filas) -->

**Resultado:** seis consumos por un total de $ 2.396.100. La placa SMB del robot de soldadura ($ 1.850.000) explica el 77 % del gasto, y su stock quedó en cero (consulta 7.2): conviene reponerla antes de una nueva falla del robot.
