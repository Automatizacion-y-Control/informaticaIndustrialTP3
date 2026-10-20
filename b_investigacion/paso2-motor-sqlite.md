# Paso 2 — Investigación: motor de base de datos y requerimientos

Fichas de investigación para redactar el Paso 2 (requisitos R2.1 a R2.4 de `a_requisitos/fase1-investigacion.md`). Las referencias [n] están en el [README](README.md#fuentes).

## 1. Por qué SQLite (R2.1)

Características del motor, según la documentación oficial [10]:

- **Sin servidor:** es una biblioteca que corre dentro del programa y lee y escribe directamente sobre archivos de disco. No hay un proceso servidor que instalar ni administrar.
- **Configuración cero** y **autocontenido**.
- **Un solo archivo:** toda la base (tablas, índices, *triggers*, vistas) queda en un único archivo, fácil de copiar y entregar.
- **Transacciones ACID**, aun ante caídas del sistema o cortes de energía.
- **Dominio público:** libre para cualquier uso, comercial o privado.
- **Multiplataforma:** el archivo se puede copiar entre sistemas de 32 y 64 bits y entre arquitecturas distintas.
- **Liviano:** la biblioteca completa pesa menos de 900 KiB.
- **Formato estable:** los desarrolladores se comprometen a mantener compatibilidad hasta el año 2050.

Cuándo conviene, según el propio proyecto [11]:

- Dispositivos embebidos e IoT (no requiere administración; funciona en el borde de la red con conectividad pobre).
- Formato de archivo de aplicaciones y análisis de datos.
- **Educación y formación:** instalación trivial y bases fáciles de crear y compartir. **Es el caso de este TP.**

Límites a mencionar con honestidad [11]:

- **Un solo escritor a la vez:** no sirve para muchos clientes escribiendo en simultáneo.
- No se recomienda acceder por red (sistemas de archivos de red).
- Para volúmenes del orden de terabytes conviene un motor cliente-servidor.
- **Conclusión para el informe:** en una planta real, un GMAO multiusuario correría sobre un motor cliente-servidor (PostgreSQL, SQL Server, MySQL). SQLite alcanza para diseñar y probar el modelo, y el SQL estándar usado es trasladable.

### Comparación breve (borrador)

| Criterio | SQLite | Cliente-servidor (PostgreSQL, MySQL, SQL Server) |
|---|---|---|
| Arquitectura | Biblioteca embebida, archivo local | Servicio en un servidor, acceso por red |
| Instalación | Nula (copiar un ejecutable o usar DB4S) | Instalar y configurar un servicio, usuarios y permisos |
| Concurrencia de escritura | Un escritor a la vez | Muchos escritores simultáneos |
| Entrega del TP | Un archivo `.db` | Requiere exportar un *dump* |
| Uso típico | Embebido, IoT, educación, prototipos | Sistemas de planta multiusuario |

## 2. Por qué DB Browser for SQLite (R2.2)

- Herramienta **visual y de código abierto** para crear, buscar y editar bases SQLite (y SQLCipher) con interfaz tipo planilla y soporte completo de SQL [12].
- Funciones útiles para el TP [12]:
  - crear y compactar bases;
  - crear, modificar y borrar tablas e índices;
  - hojear, editar, ordenar y buscar registros (**capturas del Paso 6**);
  - **ejecutar consultas SQL y ver los resultados** (capturas de los Pasos 5, 7, 8 y 9);
  - importar y exportar CSV y volcados SQL (**sirve para generar el `.sql` de respaldo**);
  - registro de los comandos SQL ejecutados;
  - gráficos simples a partir de tablas o consultas.
- Multiplataforma: Windows, macOS y la mayoría de las distribuciones Linux [12].
- Licencia: proyecto de código abierto; el repositorio publica las licencias GPL-3.0 y MPL-2.0 [13].
- Versión estable actual: **3.13.1**, publicada el 16/10/2024 [13][14].

## 3. Requerimientos de instalación (R2.3)

Opciones de descarga para Windows (versión 3.13.1) [14]:

| Opción | Arquitecturas |
|---|---|
| Instalador estándar `.msi` | 32 bits, 64 bits, ARM64 |
| `.zip` sin instalador | 32 bits, 64 bits, ARM64 |
| PortableApp (`.paf.exe`) | No disponible para ARM64 |

- Los ejecutables para Windows están firmados digitalmente (SignPath.io) [14].
- También se instala con gestores de paquetes: `winget`, Chocolatey o scoop [13].
- macOS: DMG universal o `brew install db-browser-for-sqlite`. Linux: AppImage, Snap o paquetes de la distribución [14].
- **No hace falta instalar SQLite aparte:** DB Browser trae el motor incluido.
- La página oficial **no publica requisitos mínimos de hardware ni de versión de Windows** [14]. Para el informe se documentan los datos del equipo donde se hizo el TP.

**A completar por el grupo** (con captura):

- [ ] Sistema operativo y versión del equipo usado.
- [ ] Versión de DB Browser instalada (menú *Ayuda → Acerca de*) y versión de SQLite que trae.
- [ ] Opción de instalación elegida (`.msi` 64 bits recomendado).

## 4. Método de acceso local (R2.4)

Procedimiento a documentar paso a paso, con captura de cada pantalla:

1. Abrir DB Browser for SQLite.
2. **Nueva base de datos** → elegir carpeta y nombre (propuesta: `gmao.db`). Si se abre el asistente de tablas, cancelarlo: las tablas se crean por SQL en el Paso 5.
3. Pestaña **Ejecutar SQL**: escribir o pegar el script y ejecutarlo (botón ▶ o `Ctrl+Retorno`; `F5` ejecuta todo).
4. Revisar el panel de mensajes: indica si la ejecución terminó sin errores y cuánto tardó.
5. **Escribir cambios** (`Ctrl+S`): confirma la transacción en el archivo. Sin este paso los cambios se pierden al cerrar.
6. Pestañas **Estructura de la base de datos** (tablas y columnas creadas) y **Hojear datos** (registros cargados).

**Claves foráneas:** en SQLite la verificación de FK está **desactivada por defecto** y se activa en cada conexión con `PRAGMA foreign_keys = ON;`. Se consulta con `PRAGMA foreign_keys;` (0 = desactivada, 1 = activada). Existe desde la versión 3.6.19 [15].

- [ ] Verificar en DB Browser (*Editar → Preferencias → Base de datos*) si la opción de claves foráneas viene activada, y de todas formas incluir el `PRAGMA` al comienzo del script.

## 5. Notas para la Fase II (tipos de datos en SQLite)

Se usan en el Paso 3 (R3.3). SQLite tiene tipado dinámico [16]:

- **Clases de almacenamiento:** `NULL`, `INTEGER`, `REAL`, `TEXT`, `BLOB`.
- **Afinidad** según el tipo declarado (gana la primera regla que coincide):
  1. contiene `INT` → INTEGER (`INT`, `INTEGER`, `BIGINT`);
  2. contiene `CHAR`, `CLOB` o `TEXT` → TEXT (`VARCHAR(50)` también; el largo se ignora);
  3. contiene `BLOB` o no tiene tipo → BLOB;
  4. contiene `REAL`, `FLOA` o `DOUB` → REAL (`FLOAT`, `DOUBLE`);
  5. el resto → NUMERIC (`DATETIME`, `DATE`, `DECIMAL`, `BOOLEAN`).
- **Fechas:** no hay un tipo propio. Se guardan como texto ISO 8601 (`AAAA-MM-DD HH:MM:SS`), como número juliano (REAL) o como tiempo Unix (INTEGER). En una columna `DATETIME`, un texto ISO 8601 queda guardado como TEXT [16].
- Consecuencia: se pueden declarar `VARCHAR`, `FLOAT` y `DATETIME` como pide el enunciado; SQLite los acepta y los mapea por afinidad.
