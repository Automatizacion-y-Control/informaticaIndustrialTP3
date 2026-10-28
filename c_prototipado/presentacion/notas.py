"""Notas de los oradores: miniatura de cada diapositiva, lo que se dice y en qué tiempo.

El texto se basa en el informe (d_presentacion/tp3-gmao-informe.pdf). Cada orador tiene
3:30 como máximo; la duración se estima a 130 palabras por minuto.
"""
from html import escape
from pathlib import Path

from generar import a_pdf

PALABRAS_POR_MINUTO = 130
AQUI = Path(__file__).parent

# (diapositiva, desde, hasta, texto). En el texto, **así** marca lo que conviene remarcar.
ORADORES = [
    {
        "archivo": "notaEmiliano", "nombre": "Emiliano Casali", "turno": 1,
        "recibe": "Abre la exposición.", "entrega": "Le pasa la palabra a Gustavo.",
        "diapos": [
            (1, "0:00", "0:10", "Buenas tardes. Somos el **Grupo 4** y les presentamos el Trabajo Práctico 3: el diseño, la implementación y la consulta de una base de datos relacional para la **gestión de mantenimiento industrial**."),
            (2, "0:10", "0:35", "El objetivo fue **investigar, diseñar, implementar y consultar** una base relacional orientada a la industria, usando SQL. Elegimos el escenario **GMAO** y trabajamos con **SQLite y DB Browser for SQLite**. Seguimos las cuatro fases y los nueve pasos del enunciado: yo presento la Fase I, Gustavo la II, Facundo la III y el Paso 7, y Gonzalo los Pasos 8 y 9."),
            (3, "0:35", "1:05", "Para que los datos tuvieran sentido planteamos una empresa ficticia: **Autopartes G4**, una metalmecánica de Córdoba con tres turnos. Tiene cuatro líneas, estampado, soldadura, mecanizado e inyección, y un compresor que da aire a toda la planta. Esas **seis máquinas** son los activos del sistema, y las mantienen cinco técnicos con un pañol propio. Los registros son simulados; las marcas y modelos, reales."),
            (4, "1:05", "1:08", "Empezamos con la **Fase I**, la investigación."),
            (5, "1:08", "1:43", "Una base de datos es un conjunto de datos relacionados, con una estructura definida, y su diferencia con una planilla es que **las reglas que deben cumplir los datos son parte de la base**. En el modelo relacional, propuesto por Codd, las tablas se vinculan por claves: la primaria identifica cada fila y la foránea crea el vínculo. Además garantiza transacciones **ACID**. Comparamos las relacionales con las NoSQL y las de series temporales, y concluimos que en una fábrica **no compiten: se complementan**."),
            (6, "1:43", "2:13", "El modelo **ISA-95** muestra dónde va cada una: las series temporales en supervisión y control, con el historiador del SCADA, y las relacionales en los niveles 3 y 4. Ahí identificamos tres usos críticos: la **integración ERP–MES**, el almacenamiento y versionado de **recetas** según ISA-88, y la **gestión del mantenimiento**, que es nuestro escenario."),
            (7, "2:13", "2:43", "Como gestor elegimos **SQLite**: no tiene servidor, la base completa es un único archivo, soporta transacciones ACID, claves foráneas, CHECK y triggers, y es de dominio público. Su límite es que admite **un solo escritor a la vez**; un GMAO multiusuario real correría sobre PostgreSQL o SQL Server, pero para diseñar y probar el modelo alcanza, y el SQL es estándar."),
            (8, "2:43", "3:25", "La herramienta es **DB Browser for SQLite 3.13.1**, que trae el motor incluido. La instalamos con winget en Windows 11; acá están los requisitos del equipo. El acceso local es abrir el archivo: **nueva base de datos gmao.db**, verificar en preferencias que las **claves foráneas** estén activadas, ejecutar los scripts en Ejecutar SQL con F5 y guardar con Ctrl+S. La captura muestra que **PRAGMA foreign_keys devuelve 1**. Le paso la palabra a Gustavo."),
        ],
    },
    {
        "archivo": "notaGustavo", "nombre": "Gustavo Del Soto", "turno": 2,
        "recibe": "Recibe la palabra de Emiliano.", "entrega": "Le pasa la palabra a Facundo.",
        "diapos": [
            (9, "0:00", "0:05", "Gracias, Emiliano. La **Fase II** es la planificación: pasar del escenario a un modelo de datos."),
            (10, "0:05", "0:55", "Para definir las entidades relevamos cómo resuelven el mantenimiento **SAP PM, Odoo e IBM Maximo**. Los tres coinciden en que el correctivo y el preventivo tienen **orígenes distintos** y terminan en la misma orden de trabajo. El correctivo nace de una **falla**: se registra y se emite una orden correctiva; mientras no hay orden, la falla queda pendiente. El preventivo nace de un **plan**, con una tarea cada tantos días u horas de uso. La orden se asigna a un técnico y consume repuestos. Así surgen **siete tablas**: las cinco entidades del enunciado, los planes preventivos y la tabla intermedia ot_repuestos."),
            (11, "0:55", "1:45", "Para cada atributo elegimos el tipo de dato, porque **una variable analógica guardada como texto no se puede promediar**. SQLite asigna cada tipo declarado a una **afinidad**: INTEGER para identificadores y cantidades, VARCHAR para textos, FLOAT para horas y costos, y DATE o DATETIME para las marcas de tiempo, en formato **ISO 8601**. Acá ven la estructura de la tabla central, órdenes de trabajo: clave primaria, tres claves foráneas y CHECK para el tipo y el estado. En el informe están las siete tablas."),
            (12, "1:45", "2:10", "Este es el **diagrama entidad-relación**, la Figura 7 del informe. Muestra las **claves primarias** sombreadas, las **foráneas** marcadas y los campos únicos, con la notación de **pata de gallo**: doble barra es exactamente uno, y pata de gallo con círculo, cero o muchos."),
            (13, "2:10", "2:35", "En detalle: la **orden de trabajo** está en el centro. Una máquina tiene muchas fallas y muchas órdenes, y cada orden tiene un técnico. La relación entre fallas y órdenes es **opcional**: una falla puede quedar pendiente, sin orden."),
            (14, "2:35", "2:50", "Abajo, los **planes preventivos**, que originan las órdenes preventivas, y la tabla **ot_repuestos**, con clave primaria compuesta."),
            (15, "2:50", "3:25", "Todas las relaciones son **uno a muchos**, con la clave foránea del lado muchos, salvo la de órdenes y repuestos, que es **muchos a muchos** y se resuelve con ot_repuestos. El diseño está en **tercera forma normal**. Además definimos tres reglas del proceso: la preventiva tiene plan y la correctiva no, con un **CHECK**; y la orden y su plan, o la falla y su orden, deben ser de la misma máquina, con **triggers**, porque un CHECK no puede consultar otra tabla. Ahora Facundo les muestra la construcción."),
        ],
    },
    {
        "archivo": "notaFacundo", "nombre": "Facundo Ferrero", "turno": 3,
        "recibe": "Recibe la palabra de Gustavo.", "entrega": "Le pasa la palabra a Gonzalo.",
        "diapos": [
            (16, "0:00", "0:04", "Gracias, Gustavo. En la **Fase III** el modelo se convierte en una base real."),
            (17, "0:04", "0:39", "Escribimos **a mano un CREATE TABLE por tabla**, con sus restricciones: PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE y CHECK. Acá ven el de fallas: id_ot admite NULL porque la falla puede estar pendiente. El script empieza con **PRAGMA foreign_keys = ON** y DROP TABLE IF EXISTS, para poder reejecutarlo, y crea las tablas en el **orden de sus dependencias**, con los cuatro triggers al final."),
            (18, "0:39", "1:01", "Lo ejecutamos completo en **DB Browser** y terminó **sin errores**. En la pestaña Estructura se ven las **siete tablas**, con las columnas de órdenes de trabajo desplegadas, y los **cuatro disparadores**."),
            (19, "1:01", "1:31", "Después cargamos los datos con **INSERT INTO**: cinco o más registros por tabla, simulados pero pensados para que **las consultas devuelvan resultados significativos**. Por ejemplo, el torno es el activo con más fallas, una orden atiende dos fallas, una falla queda pendiente y dos repuestos están bajo el mínimo. La carga sigue el orden de las claves foráneas, y también terminó sin errores."),
            (20, "1:31", "1:41", "Estas son las **tablas pobladas** en la pestaña Hoja de datos: las seis máquinas y los seis consumos de repuestos."),
            (21, "1:41", "1:51", "Y las **trece órdenes de trabajo**: ocho correctivas y cinco preventivas, en los tres estados. Las correctivas tienen el plan en NULL."),
            (22, "1:51", "2:15", "Para comprobar las restricciones **intentamos cargar datos inválidos**, aparte del script. Por ejemplo, una orden preventiva sin plan: DB Browser la rechaza con **CHECK constraint failed**. La tabla muestra los otros intentos y el mensaje con que la base rechazó cada uno."),
            (23, "2:15", "2:18", "Con la base cargada, pasamos a la **Fase IV**: consultarla."),
            (24, "2:18", "2:46", "El Paso 7 pide consultas con **WHERE, ORDER BY y operadores lógicos** para el supervisor. La primera trae las fallas de severidad alta o media entre el 15 de septiembre y el 10 de octubre, con **BETWEEN, IN y AND**. Como las fechas están en ISO 8601, BETWEEN funciona sin convertirlas. El resultado son **cinco fallas**."),
            (25, "2:46", "3:06", "La segunda es para el pañol: los repuestos con stock en el mínimo o por debajo, ordenados por lo que falta. Son **cuatro**: dos por debajo y dos justo en el mínimo."),
            (26, "3:06", "3:25", "La tercera usa **NOT** para listar las correctivas que no están cerradas: hay **dos**, una en curso y una pendiente. Gonzalo sigue con las agrupaciones."),
        ],
    },
    {
        "archivo": "notaGonzalo", "nombre": "Gonzalo Vera", "turno": 4,
        "recibe": "Recibe la palabra de Facundo.", "entrega": "Cierra la exposición y abre las preguntas.",
        "diapos": [
            (27, "0:00", "0:35", "Gracias, Facundo. En el Paso 8 usamos **funciones de agregación con GROUP BY**. Contamos las fallas por máquina y sumamos sus horas de parada: la máquina 1, el **torno CNC**, es el activo más crítico, con **tres fallas y diez horas y media de parada**, todas en el husillo."),
            (28, "0:35", "1:05", "La segunda agrupa las órdenes por tipo: el correctivo concentra **el 77,5 % de las horas-hombre**. Una planta con mucho correctivo trabaja apagando incendios; el objetivo es pasar horas al preventivo. Ojo: las funciones de agregación **ignoran los NULL**, por eso las órdenes pendientes cuentan como órdenes pero no suman horas."),
            (29, "1:05", "1:45", "El resultado anterior muestra el número de máquina, y el operador **no lee códigos**. El Paso 9 lo resuelve con JOIN. Esta es la consulta que pide el enunciado: une la orden con la máquina y el técnico con **INNER JOIN**, porque siempre existen. La falla y el plan van con **LEFT JOIN**, porque dependen del tipo de orden: con INNER se perderían las cinco preventivas. **COALESCE** muestra la falla o la tarea del plan en una sola columna."),
            (30, "1:45", "2:00", "Y este es el reporte legible: **catorce filas para trece órdenes**, porque la 0107 atiende dos fallas de la prensa. La falla pendiente de la inyectora no aparece, porque todavía no tiene orden."),
            (31, "2:00", "2:10", "En la otra parte del resultado se ve el **motivo**, el **técnico** y el **estado** de cada orden."),
            (32, "2:10", "2:38", "La última parte de la tabla intermedia y **calcula el costo** de cada consumo. Son seis consumos por **2.396.100 pesos**, y la placa del robot explica el 77 % del gasto. Además su stock quedó en cero, lo mismo que mostró la consulta de stock crítico."),
            (33, "2:38", "3:00", "Para cerrar, la **tabla de control del enunciado**: los nueve pasos están en el informe, cada uno con su justificación, su procedimiento y sus capturas, y todo el SQL está además en el script **tp3-gmao.sql**."),
            (34, "3:00", "3:20", "Como anexo, el grupo hizo una **implementación web** con el mismo modelo. Si quieren verla, pueden entrar con este **código QR**."),
            (35, "3:20", "3:25", "Muchas gracias. **¿Preguntas?**"),
        ],
    },
]

ESTILO = """
@page { size: A4; margin: 14mm 14mm 12mm; }
* { box-sizing: border-box; }
body { margin: 0; font-family: "IBM Plex Sans", Arial, sans-serif; color: #1B1E22; font-size: 10.5pt; }
header { border-bottom: 2px solid #1B1E22; padding-bottom: 8px; margin-bottom: 10px; }
header .k { font-family: "IBM Plex Mono", monospace; font-size: 8.5pt; color: #0E6B63; text-transform: uppercase; letter-spacing: .04em; }
header h1 { margin: 2px 0 4px; font-size: 22pt; font-weight: 600; }
header .datos { display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: 9.5pt; color: #5E656E; }
header .datos b { color: #1B1E22; }
.fila { display: grid; grid-template-columns: 54mm 1fr; gap: 5mm; padding: 7px 0; border-bottom: 1px solid #D8DBD5; break-inside: avoid; }
.fila img { width: 54mm; border: 1px solid #C3CBC8; display: block; }
.tiempo { font-family: "IBM Plex Mono", monospace; font-size: 8.5pt; color: #0E6B63; margin-bottom: 3px; }
.tiempo b { color: #1B1E22; }
.fila p { margin: 0; line-height: 1.42; }
.fila p strong { color: #0E6B63; font-weight: 600; }
.cierre { margin-top: 10px; padding: 8px 10px; background: #F6F6F3; border-left: 4px solid #0E6B63; font-size: 9.5pt; }
"""


def parrafo(texto: str) -> str:
    partes = escape(texto).split("**")
    return "".join(f"<strong>{p}</strong>" if i % 2 else p for i, p in enumerate(partes))


def duracion(orador: dict) -> tuple[int, str]:
    palabras = sum(len(d[3].replace("**", "").split()) for d in orador["diapos"])
    seg = round(palabras / PALABRAS_POR_MINUTO * 60)
    return palabras, f"{seg // 60}:{seg % 60:02d}"


def armar(exposicion: Path) -> None:
    import pymupdf
    miniaturas = exposicion / "miniaturas"
    for o in ORADORES:
        palabras, estimado = duracion(o)
        primera, ultima = o["diapos"][0][0], o["diapos"][-1][0]
        filas = "".join(
            f'<div class="fila"><img src="{(miniaturas / f"diapo-{n:02d}.png").as_uri()}">'
            f'<div><div class="tiempo"><b>Diapositiva {n}</b> · {desde} – {hasta}</div><p>{parrafo(txt)}</p></div></div>'
            for n, desde, hasta, txt in o["diapos"])
        html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Notas — {o['nombre']}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=block">
<style>{ESTILO}</style></head><body>
<header><div class="k">Notas del orador · TP Nº 3 — GMAO · Grupo Nº 4</div><h1>{o['nombre']}</h1>
<div class="datos"><span>Turno <b>{o['turno']} de 4</b></span><span>Diapositivas <b>{primera} a {ultima}</b></span>
<span>Tiempo máximo <b>3:30</b></span><span>Texto: <b>{palabras} palabras ≈ {estimado}</b></span></div></header>
<div class="tiempo" style="margin-bottom:4px">{escape(o['recibe'])}</div>
{filas}
<div class="cierre"><b>Al terminar:</b> {escape(o['entrega'])} Todo lo que se dice está en el informe; lo resaltado en verde es lo que conviene remarcar.</div>
</body></html>"""
        fuente = AQUI / f"{o['archivo']}.html"
        fuente.write_text(html, encoding="utf-8")
        pdf = exposicion / f"{o['archivo']}.pdf"
        a_pdf(fuente, pdf)
        fuente.unlink()
        paginas = len(pymupdf.open(pdf))
        print(f"{pdf.name}: {palabras} palabras, aprox. {estimado}, {paginas} pagina(s)")
