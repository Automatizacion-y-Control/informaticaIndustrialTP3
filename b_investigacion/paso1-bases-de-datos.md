# Paso 1 — Investigación: definición, clasificación y usos industriales

Fichas de investigación para redactar el Paso 1 (requisitos R1.1 a R1.4 de `a_requisitos/fase1-investigacion.md`). **No es el texto del informe**: el enunciado pide redactarlo "con sus propias palabras", así que estas notas son la base para que el grupo escriba en `c_prototipado/fase1-investigacion.md`. Las referencias [n] están en el [README](README.md#fuentes).

## 1. Qué es una base de datos (R1.1)

- Una **base de datos** es un conjunto organizado de datos relacionados entre sí, guardados de forma persistente para que varios usuarios o programas los consulten y actualicen.
- El **sistema gestor de bases de datos (SGBD / DBMS)** es el software que administra esa base: define la estructura, controla el acceso, mantiene la integridad y resuelve las consultas.
- **Base de datos relacional:** organiza los datos en **tablas** (filas = registros, columnas = atributos) con relaciones predefinidas entre ellas [2]. Cada fila se identifica con una **clave primaria (PK)**; una **clave foránea (FK)** apunta a la PK de otra tabla y crea el vínculo [2].
- Origen del modelo: E. F. Codd lo propuso en 1970 [1]. Se basa en la teoría de conjuntos y en que los datos se describen independientemente de cómo se almacenan físicamente.
- **SQL** es el lenguaje estándar para definir (DDL), manipular (DML) y consultar los datos relacionales [2].
- **Transacciones ACID** [2]:
  - *Atomicidad*: una transacción se hace completa o se deshace.
  - *Consistencia*: los datos cumplen siempre las reglas definidas (restricciones, claves).
  - *Aislamiento*: transacciones simultáneas no se interfieren.
  - *Durabilidad*: lo confirmado persiste aunque se corte la energía.
- **Integridad**: se garantiza con restricciones `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `DEFAULT` y `CHECK` [2]. Enlaza directamente con el Paso 5.

## 2. Clasificación (R1.2)

### 2.1 Relacionales (SQL)

- Esquema fijo y definido de antemano; relaciones por claves; consultas con `JOIN`; consistencia fuerte (ACID).
- Escalan principalmente en forma **vertical** (más hardware en un servidor) [3].
- Ejemplos: SQLite, PostgreSQL, MySQL/MariaDB, SQL Server, Oracle.
- En planta: datos de negocio y de gestión con estructura estable (órdenes, activos, recetas, usuarios, inventarios) [4].

### 2.2 NoSQL ("not only SQL")

- Guardan los datos fuera del modelo de tablas; suelen ser distribuidas y **no exigen esquema fijo** [3].
- Escalan en forma **horizontal** (repartiendo datos entre servidores, *sharding*) [3].
- Tipos [3]:
  - **Documentales** (JSON/BSON) — p. ej. MongoDB.
  - **Clave-valor** — p. ej. Redis (caché, sesiones).
  - **Columnares amplias** (*wide-column*) — p. ej. Cassandra, HBase.
  - **De grafos** (nodos y aristas) — p. ej. Neo4j.
- Contra: transacciones complejas y relaciones entre entidades más difíciles de garantizar [3].

### 2.3 Series temporales (TSDB) e historiadores

- Diseñadas para datos con **marca de tiempo** escritos en forma continua: altísimo volumen de escritura y consultas por **rangos de tiempo** [4].
- Escritura casi siempre de tipo *append* (se agrega, rara vez se modifica o borra un punto) [4].
- Políticas de **retención** y borrado masivo; fuerte **compresión** al guardar juntos valores del mismo tipo [4].
- Casos típicos: sensores de fábrica, IoT, monitoreo [4]. Los **historiadores de proceso** (*data historians*) de los sistemas SCADA son una categoría de TSDB [5].
- Ejemplos: InfluxDB, TimescaleDB, historiadores industriales.

### 2.4 Tabla comparativa (borrador para el informe)

| Criterio | Relacional | NoSQL | Series temporales |
|---|---|---|---|
| Modelo | Tablas y relaciones por claves | Documentos, clave-valor, columnas, grafos | Mediciones con marca de tiempo |
| Esquema | Fijo, definido antes de cargar | Flexible o sin esquema | Flexible; centrado en el tiempo |
| Consistencia | Fuerte (ACID) | Variable según el motor | Orientada a escritura masiva |
| Escalado | Vertical | Horizontal | Horizontal / compresión |
| Consulta típica | `JOIN` entre entidades, reportes | Lectura por clave o documento | Rangos de tiempo, promedios, tendencias |
| Uso en planta | ERP, MES, GMAO, recetas, calidad | Datos heterogéneos, configuraciones, logs | Variables de proceso, sensores, historiador SCADA |

**Idea fuerza:** en una fábrica no compiten, se **complementan**. Lo habitual es una arquitectura híbrida: relacional para las entidades de negocio y TSDB para las mediciones de alta frecuencia [4].

## 3. Tres usos críticos de las bases relacionales en la fábrica (R1.3)

### Uso 1 — Integración ERP ↔ MES (modelo ISA-95)

- **ISA-95 / IEC 62264** es el estándar para integrar los sistemas de negocio con los de control de manufactura; organiza la empresa en niveles 0 a 4 [6]:
  - Nivel 0: proceso físico. Nivel 1: sensores y actuadores. Nivel 2: control (PLC, DCS).
  - **Nivel 3: gestión de operaciones de manufactura (MES, SCADA).**
  - **Nivel 4: planificación de negocio y logística (ERP).**
- El estándar se centra en la interfaz entre los niveles 3 y 4, y define **modelos de objetos y atributos** (equipos, materiales, personal, órdenes) que son la base para diseñar bases relacionales [6][7].
- Qué guarda la base relacional: órdenes de producción que bajan del ERP, consumos y producción real que suben del MES, maestros de materiales y equipos. Requiere integridad referencial (una orden no puede apuntar a un material inexistente) y transacciones ACID.
- El ERP es transaccional y no está pensado para datos de sensores en tiempo real; el nivel 3 hace de capa de agregación [7].

### Uso 2 — Almacenamiento y versionado de recetas de proceso (modelo ISA-88)

- **ISA-88** (control por lotes) define cuatro tipos de receta: general, de sitio, **maestra** y **de control**. Una receta contiene encabezado, fórmula (parámetros y materiales), requerimientos de equipo y procedimiento [8].
- La receta **maestra** es la aprobada para un conjunto de equipos; la receta **de control** es la copia que se ejecuta en un lote concreto, con sus valores reales [8]. En la práctica, las recetas maestras se guardan en la base de datos del MES o del sistema de lotes con su versión y estado de aprobación (desarrollo propio: no citar como dato del estándar).
- Por qué relacional: una receta es un conjunto estructurado de pasos, parámetros, consignas y materiales con relaciones entre sí; hace falta versionado, aprobación y trazabilidad de qué receta se usó en cada lote.

### Uso 3 — Gestión del mantenimiento (GMAO / CMMS)

- Un **GMAO** (en inglés CMMS) centraliza el mantenimiento: registro de activos e historial, órdenes de trabajo, planes preventivos y control de repuestos [9].
- Datos que guarda [9]:
  - **Activos:** especificaciones, historial de mantenimiento, manuales, garantías y repuestos asociados.
  - **Órdenes de trabajo:** se registran, priorizan, asignan a técnicos y se siguen hasta su cierre.
  - **Preventivo:** tareas recurrentes disparadas por tiempo, lecturas de medidores o uso.
  - **Repuestos:** niveles de stock y reposición cuando bajan del mínimo.
- Por qué relacional: entidades bien definidas y fuertemente relacionadas (máquina → falla → orden de trabajo → técnico → repuestos); los reportes cruzan tablas (`JOIN`) y calculan indicadores (fallas por máquina, tiempos de parada, horas-hombre).
- **Es el escenario elegido para el TP**: este uso enlaza con las Fases II a IV.

## 4. Pendiente para la redacción

- [ ] Redactar con palabras propias la definición y la clasificación.
- [ ] Convertir la tabla comparativa en tabla del informe.
- [ ] Desarrollar los 3 usos (un párrafo de contexto + qué datos guarda + por qué relacional).
- [ ] Decidir si se incluye un diagrama Mermaid de la pirámide ISA-95 (niveles 0-4) para el Uso 1.
- [ ] Citar las fuentes en `referencias.md`.
