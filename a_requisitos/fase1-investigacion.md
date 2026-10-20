# Fase I — Fundamentos y clasificación (Investigación)

Requisitos de los Pasos 1 y 2 del enunciado. Cada paso lleva justificación teórica, descripción del procedimiento y capturas legibles.

## Paso 1 — Definición y usos industriales de las bases de datos

- **R1.1** Definir con palabras propias qué es una base de datos.
- **R1.2** Explicar cómo se clasifican, comparando como mínimo **relacionales vs. NoSQL / series temporales**: modelo de datos, esquema, consistencia, escalabilidad y caso de uso típico en planta.
- **R1.3** Explicar en detalle **tres (3) usos críticos** de las bases de datos relacionales en una fábrica moderna. Ejemplos del enunciado: integración con sistemas ERP/MES, almacenamiento de recetas de proceso. Tercero: gestión de mantenimiento e historial de activos, que enlaza con el escenario GMAO.
- **R1.4** Citar las fuentes consultadas.

**Evidencia en el informe:** texto explicativo e investigación de usos industriales.

## Paso 2 — Selección del motor de base de datos y requerimientos

- **R2.1** Justificar la elección de **SQLite**: motor embebido, sin servidor, base en un único archivo, dominio público, soporte de transacciones y de claves foráneas.
- **R2.2** Justificar **DB Browser for SQLite** como herramienta gráfica de gestión.
- **R2.3** Detallar los **requerimientos de instalación**: sistema operativo, versión instalada, espacio, dependencias y procedimiento de instalación.
- **R2.4** Describir el **método de acceso local**: crear y abrir el archivo `.db`, la pestaña *Ejecutar SQL*, *Escribir cambios* y la activación de claves foráneas (`PRAGMA foreign_keys = ON`).

**Evidencia en el informe:** definición del software a usar y sus requisitos de sistema, con capturas de la instalación y de la base creada.

## Criterios de aceptación de la fase

- [ ] Paso 1: texto propio con definición, clasificación relacional vs. NoSQL/series temporales y 3 usos industriales detallados.
- [ ] Paso 2: software elegido y justificado, requisitos de sistema y método de acceso local.
- [ ] Capturas de la instalación y de la base vacía creada en DB Browser.
- [ ] Fuentes citadas.
