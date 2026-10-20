# TP Nº 3 — Base de datos relacional para GMAO

Trabajo Práctico Nº 3 de **Informática Industrial** (UTN — Facultad Regional Córdoba, Licenciatura en Automatización y Control): diseño, implementación y consulta de una base de datos relacional en **SQLite** para un sistema de **Gestión de Mantenimiento Industrial (GMAO)**. Máquinas, fallas, planes preventivos, órdenes de trabajo, técnicos y repuestos.

| | |
|---|---|
| **Grupo Nº 4** | Casali, Emiliano · Del Soto, Gustavo · Ferrero, Facundo · Vera, Gonzalo |
| **Docente** | Ing. Carolina Rivarola |
| **Entrega** | Miércoles 28 de octubre de 2026, 23:59 hs (sin prórroga) |
| **Enunciado** | [`a_requisitos/TRABAJO PRACTICO NRO 3 - BASE DE DATOS.pdf`](a_requisitos/TRABAJO%20PRACTICO%20NRO%203%20-%20BASE%20DE%20DATOS.pdf) |

## Entregables

| Entregable | Archivo | Qué contiene |
|---|---|---|
| Informe técnico | [`d_presentacion/tp3-gmao-informe.pdf`](d_presentacion/tp3-gmao-informe.pdf) | Pasos 1 a 9 en el orden del enunciado, con el SQL en texto plano y las capturas. |
| Script SQL de respaldo | [`d_presentacion/tp3-gmao.sql`](d_presentacion/tp3-gmao.sql) | Todo el SQL en orden: creación (DDL), carga (DML) y consultas. |

## Estado

| Fase | Pasos | Texto | Capturas |
|---|---|---|---|
| I — Investigación | 1. Bases de datos y usos industriales · 2. Motor y requerimientos | ✅ | ✅ (4) |
| II — Planificación | 3. Entidades y atributos · 4. Modelo relacional (DER) | ✅ | — (el DER es un diagrama) |
| III — Construcción | 5. `CREATE TABLE` · 6. `INSERT INTO` | ✅ | ✅ (11) |
| IV — Consulta | 7. Filtrado · 8. Agrupaciones · 9. `JOIN` | ✅ | ⏳ faltan 7 |

Pendiente para cerrar la entrega:

- [ ] Capturas de la Fase IV: `paso7_01` a `paso7_03`, `paso8_01`, `paso8_02`, `paso9_01` y `paso9_02`.
- [ ] Sumar las consultas al `.sql` de respaldo (`python c_prototipado/sql/verificar.py --armar`).
- [ ] Regenerar el PDF y revisar todas las páginas.
- [ ] Revisión del grupo del Paso 1 («con sus propias palabras») y control final con [`a_requisitos/criterios-aceptacion.md`](a_requisitos/criterios-aceptacion.md).

El detalle de cada avance y de cada decisión está en la [bitácora](c_prototipado/bitacora.md).

## El modelo

Siete tablas en tercera forma normal. Como en los gestores de mantenimiento reales (SAP PM, Odoo, Maximo), el **correctivo** nace de una falla y el **preventivo**, de un plan. Los dos terminan en una orden de trabajo:

```
maquinas ──< fallas ─────────────>── ordenes_trabajo ──< ot_repuestos >── repuestos
maquinas ──< planes_preventivos ──<  ordenes_trabajo >── tecnicos
```

- Una falla puede quedar **pendiente** (sin orden) y una orden correctiva puede atender **varias fallas**.
- Las reglas de origen las controla la propia base: un `CHECK` exige que la preventiva tenga plan y la correctiva no, y *triggers* exigen que coincidan la máquina de la orden, la de su plan y la de sus fallas.
- Diagrama completo: [`c_prototipado/assets/fase2-planificacion_01.svg`](c_prototipado/assets/fase2-planificacion_01.svg).

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| [`a_requisitos/`](a_requisitos/) | Enunciado, requisitos de cada fase, criterios de aceptación y diseño de la portada. |
| [`b_investigacion/`](b_investigacion/) | Fichas de investigación y fuentes (Pasos 1 y 2, y relevamiento de gestores de mantenimiento reales). |
| [`c_prototipado/`](c_prototipado/) | Fuentes del informe y de la base: partes en Markdown, scripts SQL, capturas, base de trabajo y bitácora. |
| [`d_presentacion/`](d_presentacion/) | Los dos entregables. |

Dentro de `c_prototipado/`:

| Archivo | Para qué |
|---|---|
| `fase1-investigacion.md` … `fase4-explotacion.md`, `referencias.md` | Partes del informe, en el orden que fija `diseño.md`. |
| `diseño.md` | Configuración del PDF (partes, portada, índice). |
| `sql/paso5-ddl.sql` | Creación de las 7 tablas y los 4 *triggers*. |
| `sql/paso6-dml.sql` | Carga de datos simulados de planta (53 registros). |
| `sql/fase4-consultas.sql` | Las 7 consultas de los Pasos 7, 8 y 9. |
| `gmao.db` | Base de trabajo, creada en DB Browser con los scripts anteriores. |
| `assets/` | Capturas de DB Browser y diagrama entidad-relación. |
| `bitacora.md` | Registro de avances y decisiones. |

## Herramientas

- **DB Browser for SQLite 3.13.1** (trae SQLite 3.46.1). Instalación en Windows: `winget install --id DBBrowserForSQLite.DBBrowserForSQLite -e`.
- **Python 3**, solo para los scripts de verificación y de armado del informe (no necesita paquetes adicionales).

## Cómo trabajar con la base

1. Abrir `c_prototipado/gmao.db` en DB Browser (**Abrir base de datos**).
2. Para recrearla desde cero, en la pestaña **Ejecutar SQL** ejecutar `sql/paso5-ddl.sql` y después `sql/paso6-dml.sql` (`F5`), y **Guardar cambios** (`Ctrl+S`). El DDL borra y vuelve a crear las tablas, así que se puede repetir.
3. Las consultas de la Fase IV están en `sql/fase4-consultas.sql`. Para ver el resultado de una, se selecciona y se ejecuta con `Ctrl+Retorno`.

## Scripts auxiliares

Todos se ejecutan desde `c_prototipado/` o `c_prototipado/sql/`.

| Comando | Qué hace | ¿Modifica archivos? |
|---|---|---|
| `python sql/verificar.py` | Ejecuta los scripts sobre una base vacía en una carpeta temporal y comprueba varias cosas: registros por tabla, 15 casos inválidos rechazados, consultas con resultado, SQL del informe idéntico al de los scripts y si el `.sql` entregable está al día. | No. Trabaja sobre copias y borra la carpeta temporal |
| `python sql/verificar.py --armar` | Lo anterior y, además, actualiza `d_presentacion/tp3-gmao.sql`. | Sí, el `.sql` entregable |
| `python sql/armar-fase3.py` / `armar-fase4.py` | Regenera `fase3-construccion.md` / `fase4-explotacion.md` con el SQL de los scripts. La redacción de esas fases se edita en estos scripts. | Sí, el `.md` de la fase |
| `python generar-der.py assets/fase2-planificacion_01.svg` | Regenera el diagrama entidad-relación. | Sí, el `.svg` |
| `python prueba-modelo.py` | Prueba del modelo de la Fase II, en memoria. | No |

## Cómo regenerar el PDF

El PDF se arma a partir de `c_prototipado/` con la skill `documento-pdf` de Claude Code. Queda en `d_presentacion/tp3-gmao-informe.pdf` y reemplaza la versión anterior.

## Acuerdos de trabajo

- Ningún archivo del proyecto se borra ni se regenera sin acuerdo del grupo, en especial `gmao.db` y los entregables.
- Las capturas se toman en DB Browser, con la interfaz en español, y se guardan en `c_prototipado/assets/` con el nombre `pasoN_NN.png`.
- Tablas y columnas en `snake_case`, sin tildes. Redacción del informe en forma impersonal.
- Cada cambio relevante se anota en la [bitácora](c_prototipado/bitacora.md).
