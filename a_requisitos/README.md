# Requisitos — TP Nº 3: Base de Datos relacional para GMAO

Requisitos del Trabajo Práctico Nº 3 de Informática Industrial, tomados del enunciado [`TRABAJO PRACTICO NRO 3 - BASE DE DATOS.pdf`](../TRABAJO%20PRACTICO%20NRO%203%20-%20BASE%20DE%20DATOS.pdf) y de las decisiones acordadas. Lo marcado como **[A CONFIRMAR]** en los archivos es una propuesta pendiente de aprobación.

Última actualización: 2026-10-19.

## Datos del trabajo

| Campo | Valor |
|---|---|
| Institución | Universidad Tecnológica Nacional — Facultad Regional Córdoba |
| Carrera | Licenciatura en Automatización y Control |
| Asignatura | Informática Industrial |
| Trabajo | Diseño, implementación y consulta de bases de datos relacionales en entornos industriales |
| Escenario elegido | **Gestión de Mantenimiento Industrial (GMAO)** |
| Motor elegido | **SQLite**, con **DB Browser for SQLite** |
| Fecha límite | **Miércoles 28 de octubre de 2026, 23:59 hs.** Sin entregas fuera de término. |
| Grupo | **Nº 4**: Casali, Emiliano · Del Soto, Gustavo · Ferrero, Facundo · Vera, Gonzalo |
| Docente | Ing. Carolina Rivarola |

## Archivos

| Archivo | Contenido |
|---|---|
| [`requisitos-generales.md`](requisitos-generales.md) | Propósito, audiencia, alcance, idioma, origen y restricciones del informe. |
| [`fase1-investigacion.md`](fase1-investigacion.md) | Fase I — Pasos 1 y 2: conceptos de BD y entorno RDBMS. |
| [`fase2-planificacion.md`](fase2-planificacion.md) | Fase II — Pasos 3 y 4: entidades, atributos, tipos de datos y DER. |
| [`fase3-construccion.md`](fase3-construccion.md) | Fase III — Pasos 5 y 6: `CREATE TABLE` e `INSERT INTO`. |
| [`fase4-explotacion.md`](fase4-explotacion.md) | Fase IV — Pasos 7, 8 y 9: filtrado, agrupaciones y JOINs. |
| [`criterios-aceptacion.md`](criterios-aceptacion.md) | Check-list completo del enunciado y criterios del PDF. |
| [`diseno-utn.md`](diseno-utn.md) | Diseño base académico del PDF: datos de la portada, paleta y tipografía. |

## Entregables

| # | Entregable | Contenido | Ubicación |
|---|---|---|---|
| 1 | Informe técnico (PDF) | Estructura exacta de los Pasos 1 a 9, código SQL en texto plano y capturas de las consultas con sus resultados. | `d_presentacion/tp3-gmao-informe.pdf` |
| 2 | Script SQL de respaldo | Un único `.sql` con todo el código en orden: creación, inserción y consultas. | `d_presentacion/tp3-gmao.sql` |
| — | Base de trabajo (`.db`) | Archivo SQLite donde se ejecuta todo y se sacan las capturas. No se entrega salvo que se pida. | `c_prototipado/` |

## Plan de partes

Se trabaja una fase por vez y no se avanza sin validar la anterior. La **parte de muestra** (para validar el diseño del PDF) es la Fase II, por decisión del grupo del 2026-10-19.

| # | Parte | Contenido | Estado |
|---|---|---|---|
| 1 | Portada (automática, desde `diseno-utn.md`) | Universidad, carrera, asignatura, TP Nº 3 — Grupo Nº 4, título, docente/s, integrantes, lugar y fecha. | Lista |
| 2 | `fase1-investigacion.md` | Pasos 1 y 2. | Redactada, con capturas; falta revisión del grupo |
| 3 | `fase2-planificacion.md` | Pasos 3 y 4. **Parte de muestra.** | Modelo de 7 tablas verificado; en revisión del grupo |
| 4 | `fase3-construccion.md` | Pasos 5 y 6. | Scripts verificados, con capturas |
| 5 | `fase4-explotacion.md` | Pasos 7, 8 y 9. | Redactada y verificada (7 consultas); faltan capturas `paso7_01` a `paso9_02` |
| 6 | `referencias.md` | Fuentes citadas. | Lista (16 fuentes) |
| — | `tp3-gmao.sql` | Script de respaldo; lo arma `c_prototipado/sql/verificar.py`. | DDL, DML y consultas listos; falta `verificar.py --armar` con OK del grupo |

## Decisiones tomadas (2026-10-19)

Aceptadas por el grupo: redacción impersonal formal; tablas y columnas en `snake_case` sin tildes; PDF y `.sql` en `d_presentacion/`; DER como SVG (`c_prototipado/generar-der.py`) más captura de DB Browser; consultas propuestas para los Pasos 7, 8 y 9; Fase I como parte de muestra; portada sin logo.

Modelo GMAO: el correctivo nace de la falla y el preventivo de un plan preventivo; la falla apunta a la OT (como el aviso en SAP PM); reglas de origen con `CHECK` y *triggers*. Además: docente Ing. Carolina Rivarola; se trabaja con repositorio git, que se inicializa cuando el grupo lo indique.

## Pendientes a confirmar

Ninguno.
