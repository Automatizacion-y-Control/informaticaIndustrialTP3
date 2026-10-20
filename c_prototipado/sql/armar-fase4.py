"""Arma c_prototipado/fase4-explotacion.md tomando el código de fase4-consultas.sql.

El texto del informe está en este script: los cambios de redacción de la Fase IV se hacen acá
y se regenera con: python armar-fase4.py

Las capturas están en assets/ (paso7_01 a paso9_02), tomadas en DB Browser for SQLite.
"""
import re
from pathlib import Path

P = Path(__file__).resolve().parent.parent
sql = (P / 'sql/fase4-consultas.sql').read_text(encoding='utf-8')


def secciones(texto):
    """Divide un script en bloques separados por encabezados '-- ----' (título en la línea siguiente)."""
    partes = re.split(r'\n(?=-- -{10,}\n-- [^\n]+\n(?:-- [^\n]+\n)*-- -{10,}\n)', texto)
    return [p.strip('\n') for p in partes]


q = secciones(sql)  # 0: encabezado, 1..3 Paso 7, 4..5 Paso 8, 6..7 Paso 9
assert len(q) == 8, len(q)


def bloque(s):
    return f'```sql\n{s}\n```\n'


md = f"""# Fase IV — Explotación de datos y reportes industriales (La Consulta)

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

Aunque se escribe en ese orden, el motor la evalúa en otro: primero `FROM`, después `WHERE`, luego `SELECT` y al final `ORDER BY`. Por eso, en SQL estándar, un alias definido en el `SELECT` se puede usar en el `ORDER BY` pero no en el `WHERE`. SQLite lo acepta también en el `WHERE` como extensión propia, pero no es portable a otros motores y en este trabajo no se usa.

La condición del `WHERE` se arma con operadores de comparación y operadores lógicos:

| Operador | Significado | Uso en las consultas |
|---|---|---|
| `=`, `<>`, `<`, `<=`, `>`, `>=` | Comparación | `stock_actual <= stock_minimo` |
| `AND` | Se cumplen las dos condiciones | Rango de fechas y severidad |
| `OR` | Se cumple al menos una | `severidad IN ('ALTA', 'MEDIA')` equivale a `severidad = 'ALTA' OR severidad = 'MEDIA'` |
| `NOT` | Niega la condición | `NOT estado = 'CERRADA'` |
| `BETWEEN a AND b` | Rango, con los dos extremos incluidos | Fechas de las fallas |
| `IN (…)` | El valor está en la lista | `severidad IN ('ALTA', 'MEDIA')` |

Las fechas se guardaron como texto en formato ISO 8601 (`AAAA-MM-DD HH:MM:SS`). En ese formato el orden alfabético coincide con el cronológico, de modo que `BETWEEN` y `ORDER BY` funcionan sobre las fechas sin necesidad de convertirlas.

### Procedimiento

1. Se abrió `gmao.db` en DB Browser for SQLite y se pasó a la pestaña **Ejecutar SQL**.
2. Se escribió cada consulta sola en el editor y se ejecutó con **Ejecutar todo** (`F5`). Si hay texto seleccionado, DB Browser ejecuta solo la selección.
3. Se revisó el resultado en la grilla inferior y la cantidad de filas en el panel de mensajes.
4. Como las consultas solo leen, no hubo cambios que guardar.

### Consulta 7.1 — Fallas entre dos fechas

**Necesidad:** el supervisor revisa las fallas importantes de un período, por ejemplo para la reunión mensual de mantenimiento. Se combinan `BETWEEN` para el rango de fechas, `IN` para la severidad y `AND` para exigir las dos condiciones.

{bloque(q[1])}
![Consulta 7.1 en Ejecutar SQL: 5 fallas de severidad ALTA o MEDIA entre el 15/09 y el 10/10](./assets/paso7_01.png)

**Resultado:** cinco fallas entre el 15/09 y el 10/10. Por fecha quedan afuera las fallas del 02/09, 05/09, 10/09 y 15/10; la de la inyectora (12/10) queda afuera por la fecha y por su severidad baja.

### Consulta 7.2 — Repuestos con stock crítico

**Necesidad:** el pañol tiene que saber qué repuestos reponer antes de que una falla deje una máquina parada esperando una pieza. Un repuesto está en estado crítico cuando su stock llega al mínimo (punto de reposición). La columna calculada `faltante` ordena la lista por urgencia.

{bloque(q[2])}
![Consulta 7.2 en Ejecutar SQL: 4 repuestos en el stock mínimo o por debajo](./assets/paso7_02.png)

**Resultado:** cuatro repuestos. El filtro del compresor (faltan 2) y la placa SMB del robot (stock 0) están por debajo del mínimo; la correa del torno y el kit de sellos de la prensa están justo en el mínimo.

### Consulta 7.3 — Órdenes correctivas abiertas

**Necesidad:** las correctivas abiertas son máquinas con una falla sin resolver; el supervisor las sigue a diario. Se usa `NOT` para excluir las cerradas, lo que equivale a `estado IN ('PENDIENTE', 'EN CURSO')`.

{bloque(q[3])}
![Consulta 7.3 en Ejecutar SQL: 2 órdenes correctivas abiertas](./assets/paso7_03.png)

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

Con `GROUP BY` el cálculo se hace por grupos: las filas que comparten el valor de la columna indicada forman un grupo y cada grupo da una fila del resultado. En el `SELECT` solo deberían ir las columnas del `GROUP BY` y funciones de agregación, como exige el SQL estándar. SQLite acepta otras columnas sin dar error, pero devuelve el valor de una fila cualquiera del grupo, así que el resultado no es confiable. Si hace falta filtrar grupos (por ejemplo, máquinas con más de dos fallas) se usa `HAVING`, porque `WHERE` filtra filas antes de agrupar.

Las funciones de agregación **ignoran los `NULL`**, salvo `COUNT(*)`, que cuenta filas. Esto importa en las horas-hombre: las órdenes pendientes todavía no tienen horas cargadas, cuentan como órdenes pero no entran en la suma ni en el promedio.

### Procedimiento

Se siguió el mismo procedimiento que en el Paso 7: cada consulta se ejecutó sola en la pestaña **Ejecutar SQL** y se revisó la grilla de resultados. En las capturas se ensancharon las columnas de texto para que se lean completas.

### Consulta 8.1 — Fallas por máquina (activo más crítico)

**Necesidad:** identificar el activo que más falla para priorizar su mantenimiento y revisar su plan preventivo. Se cuentan las fallas de cada máquina y se suman sus horas de parada, que son las que miden el impacto en la producción.

{bloque(q[4])}
![Consulta 8.1 en Ejecutar SQL: fallas y horas de parada por máquina](./assets/paso8_01.png)

**Resultado:** la máquina 1, el torno CNC, es el activo más crítico: 3 fallas y 10,5 horas de parada, todas mecánicas en el husillo. Le siguen la prensa hidráulica (máquina 5) y el robot de soldadura (máquina 4), con 2 fallas cada uno; la prensa queda primero por tener más horas de parada (6 contra 5). El resultado muestra el identificador de la máquina: en el Paso 9 se resuelve el nombre con un `JOIN`.

### Consulta 8.2 — Horas-hombre por tipo de mantenimiento

**Necesidad:** comparar el esfuerzo dedicado al mantenimiento correctivo y al preventivo. Una planta con mucho correctivo trabaja apagando incendios; el objetivo es desplazar horas hacia el preventivo.

{bloque(q[5])}
![Consulta 8.2 en Ejecutar SQL: órdenes y horas-hombre por tipo de mantenimiento](./assets/paso8_02.png)

**Resultado:** el correctivo concentra 8 órdenes y 23,25 horas-hombre, el 77,5 % de las 30 horas registradas; el preventivo, 5 órdenes y 6,75 horas. El promedio por orden correctiva (3,32 h) es casi el doble del de la preventiva (1,69 h). Los promedios se calculan sobre las órdenes con horas cargadas: 7 de las 8 correctivas y 4 de las 5 preventivas, porque las dos pendientes tienen `horas_hombre` en `NULL`.

## Paso 9 — Consultas de integración de tablas (JOINs)

### Justificación teórica

En un modelo normalizado cada dato está en una sola tabla y las demás lo referencian por su clave. Una orden de trabajo guarda `id_maquina = 1`, no el texto «Torno CNC». Para mostrar la información completa hay que **reunir** las tablas siguiendo las relaciones PK–FK del DER, con `JOIN … ON`:

- `INNER JOIN` devuelve solo las filas que tienen pareja en las dos tablas.
- `LEFT JOIN` devuelve todas las filas de la tabla de la izquierda; si no tienen pareja, las columnas de la derecha quedan en `NULL`.

Los **alias** de tabla (`ordenes_trabajo AS ot`) acortan el código e indican de qué tabla sale cada columna cuando dos tablas tienen columnas con el mismo nombre, como `id_maquina`. El operador `||` concatena texto; si alguno de sus operandos es `NULL`, el resultado completo es `NULL`. `COALESCE(a, b)` devuelve el primer valor que no sea `NULL`.

### Procedimiento

Se siguió el mismo procedimiento que en los Pasos 7 y 8. Antes de escribir cada consulta se tomó del DER el camino de claves entre las tablas a cruzar.

### Consulta 9.1 — Órdenes con máquina, falla y técnico

**Necesidad:** el listado de órdenes que lee el personal de planta, con el nombre de la máquina, el motivo de la orden y el técnico asignado en lugar de los identificadores.

Máquina y técnico son obligatorios en toda orden, por eso se unen con `INNER JOIN`. La falla y el plan, en cambio, dependen del tipo de orden: la correctiva tiene falla y no tiene plan, y la preventiva al revés. Con `INNER JOIN fallas` desaparecerían las 5 órdenes preventivas; con `LEFT JOIN` se conservan todas y `COALESCE` muestra, en una sola columna, la descripción de la falla o la tarea del plan.

{bloque(q[6])}
![Consulta 9.1 en Ejecutar SQL: 14 filas con máquina, motivo y técnico de cada orden](./assets/paso9_01.png)

**Resultado:** 14 filas para las 13 órdenes, porque la OT-2026-0107 atiende dos fallas de la prensa hidráulica (pérdida de presión y fuga en el sello) y aparece una vez por cada una. La falla pendiente de la inyectora no figura porque todavía no tiene orden: la consulta parte de las órdenes.

### Consulta 9.2 — Repuestos consumidos por orden de trabajo

**Necesidad:** conocer el costo en repuestos de cada intervención, para imputarlo a la máquina y controlar el gasto de mantenimiento. La consulta parte de la tabla intermedia `ot_repuestos`, que resuelve la relación N:M, y la une con la orden, la máquina y el repuesto. El costo de cada consumo se calcula como cantidad por costo unitario.

{bloque(q[7])}
![Consulta 9.2 en Ejecutar SQL: repuestos consumidos por orden, con máquina y costo](./assets/paso9_02.png)

**Resultado:** seis consumos por un total de $ 2.396.100. La placa SMB del robot de soldadura ($ 1.850.000) explica el 77 % del gasto, y su stock quedó en cero (consulta 7.2): conviene reponerla antes de una nueva falla del robot.
"""
(P / 'fase4-explotacion.md').write_text(md, encoding='utf-8')
print('ok', len(md))
