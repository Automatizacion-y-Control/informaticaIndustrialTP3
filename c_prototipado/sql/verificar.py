"""Verifica los scripts SQL del TP trabajando sobre copias.

Todo se hace en una carpeta temporal del sistema, fuera del proyecto, que se borra al terminar.
Los archivos del proyecto solo se leen: no se crea, modifica ni borra ninguno.

1. Copia los scripts a la carpeta temporal y los ejecuta sobre una base vacía creada ahí.
2. Cuenta los registros por tabla (mínimo 5 por tabla, según el enunciado).
3. Prueba que la base rechace los casos inválidos (FK, CHECK, triggers).
3b. Ejecuta las consultas de la Fase IV y comprueba que ninguna devuelva un resultado vacío.
4. Comprueba que el código SQL del informe sea idéntico al de los scripts.
5. Arma un tp3-gmao.sql de prueba en la carpeta temporal y lo compara con el entregable
   d_presentacion/tp3-gmao.sql: informa si está al día o desactualizado.

Uso:
  python verificar.py           solo verifica (no escribe nada en el proyecto)
  python verificar.py --armar   además, reemplaza d_presentacion/tp3-gmao.sql por la versión armada
"""
import re
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PROTO = AQUI.parent
RAIZ = PROTO.parent
SCRIPTS = ['paso5-ddl.sql', 'paso6-dml.sql']
CONSULTAS = 'fase4-consultas.sql'
INFORMES = {'paso5-ddl.sql': 'fase3-construccion.md', 'paso6-dml.sql': 'fase3-construccion.md',
            CONSULTAS: 'fase4-explotacion.md'}
TABLAS = ['maquinas', 'tecnicos', 'repuestos', 'planes_preventivos', 'ordenes_trabajo', 'fallas', 'ot_repuestos']

INVALIDOS = [
    ('OT preventiva sin plan',
     "INSERT INTO ordenes_trabajo VALUES (90,'OT-X1','PREVENTIVA',1,NULL,1,'2026-10-20 08:00:00',NULL,'PENDIENTE','x',NULL)"),
    ('OT correctiva con plan',
     "INSERT INTO ordenes_trabajo VALUES (90,'OT-X1','CORRECTIVA',1,1,1,'2026-10-20 08:00:00',NULL,'PENDIENTE','x',NULL)"),
    ('OT preventiva de otra máquina que su plan',
     "INSERT INTO ordenes_trabajo VALUES (90,'OT-X1','PREVENTIVA',2,1,1,'2026-10-20 08:00:00',NULL,'PENDIENTE','x',NULL)"),
    ('Falla asignada a una OT preventiva',
     "INSERT INTO fallas VALUES (90,3,2,'2026-10-20 08:00:00','x','MECANICA','BAJA',0)"),
    ('Falla asignada a una OT de otra máquina',
     "INSERT INTO fallas VALUES (90,2,1,'2026-10-20 08:00:00','x','MECANICA','BAJA',0)"),
    ('Falla reasignada a una OT preventiva (UPDATE)',
     "UPDATE fallas SET id_ot = 5 WHERE id_falla = 1"),
    ('OT con fallas cambiada a preventiva (UPDATE)',
     "UPDATE ordenes_trabajo SET tipo = 'PREVENTIVA', id_plan = 1 WHERE id_ot = 1"),
    ('Máquina inexistente (FK)',
     "INSERT INTO fallas VALUES (90,99,NULL,'2026-10-20 08:00:00','x','MECANICA','BAJA',0)"),
    ('Técnico inexistente (FK)',
     "INSERT INTO ordenes_trabajo VALUES (90,'OT-X1','CORRECTIVA',1,NULL,99,'2026-10-20 08:00:00',NULL,'PENDIENTE','x',NULL)"),
    ('Estado fuera de la lista (CHECK)',
     "INSERT INTO ordenes_trabajo VALUES (90,'OT-X1','CORRECTIVA',1,NULL,1,'2026-10-20 08:00:00',NULL,'ABIERTA','x',NULL)"),
    ('Número de OT repetido (UNIQUE)',
     "INSERT INTO ordenes_trabajo VALUES (90,'OT-2026-0101','CORRECTIVA',1,NULL,1,'2026-10-20 08:00:00',NULL,'PENDIENTE','x',NULL)"),
    ('Campo obligatorio vacío (NOT NULL)',
     "INSERT INTO maquinas (id_maquina, codigo, nombre, sector, criticidad) VALUES (90, 'X-01', NULL, 'X', 'ALTA')"),
    ('Repuesto repetido en la misma OT (PK compuesta)',
     "INSERT INTO ot_repuestos VALUES (1,1,2)"),
    ('Cantidad cero (CHECK)',
     "INSERT INTO ot_repuestos VALUES (3,2,0)"),
    ('Borrar una máquina con historial (FK)',
     "DELETE FROM maquinas WHERE id_maquina = 1"),
]


def leer(ruta):
    return Path(ruta).read_text(encoding='utf-8')


def sin_comentarios(sql):
    """Sentencias del script sin comentarios ni líneas vacías, para comparar con el informe."""
    lineas = [l.rstrip() for l in sql.splitlines()]
    return '\n'.join(l for l in lineas if l.strip() and not l.lstrip().startswith('--'))


def verificar(tmp, armar):
    errores = []

    # 1. Copias de los scripts y ejecución sobre una base vacía, todo en la carpeta temporal
    for s in SCRIPTS + [CONSULTAS]:
        if (AQUI / s).exists():
            shutil.copy2(AQUI / s, tmp / s)
    print(f'Trabajando sobre copias en: {tmp}')
    db = sqlite3.connect(tmp / 'verificacion.db')
    for s in SCRIPTS:
        try:
            db.executescript(leer(tmp / s))
        except sqlite3.Error as e:
            print(f'ERROR al ejecutar {s}: {e}')
            db.close()
            return False
    db.commit()
    print(f'Scripts ejecutados sin errores sobre una base vacía: {", ".join(SCRIPTS)}')
    print(f'Claves foráneas activas: {db.execute("PRAGMA foreign_keys").fetchone()[0] == 1}')
    problemas_fk = db.execute('PRAGMA foreign_key_check').fetchall()
    print(f'Referencias rotas (foreign_key_check): {len(problemas_fk)}')
    if problemas_fk:
        errores.append('foreign_key_check encontró referencias rotas')

    # 2. Registros por tabla
    print('\nRegistros por tabla:')
    for t in TABLAS:
        n = db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
        marca = 'ok' if n >= 5 else 'MENOS DE 5'
        print(f'  {t:20} {n:3}  {marca}')
        if n < 5:
            errores.append(f'{t} tiene {n} registros')

    # 3. Casos inválidos (cada uno dentro de un punto de guardado que se deshace)
    print('\nCasos inválidos:')
    for nombre, sql in INVALIDOS:
        db.execute('SAVEPOINT prueba')
        try:
            db.execute(sql)
            print(f'  NO RECHAZADO  {nombre}')
            errores.append(f'no se rechazó: {nombre}')
        except sqlite3.Error as e:
            print(f'  rechazado     {nombre}: {e}')
        db.execute('ROLLBACK TO prueba')
        db.execute('RELEASE prueba')

    # 3b. Consultas de la Fase IV: se ejecutan una por una y ninguna puede dar vacío
    if (tmp / CONSULTAS).exists():
        print('\nConsultas de la Fase IV:')
        texto = leer(tmp / CONSULTAS)
        for sentencia in texto.split(';'):
            if 'SELECT' not in sentencia:
                continue
            titulo = re.search(r'-- (Consulta [^\n]+)', sentencia)
            titulo = titulo.group(1) if titulo else sentencia.strip()[:40]
            try:
                filas = db.execute(sentencia).fetchall()
            except sqlite3.Error as e:
                print(f'  ERROR         {titulo}: {e}')
                errores.append(f'error en {titulo}')
                continue
            marca = 'ok' if filas else 'VACÍA'
            print(f'  {len(filas):3} filas  {marca:5}  {titulo}')
            if not filas:
                errores.append(f'resultado vacío: {titulo}')
    db.close()

    # 4. Código del informe idéntico al de los scripts (el informe solo se lee)
    print('\nCódigo SQL del informe:')
    for s, md in INFORMES.items():
        ruta_md = PROTO / md
        if not ruta_md.exists():
            print(f'  {md} todavía no existe')
            continue
        bloques = re.findall(r'```sql\n(.*?)```', leer(ruta_md), re.S)
        en_informe = sin_comentarios('\n'.join(bloques))
        if sin_comentarios(leer(tmp / s)) in en_informe:
            print(f'  {s}: idéntico en {md}')
        else:
            print(f'  {s}: NO coincide con {md}')
            errores.append(f'{s} no coincide con {md}')

    # 5. Script de respaldo: se arma en la carpeta temporal y se compara con el entregable
    partes = [leer(tmp / s).rstrip() + '\n' for s in SCRIPTS]
    if (tmp / CONSULTAS).exists():
        partes.append(leer(tmp / CONSULTAS).rstrip() + '\n')
    armado = tmp / 'tp3-gmao.sql'
    armado.write_text('\n'.join(partes), encoding='utf-8')
    destino = RAIZ / 'd_presentacion' / 'tp3-gmao.sql'
    al_dia = destino.exists() and leer(destino) == leer(armado)
    estado = 'al día' if al_dia else 'DESACTUALIZADO respecto de los scripts'
    print(f'\nEntregable {destino.relative_to(RAIZ)}: {estado}')
    if armar and not errores and not al_dia:
        shutil.copy2(armado, destino)
        print('  Reemplazado por la versión armada (se pidió --armar).')
    elif not al_dia:
        print('  No se modificó. Para actualizarlo: python verificar.py --armar')

    if errores:
        print('\nVERIFICACIÓN CON ERRORES:')
        for e in errores:
            print('  -', e)
        return False
    print('\nVerificación completa: sin errores.')
    return True


def main():
    armar = '--armar' in sys.argv
    with tempfile.TemporaryDirectory(prefix='tp3-verificacion-') as tmp:
        ok = verificar(Path(tmp), armar)
    print('Carpeta temporal borrada.')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
