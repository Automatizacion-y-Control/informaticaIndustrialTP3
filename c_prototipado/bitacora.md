# Bitácora: Informe TP Nº 3 — GMAO

Registro del desarrollo: cada parte cerrada, las decisiones tomadas con el grupo y los cambios de diseño. Lo más nuevo, abajo.

## 2026-10-19 — Inicio

- Escenario: Gestión de Mantenimiento Industrial (GMAO). Motor: SQLite con DB Browser for SQLite.
- Requisitos registrados en `a_requisitos/` y aceptados por el grupo.
- Grupo Nº 4: Casali, Emiliano; Del Soto, Gustavo; Ferrero, Facundo; Vera, Gonzalo.
- Estructura por fases creada. Diseño base académico (`a_requisitos/diseno-utn.md`) con portada de la cátedra.
- Investigación de los Pasos 1 y 2 iniciada en `b_investigacion/`.
- Docente: Ing. Carolina Rivarola. Git: se inicializa cuando el grupo lo indique.

## 2026-10-19 — Fase II (parte de muestra)

- El grupo decidió empezar por la Fase II; queda como parte de muestra para validar el diseño del PDF.
- Modelo: 6 tablas (`maquinas`, `tecnicos`, `fallas`, `ordenes_trabajo`, `repuestos`, `ot_repuestos`), en 3FN; N:M entre órdenes y repuestos resuelta con `ot_repuestos`.
- DER: el diagrama Mermaid salía ilegible en A4; se reemplazó por un SVG generado con `generar-der.py` (grilla 3×2, notación pata de gallo). Para regenerarlo: `python generar-der.py assets/fase2-planificacion_01.svg`.
- Epígrafes de tablas: cada tabla tiene su propio título `###` para que el epígrafe la nombre.
- Pendiente: validación del grupo; captura de la vista *Estructura de la base de datos* de DB Browser después del Paso 5.

## 2026-10-19 — Fase II: revisión del modelo

- Observación del grupo: la OT preventiva no nace de una falla sino del área de mantenimiento preventivo.
- Se relevaron SAP PM, Odoo e IBM Maximo (`b_investigacion/gmao-sistemas-reales.md`). Los tres separan el origen correctivo (aviso o falla) del preventivo (plan con frecuencia por tiempo o contador).
- Cambios: tabla nueva `planes_preventivos`; `ordenes_trabajo.id_falla` se reemplaza por `ordenes_trabajo.id_plan`; `fallas` gana `id_ot`, de modo que una OT puede agrupar varias fallas y una falla puede quedar pendiente (como el aviso de SAP). Modelo de 7 tablas.
- Reglas: `CHECK` de origen según el tipo de OT; *triggers* para la misma máquina entre OT y plan y para que una falla solo se asigne a una OT correctiva de la misma máquina.
- Verificación: `prueba-modelo.py` acepta 11 de 11 casos válidos y rechaza 9 de 9 inválidos.
- DER regenerado con 7 tablas; la leyenda va antes de la figura y el diagrama va antes de las reglas, para que el título, la leyenda y la figura queden en la misma página.

## 2026-10-19 — Fase III (Pasos 5 y 6)

- Scripts en `c_prototipado/sql/`: `paso5-ddl.sql` (7 `CREATE TABLE`, `PRAGMA foreign_keys`, `DROP TABLE IF EXISTS` para poder reejecutar y 4 *triggers*) y `paso6-dml.sql` (53 registros, con 5 o más por tabla).
- Se agregó `CHECK (>= 0)` al stock actual y al mínimo de `repuestos`.
- `verificar.py`: ejecuta los dos scripts sobre una base vacía de prueba (`c_prototipado/sql/verificacion.db`), cuenta los registros, prueba 15 casos inválidos (todos rechazados), comprueba que el SQL del informe sea idéntico al de los scripts y arma `d_presentacion/tp3-gmao.sql`.
- `fase3-construccion.md` se genera con `sql/armar-fase3.py`, que toma el código de los scripts. Los cambios de redacción de la Fase III se hacen en ese script.
- Formato: líneas de SQL de 80 caracteres como máximo, para que no se corten en el PDF.
- Capturas pendientes (las toma el grupo en DB Browser y se guardan en `c_prototipado/assets/`), marcadas en el informe con comentarios `CAPTURA`:
  - `paso5_01`: Ejecutar SQL con el DDL ejecutado sin errores.
  - `paso5_02`: Estructura de la base de datos con las 7 tablas y los 4 *triggers*.
  - `paso6_01`: Ejecutar SQL con el DML ejecutado sin errores.
  - `paso6_02` a `paso6_08`: Hojear datos de cada tabla.
  - `paso6_09` (opcional): mensaje de error al intentar cargar una OT preventiva sin plan.

## 2026-10-19 — Error al abrir la base en VS Code

- La extensión SQLite (alexcvzz 0.14.1) falla al abrir cualquier base con `no such column: "table"`. Usa el `sqlite3` del sistema (3.53.4), que desde la 3.41 no acepta comillas dobles como texto. No es un problema de la base: `integrity_check` da `ok`.
- Se usa DB Browser for SQLite (o la extensión Database Client).
- `verificar.py` pasa a usar `sql/verificacion.db`, para no borrar el `gmao.db` que el grupo crea en DB Browser.

## 2026-10-19 — DB Browser y Fase I (Pasos 1 y 2)

- DB Browser for SQLite 3.13.1 instalado con `winget install --id DBBrowserForSQLite.DBBrowserForSQLite -e` (`.msi` de 64 bits, en `C:\Program Files\DB Browser for SQLite\`, 47 MB). Trae SQLite 3.46.1.
- Equipo del trabajo: Windows 11 Pro de 64 bits (10.0.26200), AMD Ryzen 5 5500, 16 GB de RAM.
- `fase1-investigacion.md`: Paso 1 (definición, clasificación con tabla comparativa, diagrama ISA-95 y 3 usos: ERP–MES, recetas ISA-88 y GMAO) y Paso 2 (SQLite, DB Browser, requisitos con los datos del equipo y método de acceso local).
- `referencias.md`: 16 fuentes, con la misma numeración que `b_investigacion/README.md`.
- `diseño.md`: se agregan `fase1-investigacion.md` al principio y `referencias.md` al final.
- Pendiente: revisión del Paso 1 por el grupo («con sus propias palabras») y capturas `paso2_01` a `paso2_04`.
- `gmao.db` se volvió a crear con `d_presentacion/tp3-gmao.sql` después de haberse borrado sin consultar. Desde ahora no se borra ni se regenera ningún archivo del proyecto sin OK del grupo.
- `verificar.py` trabaja sobre copias en una carpeta temporal que borra al terminar; no modifica el proyecto. El entregable `.sql` solo se reemplaza con `--armar`.

## 2026-10-19 — Capturas de las Fases I y III

- Las 15 capturas se tomaron en DB Browser for SQLite 3.13.1 sobre el equipo del trabajo y se guardaron en `assets/` como PNG: `paso2_01` a `paso2_04`, `paso5_01`, `paso5_02` y `paso6_01` a `paso6_09`.
- Interfaz de DB Browser en español (Preferencias → General → Idioma) y fuentes en 11-12 pt, para que las capturas se lean en A4. Se ocultaron los paneles laterales (Editar celda, Remoto, etc.).
- Para tomar las capturas del procedimiento real, `gmao.db` se volvió a crear con **Nueva base de datos** y se ejecutaron `sql/paso5-ddl.sql` y `sql/paso6-dml.sql`. Antes se comprobó que la base anterior fuera idéntica a la que generan los scripts. Después se volvió a comparar: mismos datos y mismo esquema (solo cambian los saltos de línea de Windows en el texto del esquema); `integrity_check` = `ok`.
- `paso6_09`: el `INSERT` de la OT preventiva sin plan fue rechazado con `CHECK constraint failed` y no dejó cambios pendientes.
- Los comentarios `CAPTURA` de `fase1-investigacion.md` y `fase3-construccion.md` (y de `sql/armar-fase3.py`) se reemplazaron por las imágenes. Se comprobó que `armar-fase3.py` regenera el mismo `fase3-construccion.md`.
- Los nombres de la interfaz se ajustaron a los de la versión en español que se ve en las capturas: **Hojear datos** → **Hoja de datos**, **Escribir cambios** → **Guardar cambios**, **Estructura de la base de datos** → **Estructura**.
- Pendiente: regenerar el PDF con la skill `documento-pdf` y revisar que las capturas se lean bien al tamaño impreso.

## 2026-10-19 — Fase IV (Pasos 7, 8 y 9)

- `sql/fase4-consultas.sql`: 7 consultas. Paso 7: fallas entre dos fechas (`BETWEEN`, `IN`, `AND`), repuestos con stock crítico (columna calculada `faltante`) y correctivas abiertas (`NOT`). Paso 8: fallas y horas de parada por máquina, y horas-hombre por tipo de OT (`COUNT`, `SUM`, `AVG`, `MAX`). Paso 9: órdenes con máquina, motivo y técnico (`INNER JOIN` + `LEFT JOIN` a fallas y planes con `COALESCE`) y repuestos por OT con costo (4 tablas).
- Resultados sobre `gmao.db` (solo lectura): 5, 4, 2, 6, 2, 14 y 6 filas. Ninguna vacía.
- `fase4-explotacion.md` se genera con `sql/armar-fase4.py`, igual que la Fase III. Cada consulta lleva necesidad, SQL, captura y lectura del resultado.
- Sin `;` en los comentarios del script de consultas, para poder separarlo por sentencias.
- `verificar.py`: ejecuta las consultas, controla que ninguna dé vacío y compara el SQL de `fase4-explotacion.md` con el script.
- `diseño.md`: se agregó `fase4-explotacion.md` a `fuentes`.
- Capturas pendientes (Ejecutar SQL, consulta seleccionada + grilla de resultados), marcadas con comentarios `CAPTURA`: `paso7_01`, `paso7_02`, `paso7_03`, `paso8_01`, `paso8_02`, `paso9_01`, `paso9_02`.
- Pendiente con OK del grupo: `python verificar.py --armar` para sumar las consultas a `d_presentacion/tp3-gmao.sql`, y regenerar el PDF.
