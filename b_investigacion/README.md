# Investigación — TP Nº 3 GMAO

Respaldo de las Fases I y II: fichas de investigación y fuentes consultadas para los Pasos 1 y 2. Lo que se usa para redactar y no va tal cual en el PDF. El texto final está en `c_prototipado/fase1-investigacion.md` y las fuentes citadas, en `c_prototipado/referencias.md`.

## Archivos

| Archivo | Contenido | Estado |
|---|---|---|
| [`paso1-bases-de-datos.md`](paso1-bases-de-datos.md) | Definición, clasificación (relacional / NoSQL / series temporales) y 3 usos industriales. | Fichas listas, falta redacción propia |
| [`paso2-motor-sqlite.md`](paso2-motor-sqlite.md) | Justificación de SQLite y DB Browser, requerimientos de instalación, método de acceso local y notas de tipos de datos para la Fase II. | Fichas listas, faltan datos del equipo y capturas |
| [`gmao-sistemas-reales.md`](gmao-sistemas-reales.md) | Cómo modelan el mantenimiento SAP PM, Odoo y Maximo; conclusiones para el modelo de la Fase II. | Lista, con referencias propias |

## Criterio de fuentes

- Se prefiere la documentación oficial (SQLite, DB Browser, ISA) y los organismos de normalización.
- Las páginas de proveedores (InfluxData, AWS, IBM, dataPARC, etc.) se usan para definiciones generales y se marcan como tales; las cifras de rendimiento de proveedores no se citan como dato independiente.
- Los textos completos de ISA-95 e ISA-88 son pagos: se citan a través de su página oficial y de fuentes secundarias.

## Fuentes

Consultadas el 2026-10-19.

| # | Fuente | Uso |
|---|---|---|
| 1 | Codd, E. F. (1970). A relational model of data for large shared data banks. *Communications of the ACM*, 13(6), 377-387. https://doi.org/10.1145/362384.362685 | Origen del modelo relacional |
| 2 | Amazon Web Services. *What is a relational database?* https://aws.amazon.com/relational-database/ | Definición, PK/FK, SQL, ACID, restricciones |
| 3 | IBM. *What is a NoSQL database?* https://www.ibm.com/think/topics/nosql-databases | Tipos de NoSQL y diferencias con relacional |
| 4 | InfluxData. *Relational databases vs time series databases.* https://www.influxdata.com/blog/relational-databases-vs-time-series-databases/ | Características de las TSDB, arquitectura híbrida (proveedor) |
| 5 | dataPARC. *Time-series database vs. relational database vs. data lake.* https://www.dataparc.com/blog/time-series-database-vs-relational-database-vs-data-lake/ | Historiadores de proceso como TSDB (proveedor) |
| 6 | International Society of Automation. *ISA-95 Standard: Enterprise-Control System Integration.* https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard | Niveles 0-4, ERP/MES, IEC 62264 |
| 7 | TeepTrak. *MES architecture ISA-95 implementation 2026.* https://teeptrak.com/en/mes-architecture-isa-95-implementation-2026/ | Nivel 3 como capa de agregación (proveedor) |
| 8 | Wikipedia. *ISA-88.* https://en.wikipedia.org/wiki/ISA-88 | Tipos y contenido de receta ISA-88 (secundaria; la norma es ANSI/ISA-88) |
| 9 | Accendo Reliability. *CMMS in maintenance.* https://accendoreliability.com/cmms-in-maintenance/ | Funciones de un GMAO/CMMS |
| 10 | SQLite. *About SQLite.* https://www.sqlite.org/about.html | Características del motor |
| 11 | SQLite. *Appropriate Uses For SQLite.* https://www.sqlite.org/whentouse.html | Cuándo usarlo y límites |
| 12 | DB Browser for SQLite. Sitio oficial. https://sqlitebrowser.org/ | Funciones y plataformas |
| 13 | sqlitebrowser/sqlitebrowser. Repositorio en GitHub. https://github.com/sqlitebrowser/sqlitebrowser | Licencias, versión, gestores de paquetes |
| 14 | DB Browser for SQLite. *Downloads.* https://sqlitebrowser.org/dl/ | Opciones de instalación 3.13.1 |
| 15 | SQLite. *SQLite Foreign Key Support.* https://www.sqlite.org/foreignkeys.html | `PRAGMA foreign_keys` |
| 16 | SQLite. *Datatypes In SQLite.* https://www.sqlite.org/datatype3.html | Clases de almacenamiento, afinidad, fechas |

Verificación: [9] se abrió y confirma órdenes de trabajo, preventivo, repuestos e historial de activos. Una guía de proveedor sobre ISA-88 se descartó porque no confirmaba lo citado.

## Glosario de trabajo

| Término | Uso en el informe |
|---|---|
| GMAO | Gestión de Mantenimiento Asistido por Ordenador (en inglés CMMS). |
| OT | Orden de trabajo. |
| RDBMS / SGBD | Sistema gestor de bases de datos relacionales. |
| DDL / DML | Lenguaje de definición / de manipulación de datos. |
| TSDB | Base de datos de series temporales. |
| PK / FK | Clave primaria / clave foránea. |
