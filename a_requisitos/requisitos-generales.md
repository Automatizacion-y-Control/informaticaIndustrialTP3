# Requisitos generales del informe

Propósito, audiencia, alcance, idioma, origen y restricciones del TP Nº 3. Tomados del enunciado `TRABAJO PRACTICO NRO 3 - BASE DE DATOS.pdf` y de lo acordado con el usuario. Lo marcado como **[A CONFIRMAR]** es una propuesta pendiente de aprobación.

## 1. Propósito

Informe técnico formal que documenta, paso a paso, la investigación, el diseño, la implementación y la consulta de una base de datos relacional para un sistema GMAO, usando SQL sobre SQLite. Es la evidencia evaluable de que el trabajo se hizo en el orden exigido (Pasos 1 a 9).

## 2. Audiencia

El docente de Informática Industrial que corrige el TP. Conoce bases de datos y SQL. Evalúa la justificación teórica, la corrección del SQL y la evidencia (capturas) de cada paso.

## 3. Alcance

**Incluye:**

- Las 4 fases y los 9 pasos del enunciado, en ese orden y con esos títulos.
- En cada paso: **justificación teórica**, **descripción detallada del procedimiento** y **capturas de pantalla legibles** del gestor como evidencia.
- Los bloques de código SQL en **texto plano** (copiables) dentro del informe, no solo como imagen.
- Un script `.sql` de respaldo, aparte del PDF.

**Queda afuera:**

- Los otros dos escenarios (Trazabilidad de lotes y Control de calidad).
- Otros motores (MySQL, PostgreSQL, SQL Server), salvo como comparación en el Paso 2.
- Aplicaciones, formularios o interfaces sobre la base. La integración real con PLC, SCADA, ERP o MES se menciona solo como uso en el Paso 1.

**Entrega:** única (PDF + `.sql`), pero se **trabaja por fases**: cada fase se cierra y se valida con el usuario antes de pasar a la siguiente.

## 4. Idioma y registro

- Español rioplatense, registro técnico formal, en forma impersonal ("se definió", "se ejecutó").
- Quedan en inglés las palabras clave de SQL (`CREATE TABLE`, `PRIMARY KEY`, `INNER JOIN`…), los tipos de datos y las siglas de uso corriente (RDBMS, NoSQL, ERP, MES, SCADA, PK, FK, DER, DDL, DML).
- Nombres de tablas y columnas en español, en `snake_case`, sin tildes ni ñ (por ejemplo `ordenes_trabajo`, `id_maquina`).

## 5. Origen y licencia

- **Contenido propio** del alumno. El enunciado exige que el Paso 1 se redacte "con sus propias palabras" y que el SQL del Paso 5 se escriba "de manera manual".
- Las fuentes consultadas en los Pasos 1 y 2 se citan en una sección de referencias y se registran en `b_investigacion/`.
- Los datos de planta del Paso 6 son **simulados**, y así se declara en el informe.
- No se usan logos ni marcas de terceros. La portada va sin logo, solo con texto.

## 6. Restricciones y responsabilidades

- Las **capturas de pantalla** las toma el usuario en DB Browser for SQLite en su equipo: son la evidencia de una ejecución real y no se reemplazan por imágenes generadas.
- El SQL del informe y el del `.sql` deben ser **idénticos** al ejecutado en las capturas.
- Todo el script se tiene que poder ejecutar de corrido sobre una base vacía, sin errores.
- No se avanza a la fase siguiente sin validar la anterior.
