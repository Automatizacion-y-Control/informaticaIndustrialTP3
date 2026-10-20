"""Prueba del modelo GMAO de la Fase II: crea las tablas en memoria, carga casos validos e invalidos
y verifica que la base acepte o rechace cada uno. Uso: python prueba-modelo.py
"""
import sqlite3

db = sqlite3.connect(':memory:')
db.execute('PRAGMA foreign_keys = ON')
db.executescript('''
CREATE TABLE maquinas (
  id_maquina INTEGER PRIMARY KEY,
  codigo VARCHAR(10) NOT NULL UNIQUE,
  nombre VARCHAR(60) NOT NULL,
  marca VARCHAR(40), modelo VARCHAR(40),
  sector VARCHAR(40) NOT NULL,
  fecha_instalacion DATE,
  horas_operacion FLOAT,
  criticidad VARCHAR(5) NOT NULL CHECK (criticidad IN ('ALTA','MEDIA','BAJA')));
CREATE TABLE tecnicos (
  id_tecnico INTEGER PRIMARY KEY,
  legajo VARCHAR(10) NOT NULL UNIQUE,
  nombre VARCHAR(40) NOT NULL, apellido VARCHAR(40) NOT NULL,
  especialidad VARCHAR(20) NOT NULL,
  turno VARCHAR(10) NOT NULL CHECK (turno IN ('MAÑANA','TARDE','NOCHE')),
  telefono VARCHAR(20));
CREATE TABLE planes_preventivos (
  id_plan INTEGER PRIMARY KEY,
  codigo VARCHAR(15) NOT NULL UNIQUE,
  id_maquina INTEGER NOT NULL REFERENCES maquinas(id_maquina),
  tarea VARCHAR(200) NOT NULL,
  frecuencia INTEGER NOT NULL CHECK (frecuencia > 0),
  unidad_frecuencia VARCHAR(5) NOT NULL CHECK (unidad_frecuencia IN ('DIAS','HORAS')),
  especialidad VARCHAR(20) NOT NULL,
  duracion_estimada_h FLOAT);
CREATE TABLE ordenes_trabajo (
  id_ot INTEGER PRIMARY KEY,
  nro_ot VARCHAR(15) NOT NULL UNIQUE,
  tipo VARCHAR(12) NOT NULL CHECK (tipo IN ('CORRECTIVA','PREVENTIVA')),
  id_maquina INTEGER NOT NULL REFERENCES maquinas(id_maquina),
  id_plan INTEGER REFERENCES planes_preventivos(id_plan),
  id_tecnico INTEGER NOT NULL REFERENCES tecnicos(id_tecnico),
  fecha_emision DATETIME NOT NULL,
  fecha_cierre DATETIME,
  estado VARCHAR(10) NOT NULL CHECK (estado IN ('PENDIENTE','EN CURSO','CERRADA')),
  tarea VARCHAR(200) NOT NULL,
  horas_hombre FLOAT,
  CHECK ((tipo = 'PREVENTIVA' AND id_plan IS NOT NULL) OR (tipo = 'CORRECTIVA' AND id_plan IS NULL)));
CREATE TABLE fallas (
  id_falla INTEGER PRIMARY KEY,
  id_maquina INTEGER NOT NULL REFERENCES maquinas(id_maquina),
  id_ot INTEGER REFERENCES ordenes_trabajo(id_ot),
  fecha_hora DATETIME NOT NULL,
  descripcion VARCHAR(200) NOT NULL,
  tipo_falla VARCHAR(15) NOT NULL,
  severidad VARCHAR(5) NOT NULL CHECK (severidad IN ('ALTA','MEDIA','BAJA')),
  horas_parada FLOAT);
CREATE TABLE repuestos (
  id_repuesto INTEGER PRIMARY KEY,
  codigo VARCHAR(15) NOT NULL UNIQUE,
  descripcion VARCHAR(100) NOT NULL,
  marca VARCHAR(40),
  stock_actual INTEGER NOT NULL,
  stock_minimo INTEGER NOT NULL,
  costo_unitario FLOAT);
CREATE TABLE ot_repuestos (
  id_ot INTEGER NOT NULL REFERENCES ordenes_trabajo(id_ot),
  id_repuesto INTEGER NOT NULL REFERENCES repuestos(id_repuesto),
  cantidad INTEGER NOT NULL CHECK (cantidad > 0),
  PRIMARY KEY (id_ot, id_repuesto));
CREATE TRIGGER trg_ot_plan_misma_maquina BEFORE INSERT ON ordenes_trabajo
WHEN NEW.id_plan IS NOT NULL AND NEW.id_maquina <> (SELECT id_maquina FROM planes_preventivos WHERE id_plan = NEW.id_plan)
BEGIN SELECT RAISE(ABORT, 'La OT preventiva debe ser de la misma maquina que su plan'); END;
CREATE TRIGGER trg_falla_ot_correctiva BEFORE INSERT ON fallas
WHEN NEW.id_ot IS NOT NULL AND (
  (SELECT tipo FROM ordenes_trabajo WHERE id_ot = NEW.id_ot) <> 'CORRECTIVA' OR
  (SELECT id_maquina FROM ordenes_trabajo WHERE id_ot = NEW.id_ot) <> NEW.id_maquina)
BEGIN SELECT RAISE(ABORT, 'La falla solo se asigna a una OT correctiva de la misma maquina'); END;
CREATE TRIGGER trg_falla_ot_correctiva_upd BEFORE UPDATE OF id_ot ON fallas
WHEN NEW.id_ot IS NOT NULL AND (
  (SELECT tipo FROM ordenes_trabajo WHERE id_ot = NEW.id_ot) <> 'CORRECTIVA' OR
  (SELECT id_maquina FROM ordenes_trabajo WHERE id_ot = NEW.id_ot) <> NEW.id_maquina)
BEGIN SELECT RAISE(ABORT, 'La falla solo se asigna a una OT correctiva de la misma maquina'); END;
''')

ok = [
    "INSERT INTO maquinas VALUES (1,'TOR-01','Torno CNC','Haas','ST-20','Mecanizado','2021-03-15',12850.5,'ALTA')",
    "INSERT INTO maquinas VALUES (2,'CMP-01','Compresor de tornillo','Atlas Copco','GA 37','Servicios','2019-07-01',30210,'MEDIA')",
    "INSERT INTO tecnicos VALUES (1,'L-1021','Juan','Pérez','MECANICA','MAÑANA','351-555-0101')",
    "INSERT INTO planes_preventivos VALUES (1,'PM-CMP01-ACE',2,'Cambio de aceite y filtro',2000,'HORAS','MECANICA',3.0)",
    # Correctivo: la falla se registra sin OT (pendiente), luego se emite la OT y se vincula.
    "INSERT INTO fallas VALUES (1,1,NULL,'2026-09-02 08:15:00','Rotura de correa del husillo','MECANICA','ALTA',3.5)",
    "INSERT INTO ordenes_trabajo VALUES (1,'OT-2026-0101','CORRECTIVA',1,NULL,1,'2026-09-02 08:40:00',NULL,'EN CURSO','Reemplazo de correa',NULL)",
    "UPDATE fallas SET id_ot = 1 WHERE id_falla = 1",
    # Una segunda falla agrupada en la misma OT, como en SAP.
    "INSERT INTO fallas VALUES (2,1,1,'2026-09-02 08:20:00','Ruido en caja de engranajes','MECANICA','MEDIA',0)",
    # Preventivo: la OT sale del plan.
    "INSERT INTO ordenes_trabajo VALUES (2,'OT-2026-0102','PREVENTIVA',2,1,1,'2026-09-10 07:00:00','2026-09-10 10:00:00','CERRADA','Cambio de aceite y filtro',3.0)",
    "INSERT INTO repuestos VALUES (1,'FIL-AC-1625','Filtro de aceite','Atlas Copco',1,2,45000)",
    "INSERT INTO ot_repuestos VALUES (2,1,1)",
]
mal = [
    ("Preventiva sin plan", "INSERT INTO ordenes_trabajo VALUES (3,'OT-2026-0103','PREVENTIVA',2,NULL,1,'2026-09-11 07:00:00',NULL,'PENDIENTE','x',NULL)"),
    ("Correctiva con plan", "INSERT INTO ordenes_trabajo VALUES (3,'OT-2026-0103','CORRECTIVA',2,1,1,'2026-09-11 07:00:00',NULL,'PENDIENTE','x',NULL)"),
    ("Preventiva de otra maquina que su plan", "INSERT INTO ordenes_trabajo VALUES (3,'OT-2026-0103','PREVENTIVA',1,1,1,'2026-09-11 07:00:00',NULL,'PENDIENTE','x',NULL)"),
    ("Falla asignada a una OT preventiva", "INSERT INTO fallas VALUES (3,2,2,'2026-09-12 10:00:00','x','MECANICA','BAJA',0)"),
    ("Falla reasignada a OT de otra maquina (UPDATE)", "UPDATE fallas SET id_ot = 2 WHERE id_falla = 1"),
    ("FK a maquina inexistente", "INSERT INTO fallas VALUES (3,99,NULL,'2026-09-12 10:00:00','x','MECANICA','BAJA',0)"),
    ("Estado fuera de lista", "INSERT INTO ordenes_trabajo VALUES (3,'OT-2026-0103','CORRECTIVA',1,NULL,1,'2026-09-11',NULL,'ABIERTA','x',NULL)"),
    ("Repuesto repetido en la misma OT", "INSERT INTO ot_repuestos VALUES (2,1,3)"),
    ("Cantidad cero", "INSERT INTO ot_repuestos VALUES (1,1,0)"),
]
for s in ok:
    db.execute(s)
print('Casos validos aceptados: %d/%d' % (len(ok), len(ok)))
fallos = 0
for nombre, s in mal:
    try:
        db.execute(s)
        print('  NO RECHAZADO:', nombre)
        fallos += 1
    except sqlite3.Error as e:
        print('  rechazado -', nombre, '->', e)
print('Casos invalidos rechazados: %d/%d' % (len(mal) - fallos, len(mal)))

print('\nPrueba Paso 9: OT con maquina, origen y tecnico')
for r in db.execute('''
SELECT ot.nro_ot, ot.tipo, m.nombre, COALESCE(f.descripcion, p.tarea) AS origen, t.apellido || ', ' || t.nombre
FROM ordenes_trabajo ot
JOIN maquinas m ON m.id_maquina = ot.id_maquina
JOIN tecnicos t ON t.id_tecnico = ot.id_tecnico
LEFT JOIN fallas f ON f.id_ot = ot.id_ot
LEFT JOIN planes_preventivos p ON p.id_plan = ot.id_plan
ORDER BY ot.nro_ot, f.fecha_hora'''):
    print('  ', r)
print('\nFallas pendientes (sin OT):', db.execute('SELECT COUNT(*) FROM fallas WHERE id_ot IS NULL').fetchone()[0])
