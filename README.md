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
| IV — Consulta | 7. Filtrado · 8. Agrupaciones · 9. `JOIN` | ✅ | ✅ (7) |

Los dos entregables están completos y verificados: el informe tiene 48 páginas, con introducción y las 22 capturas, y el `.sql` contiene creación, carga y consultas. El control final contra el enunciado está en [`a_requisitos/criterios-aceptacion.md`](a_requisitos/criterios-aceptacion.md).

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
| [`a_requisitos/`](a_requisitos/) | Enunciado, caso de estudio (la planta), requisitos de cada fase, criterios de aceptación. |
| [`b_investigacion/`](b_investigacion/) | Fichas de investigación y fuentes (Pasos 1 y 2, y relevamiento de gestores de mantenimiento reales). |
| [`c_prototipado/`](c_prototipado/) | Desarrollo del TP: informe por fases, scripts SQL, capturas, diagrama y base de datos. |
| [`d_presentacion/`](d_presentacion/) | Los dos entregables. |

## Herramientas

- **DB Browser for SQLite 3.13.1** (trae SQLite 3.46.1). Instalación en Windows: `winget install --id DBBrowserForSQLite.DBBrowserForSQLite -e`.
- **Python 3**, opcional para ejecutar las verificaciones de la base con la biblioteca estándar `sqlite3`.

## Cómo trabajar con la base

1. Abrir `c_prototipado/gmao.db` en DB Browser (**Abrir base de datos**).
2. Para recrearla desde cero, en la pestaña **Ejecutar SQL** ejecutar `c_prototipado/sql/paso5-ddl.sql` y después `c_prototipado/sql/paso6-dml.sql` (`F5`), y **Guardar cambios** (`Ctrl+S`). El DDL borra y vuelve a crear las tablas, así que se puede repetir.
3. Las consultas de la Fase IV están en `c_prototipado/sql/fase4-consultas.sql`. Para ver el resultado de una, se selecciona y se ejecuta con `F5` (o `Ctrl+Retorno`): con texto seleccionado, DB Browser ejecuta solo la selección.

## Verificación de la base

Desde la raíz del repositorio:

```powershell
python c_prototipado/sql/verificar.py
```

El verificador ejecuta los scripts sobre una base temporal, comprueba al menos cinco registros por tabla, prueba restricciones de integridad y ejecuta las siete consultas. También controla la coincidencia del SQL con las fuentes del informe y con el script entregable.

La verificación del 26/10/2026 confirmó 53 registros en siete tablas, 15 casos inválidos rechazados y resultados en las siete consultas. La base guardada coincide con los datos del script entregable.

## Implementación básica

El grupo cuenta con una implementación básica complementaria en [gmao.24hs.click](https://gmao.24hs.click/). Los entregables académicos son el PDF y el script SQL de `d_presentacion/`.
