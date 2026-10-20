"""Arma c_prototipado/fase3-construccion.md tomando el código de paso5-ddl.sql y paso6-dml.sql.

El texto del informe está en este script: los cambios de redacción de la Fase III se hacen acá
y se regenera con: python armar-fase3.py
"""
import re
from pathlib import Path

P = Path(__file__).resolve().parent.parent
ddl = (P / 'sql/paso5-ddl.sql').read_text(encoding='utf-8')
dml = (P / 'sql/paso6-dml.sql').read_text(encoding='utf-8')


def secciones(sql):
    """Divide un script en bloques separados por encabezados '-- ----' (título en la línea siguiente)."""
    partes = re.split(r'\n(?=-- -{10,}\n-- [^\n]+\n(?:-- [^\n]+\n)*-- -{10,}\n)', sql)
    return [p.strip('\n') for p in partes]


d = secciones(ddl)  # 0: encabezado+PRAGMA+DROP, 1..7 tablas, 8 triggers
m = secciones(dml)  # 0: encabezado+PRAGMA, 1..7 inserts
assert len(d) == 9 and len(m) == 8, (len(d), len(m))


def bloque(s):
    return f'```sql\n{s}\n```\n'


md = f"""# Fase III — Implementación y carga de datos mediante SQL (La Construcción)

En esta fase el modelo de la Fase II se convierte en una base de datos real. Primero se escriben las sentencias de creación de tablas, con todas sus restricciones de integridad (Paso 5), y después se cargan datos simulados de planta (Paso 6). Los dos scripts se ejecutaron en DB Browser for SQLite sobre una base vacía, en ese orden, y se verificó que la base acepta los datos válidos y rechaza los inválidos.

## Paso 5 — Scripts de creación de tablas (DDL)

### Justificación teórica

SQL se divide en sublenguajes según su función. El **DDL** (*Data Definition Language*, lenguaje de definición de datos) crea, modifica y elimina la estructura de la base: tablas, índices y *triggers*. Su sentencia principal es `CREATE TABLE`, que define el nombre de la tabla, sus columnas con el tipo de dato y las **restricciones de integridad** que todo registro debe cumplir:

| Restricción | Qué garantiza | Ejemplo en el modelo |
|---|---|---|
| `PRIMARY KEY` | Cada fila se identifica de forma única y su clave no puede quedar vacía. | `id_maquina INTEGER PRIMARY KEY` |
| `FOREIGN KEY … REFERENCES` | El valor existe en la tabla referenciada (integridad referencial). | `FOREIGN KEY (id_maquina) REFERENCES maquinas (id_maquina)` |
| `NOT NULL` | El campo es obligatorio. | `nombre VARCHAR(60) NOT NULL` |
| `UNIQUE` | No se repite el valor en toda la tabla. | `codigo VARCHAR(10) NOT NULL UNIQUE` |
| `CHECK` | El valor cumple una condición. | `CHECK (estado IN ('PENDIENTE', 'EN CURSO', 'CERRADA'))` |

Un `CHECK` solo puede evaluar columnas de la misma fila. Las reglas que necesitan consultar otra tabla, como que una falla se asigne solo a una orden correctiva de la misma máquina, se implementan con **triggers**: bloques que SQLite ejecuta automáticamente antes de una inserción o una modificación y que, si la regla no se cumple, cancelan la operación con `RAISE(ABORT, 'mensaje')`.

En SQLite la verificación de claves foráneas viene **desactivada por defecto** y se activa en cada conexión con `PRAGMA foreign_keys = ON`. Por eso el script empieza con esa sentencia. A continuación borra las tablas si ya existían (`DROP TABLE IF EXISTS`), de modo que se puede volver a ejecutar desde cero. El borrado se hace en orden inverso a las dependencias: primero las tablas que referencian a otras.

Las tablas se crean en el orden contrario, empezando por las que no dependen de ninguna: `maquinas`, `tecnicos` y `repuestos`; después `planes_preventivos`, `ordenes_trabajo` y `fallas`; y al final la tabla intermedia `ot_repuestos`.

### Procedimiento

1. En DB Browser for SQLite se eligió **Nueva base de datos** y se guardó el archivo `gmao.db`. El asistente de creación de tablas se cerró sin usarlo, porque las tablas se crean por código.
2. En **Editar → Preferencias → Base de datos** se verificó que la opción de claves foráneas estuviera activada. De todas formas, el script incluye el `PRAGMA`.
3. En la pestaña **Ejecutar SQL** se cargó el script `paso5-ddl.sql` y se ejecutó completo con **Ejecutar todo** (`F5`).
4. Se revisó el panel de mensajes: la ejecución terminó sin errores.
5. Se confirmaron los cambios con **Guardar cambios** (`Ctrl+S`).
6. En la pestaña **Estructura** se comprobaron las 7 tablas, sus columnas y los 4 *triggers*.

![Ejecución de paso5-ddl.sql en la pestaña Ejecutar SQL, terminada sin errores](./assets/paso5_01.png)
![Pestaña Estructura: las 7 tablas (con las columnas de ordenes_trabajo desplegadas) y los 4 disparadores](./assets/paso5_02.png)

### Activación de claves foráneas y reinicio de la base

{bloque(d[0])}
### Tabla `maquinas`

{bloque(d[1])}
### Tabla `tecnicos`

{bloque(d[2])}
### Tabla `repuestos`

Además de lo definido en el Paso 3, el stock actual y el mínimo no pueden ser negativos.

{bloque(d[3])}
### Tabla `planes_preventivos`

{bloque(d[4])}
### Tabla `ordenes_trabajo`

El `CHECK` de tabla, al final de las columnas, exige que el origen de la orden corresponda a su tipo: la preventiva tiene plan y la correctiva no.

{bloque(d[5])}
### Tabla `fallas`

`id_ot` admite `NULL`: una falla puede registrarse antes de que se emita su orden de trabajo, y queda pendiente.

{bloque(d[6])}
### Tabla `ot_repuestos`

La clave primaria es compuesta y cada una de sus columnas es, además, clave foránea.

{bloque(d[7])}
### Reglas entre tablas (triggers)

Los cuatro *triggers* hacen cumplir las reglas del Paso 4 que un `CHECK` no puede verificar. Se controlan tanto las inserciones como las modificaciones, para que no se pueda dejar la base en un estado incoherente con un `UPDATE` posterior.

{bloque(d[8])}
## Paso 6 — Script de inserción de datos de planta (DML)

### Justificación teórica

El **DML** (*Data Manipulation Language*, lenguaje de manipulación de datos) opera sobre el contenido de las tablas: `INSERT` agrega registros, `UPDATE` los modifica, `DELETE` los elimina y `SELECT` los consulta. La sentencia `INSERT INTO tabla (columnas) VALUES (…), (…)` permite cargar varios registros en una sola instrucción. Nombrar las columnas de forma explícita hace que el script no dependa del orden en que fueron creadas.

El orden de carga respeta las claves foráneas: no se puede insertar una orden de trabajo de una máquina que todavía no existe. Por eso primero se cargan `maquinas`, `tecnicos` y `repuestos`, después `planes_preventivos`, luego `ordenes_trabajo`, después `fallas` (que referencian a su orden) y al final `ot_repuestos`.

Los valores ausentes se cargan como `NULL`: la fecha de cierre de una orden abierta, el plan de una orden correctiva o la orden de una falla pendiente. Las fechas se escriben en formato ISO 8601. Los cambios quedan en una transacción hasta que se confirman con **Guardar cambios**: si alguna sentencia falla, DB Browser no guarda nada a medias.

### Procedimiento

1. Sobre la base `gmao.db` creada en el Paso 5 se abrió la pestaña **Ejecutar SQL**.
2. Se cargó el script `paso6-dml.sql` y se ejecutó completo (`F5`).
3. Se revisó el panel de mensajes: todas las inserciones terminaron sin errores.
4. Se confirmaron los cambios con **Guardar cambios** (`Ctrl+S`).
5. En la pestaña **Hoja de datos** se revisó cada tabla.

### Datos cargados

Los datos son **simulados**, pero se eligieron para que representen una planta real y para que las consultas de la Fase IV devuelvan resultados significativos:

| Tabla | Registros | Qué permite analizar |
|---|---|---|
| `maquinas` | 6 | Equipos reales de distintos sectores y criticidades (Haas, Atlas Copco, ABB, Engel). |
| `tecnicos` | 5 | Especialidades y turnos distintos. |
| `repuestos` | 7 | Dos repuestos por debajo del stock mínimo (filtro del compresor y placa del robot). |
| `planes_preventivos` | 6 | Planes por calendario (días) y por horómetro (horas). |
| `ordenes_trabajo` | 13 | 8 correctivas y 5 preventivas, en los tres estados. |
| `fallas` | 10 | Fallas entre septiembre y octubre de 2026; el torno CNC es el activo con más fallas; dos fallas se atienden en una misma orden y una queda pendiente. |
| `ot_repuestos` | 6 | Consumo de repuestos en correctivas y preventivas. |

![Ejecución de paso6-dml.sql en la pestaña Ejecutar SQL, terminada sin errores](./assets/paso6_01.png)
![Pestaña Hoja de datos: tabla maquinas (6 registros)](./assets/paso6_02.png)

![Pestaña Hoja de datos: tabla tecnicos (5 registros)](./assets/paso6_03.png)

![Pestaña Hoja de datos: tabla repuestos (7 registros)](./assets/paso6_04.png)

![Pestaña Hoja de datos: tabla planes_preventivos (6 registros)](./assets/paso6_05.png)

![Pestaña Hoja de datos: tabla ordenes_trabajo (13 registros)](./assets/paso6_06.png)

![Pestaña Hoja de datos: tabla fallas (10 registros)](./assets/paso6_07.png)

![Pestaña Hoja de datos: tabla ot_repuestos (6 registros)](./assets/paso6_08.png)

### Activación de claves foráneas

{bloque(m[0])}
### Carga de `maquinas`

{bloque(m[1])}
### Carga de `tecnicos`

{bloque(m[2])}
### Carga de `repuestos`

{bloque(m[3])}
### Carga de `planes_preventivos`

{bloque(m[4])}
### Carga de `ordenes_trabajo`

{bloque(m[5])}
### Carga de `fallas`

{bloque(m[6])}
### Carga de `ot_repuestos`

{bloque(m[7])}
### Verificación de la integridad

Para comprobar que las restricciones funcionan se intentó cargar datos inválidos. Estas sentencias **no forman parte del script**: se ejecutaron aparte y la base las rechazó con el mensaje indicado.

| Intento | Mensaje de SQLite |
|---|---|
| OT preventiva sin plan | `CHECK constraint failed` |
| OT preventiva de otra máquina que su plan | `La OT preventiva debe ser de la misma maquina que su plan` |
| Falla asignada a una OT preventiva | `La falla solo se asigna a una OT correctiva de la misma maquina` |
| Falla de una máquina inexistente | `FOREIGN KEY constraint failed` |
| Número de OT repetido | `UNIQUE constraint failed: ordenes_trabajo.nro_ot` |
| Máquina sin nombre | `NOT NULL constraint failed: maquinas.nombre` |
| Borrar una máquina con historial | `FOREIGN KEY constraint failed` |

Por ejemplo, la primera prueba:

```sql
INSERT INTO ordenes_trabajo (id_ot, nro_ot, tipo, id_maquina, id_plan, id_tecnico, fecha_emision, estado, tarea)
VALUES (90, 'OT-2026-0190', 'PREVENTIVA', 1, NULL, 1, '2026-10-20 08:00:00', 'PENDIENTE', 'Prueba');
```

![DB Browser rechaza la OT preventiva sin plan: CHECK constraint failed](./assets/paso6_09.png)
"""
(P / 'fase3-construccion.md').write_text(md, encoding='utf-8')
print('ok', len(md))
