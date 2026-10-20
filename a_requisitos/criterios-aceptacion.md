# Criterios de aceptación

Lo que tienen que cumplir los entregables para considerarse terminados. Los criterios de cada fase están detallados en su archivo (`fase1-…` a `fase4-…`); acá va la lista completa para el control final.

## Del enunciado (check-list obligatorio)

| Fase | Paso | Tarea | Entregable evidente en el informe | ✓ |
|---|---|---|---|---|
| I. Investigación | 1 | Conceptos de BD | Texto explicativo e investigación de usos industriales. | [x] |
| I. Investigación | 2 | Entorno RDBMS | Definición del software a usar y sus requisitos de sistema. | [x] |
| II. Planificación | 3 | Entidades y datos | Tabla con la estructura de campos y tipos de datos elegidos. | [x] |
| II. Planificación | 4 | Diagrama DER | Imagen clara del modelo relacional (llaves PK/FK visibles). | [x] |
| III. Construcción | 5 | Tablas en SQL | Capturas y código de los `CREATE TABLE` ejecutados. | [x] |
| III. Construcción | 6 | Carga de datos | Capturas y código de los `INSERT INTO` con los datos cargados. | [x] |
| IV. Explotación | 7 | Consultas básicas | Código SQL de los `SELECT` con filtros y capturas de los resultados. | [x] |
| IV. Explotación | 8 | Agrupaciones | Código SQL con `GROUP BY` y estadísticas obtenidas. | [x] |
| IV. Explotación | 9 | Joins avanzados | Código SQL usando `INNER JOIN` para vincular datos relacionales. | [x] |

Además:

- [x] Cada paso tiene justificación teórica, descripción del procedimiento y capturas legibles.
- [x] El `.sql` es un único archivo con todo el código ordenado (creación, inserción y consultas) y se ejecuta sin errores sobre una base vacía.
- [ ] Entrega antes del **miércoles 28/10/2026 a las 23:59** (la sube el grupo).

## Del documento PDF

- [x] El código SQL aparece como texto seleccionable, en fuente monoespaciada.
- [x] Las capturas son legibles al tamaño impreso y cada una tiene número y epígrafe.
- [x] Las imágenes explican el contenido de su sección (nada decorativo).
- [x] El índice tiene las páginas reales.
- [x] El texto corrido está justificado, sin espacios grandes.
- [x] Los enlaces de las referencias están activos.
- [x] Ninguna fuente está incrustada como Type 3.

## Control final (2026-10-19)

- Informe: 48 páginas, introducción con el caso de estudio y Pasos 1 a 9 en el orden del enunciado, 25 figuras (22 capturas de DB Browser, el proceso productivo, el diagrama ISA-95 y el DER) y 18 tablas, numeradas sin saltos. Sin marcas de captura pendientes.
- Fuentes del PDF: todas Type0, ninguna Type 3. Enlaces externos activos: 21.
- `verificar.py`: scripts ejecutados sobre una base vacía sin errores, 5 o más registros por tabla, 15 casos inválidos rechazados, las 7 consultas con resultado (5, 4, 2, 6, 2, 14 y 6 filas), SQL del informe idéntico al de los scripts y `tp3-gmao.sql` al día.
- Pendiente del grupo: revisión de la redacción del Paso 1 («con sus propias palabras») y la entrega.
