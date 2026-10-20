-- =====================================================================
-- TP N.º 3 — Base de datos GMAO (SQLite)
-- Paso 5: Creación de tablas (DDL)
-- Grupo N.º 4 — Informática Industrial — UTN FRC
-- =====================================================================

-- Activa la verificación de claves foráneas (SQLite la trae desactivada).
PRAGMA foreign_keys = ON;

-- Permite volver a ejecutar el script desde cero: se borran primero las
-- tablas que dependen de otras.
DROP TABLE IF EXISTS ot_repuestos;
DROP TABLE IF EXISTS fallas;
DROP TABLE IF EXISTS ordenes_trabajo;
DROP TABLE IF EXISTS planes_preventivos;
DROP TABLE IF EXISTS repuestos;
DROP TABLE IF EXISTS tecnicos;
DROP TABLE IF EXISTS maquinas;

-- ---------------------------------------------------------------------
-- Activos de la planta
-- ---------------------------------------------------------------------
CREATE TABLE maquinas (
    id_maquina        INTEGER      PRIMARY KEY,
    codigo            VARCHAR(10)  NOT NULL UNIQUE,
    nombre            VARCHAR(60)  NOT NULL,
    marca             VARCHAR(40),
    modelo            VARCHAR(40),
    sector            VARCHAR(40)  NOT NULL,
    fecha_instalacion DATE,
    horas_operacion   FLOAT,
    criticidad        VARCHAR(5)   NOT NULL
                      CHECK (criticidad IN ('ALTA', 'MEDIA', 'BAJA'))
);

-- ---------------------------------------------------------------------
-- Personal de mantenimiento
-- ---------------------------------------------------------------------
CREATE TABLE tecnicos (
    id_tecnico   INTEGER      PRIMARY KEY,
    legajo       VARCHAR(10)  NOT NULL UNIQUE,
    nombre       VARCHAR(40)  NOT NULL,
    apellido     VARCHAR(40)  NOT NULL,
    especialidad VARCHAR(20)  NOT NULL,
    turno        VARCHAR(10)  NOT NULL
                 CHECK (turno IN ('MAÑANA', 'TARDE', 'NOCHE')),
    telefono     VARCHAR(20)
);

-- ---------------------------------------------------------------------
-- Catálogo y stock de repuestos
-- ---------------------------------------------------------------------
CREATE TABLE repuestos (
    id_repuesto    INTEGER       PRIMARY KEY,
    codigo         VARCHAR(15)   NOT NULL UNIQUE,
    descripcion    VARCHAR(100)  NOT NULL,
    marca          VARCHAR(40),
    stock_actual   INTEGER       NOT NULL CHECK (stock_actual >= 0),
    stock_minimo   INTEGER       NOT NULL CHECK (stock_minimo >= 0),
    costo_unitario FLOAT
);

-- ---------------------------------------------------------------------
-- Planes de mantenimiento preventivo (origen de las OT preventivas)
-- ---------------------------------------------------------------------
CREATE TABLE planes_preventivos (
    id_plan             INTEGER       PRIMARY KEY,
    codigo              VARCHAR(15)   NOT NULL UNIQUE,
    id_maquina          INTEGER       NOT NULL,
    tarea               VARCHAR(200)  NOT NULL,
    frecuencia          INTEGER       NOT NULL CHECK (frecuencia > 0),
    unidad_frecuencia   VARCHAR(5)    NOT NULL
                        CHECK (unidad_frecuencia IN ('DIAS', 'HORAS')),
    especialidad        VARCHAR(20)   NOT NULL,
    duracion_estimada_h FLOAT,
    FOREIGN KEY (id_maquina) REFERENCES maquinas (id_maquina)
);

-- ---------------------------------------------------------------------
-- Órdenes de trabajo (correctivas y preventivas)
-- ---------------------------------------------------------------------
CREATE TABLE ordenes_trabajo (
    id_ot         INTEGER       PRIMARY KEY,
    nro_ot        VARCHAR(15)   NOT NULL UNIQUE,
    tipo          VARCHAR(12)   NOT NULL
                  CHECK (tipo IN ('CORRECTIVA', 'PREVENTIVA')),
    id_maquina    INTEGER       NOT NULL,
    id_plan       INTEGER,
    id_tecnico    INTEGER       NOT NULL,
    fecha_emision DATETIME      NOT NULL,
    fecha_cierre  DATETIME,
    estado        VARCHAR(10)   NOT NULL
                  CHECK (estado IN ('PENDIENTE', 'EN CURSO', 'CERRADA')),
    tarea         VARCHAR(200)  NOT NULL,
    horas_hombre  FLOAT,
    -- La preventiva nace de un plan; la correctiva no tiene plan.
    CHECK ((tipo = 'PREVENTIVA' AND id_plan IS NOT NULL)
        OR (tipo = 'CORRECTIVA' AND id_plan IS NULL)),
    FOREIGN KEY (id_maquina) REFERENCES maquinas (id_maquina),
    FOREIGN KEY (id_plan)    REFERENCES planes_preventivos (id_plan),
    FOREIGN KEY (id_tecnico) REFERENCES tecnicos (id_tecnico)
);

-- ---------------------------------------------------------------------
-- Historial de fallas (origen de las OT correctivas)
-- ---------------------------------------------------------------------
CREATE TABLE fallas (
    id_falla     INTEGER       PRIMARY KEY,
    id_maquina   INTEGER       NOT NULL,
    id_ot        INTEGER,
    fecha_hora   DATETIME      NOT NULL,
    descripcion  VARCHAR(200)  NOT NULL,
    tipo_falla   VARCHAR(15)   NOT NULL,
    severidad    VARCHAR(5)    NOT NULL
                 CHECK (severidad IN ('ALTA', 'MEDIA', 'BAJA')),
    horas_parada FLOAT,
    FOREIGN KEY (id_maquina) REFERENCES maquinas (id_maquina),
    FOREIGN KEY (id_ot)      REFERENCES ordenes_trabajo (id_ot)
);

-- ---------------------------------------------------------------------
-- Repuestos consumidos por orden de trabajo (relación N:M)
-- ---------------------------------------------------------------------
CREATE TABLE ot_repuestos (
    id_ot       INTEGER  NOT NULL,
    id_repuesto INTEGER  NOT NULL,
    cantidad    INTEGER  NOT NULL CHECK (cantidad > 0),
    PRIMARY KEY (id_ot, id_repuesto),
    FOREIGN KEY (id_ot)       REFERENCES ordenes_trabajo (id_ot),
    FOREIGN KEY (id_repuesto) REFERENCES repuestos (id_repuesto)
);

-- ---------------------------------------------------------------------
-- Reglas entre tablas (un CHECK no puede consultar otra tabla)
-- ---------------------------------------------------------------------

-- Una OT preventiva tiene que ser de la misma máquina que su plan.
CREATE TRIGGER trg_ot_preventiva_ins
BEFORE INSERT ON ordenes_trabajo
WHEN NEW.id_plan IS NOT NULL
 AND NEW.id_maquina <> (SELECT id_maquina FROM planes_preventivos
                        WHERE id_plan = NEW.id_plan)
BEGIN
    SELECT RAISE(ABORT,
        'La OT preventiva debe ser de la misma maquina que su plan');
END;

-- Al modificar una OT se vuelve a controlar su plan y las fallas que atiende.
CREATE TRIGGER trg_ot_upd
BEFORE UPDATE OF tipo, id_maquina, id_plan ON ordenes_trabajo
WHEN (NEW.id_plan IS NOT NULL
      AND NEW.id_maquina <> (SELECT id_maquina FROM planes_preventivos
                             WHERE id_plan = NEW.id_plan))
  OR (NEW.tipo = 'PREVENTIVA'
      AND EXISTS (SELECT 1 FROM fallas WHERE id_ot = NEW.id_ot))
  OR EXISTS (SELECT 1 FROM fallas
             WHERE id_ot = NEW.id_ot AND id_maquina <> NEW.id_maquina)
BEGIN
    SELECT RAISE(ABORT,
        'Cambio incoherente con el plan o las fallas de la OT');
END;

-- Una falla solo se asigna a una OT correctiva de la misma máquina.
CREATE TRIGGER trg_falla_ins
BEFORE INSERT ON fallas
WHEN NEW.id_ot IS NOT NULL
 AND ((SELECT tipo FROM ordenes_trabajo
       WHERE id_ot = NEW.id_ot) <> 'CORRECTIVA'
   OR (SELECT id_maquina FROM ordenes_trabajo
       WHERE id_ot = NEW.id_ot) <> NEW.id_maquina)
BEGIN
    SELECT RAISE(ABORT,
        'La falla solo se asigna a una OT correctiva de la misma maquina');
END;

CREATE TRIGGER trg_falla_upd
BEFORE UPDATE OF id_ot, id_maquina ON fallas
WHEN NEW.id_ot IS NOT NULL
 AND ((SELECT tipo FROM ordenes_trabajo
       WHERE id_ot = NEW.id_ot) <> 'CORRECTIVA'
   OR (SELECT id_maquina FROM ordenes_trabajo
       WHERE id_ot = NEW.id_ot) <> NEW.id_maquina)
BEGIN
    SELECT RAISE(ABORT,
        'La falla solo se asigna a una OT correctiva de la misma maquina');
END;
