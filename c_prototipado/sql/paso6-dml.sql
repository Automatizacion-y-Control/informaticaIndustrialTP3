-- =====================================================================
-- TP N.º 3 — Base de datos GMAO (SQLite)
-- Paso 6: Carga de datos de planta (DML)
-- Datos simulados. Fechas en formato ISO 8601 (AAAA-MM-DD HH:MM:SS).
-- Orden de carga: primero las tablas referenciadas, después las que
-- dependen de ellas.
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- Máquinas
-- ---------------------------------------------------------------------
INSERT INTO maquinas (id_maquina, codigo, nombre, marca, modelo, sector,
                      fecha_instalacion, horas_operacion, criticidad)
VALUES
(1, 'TOR-01', 'Torno CNC', 'Haas', 'ST-20',
    'Mecanizado', '2021-03-15', 12850.5, 'ALTA'),
(2, 'FRE-01', 'Centro de mecanizado vertical', 'Haas', 'VF-2',
    'Mecanizado', '2020-11-02', 15420.0, 'ALTA'),
(3, 'CMP-01', 'Compresor de tornillo', 'Atlas Copco', 'GA 37',
    'Servicios', '2019-07-01', 30210.0, 'MEDIA'),
(4, 'ROB-01', 'Robot de soldadura', 'ABB', 'IRB 2600',
    'Soldadura', '2022-05-20', 9870.0, 'ALTA'),
(5, 'PRE-01', 'Prensa hidráulica', 'Schuler', 'PH 250',
    'Estampado', '2018-02-12', 41200.0, 'MEDIA'),
(6, 'INY-01', 'Inyectora de plástico', 'Engel', 'e-mac 180',
    'Inyección', '2023-01-09', 6150.0, 'BAJA');

-- ---------------------------------------------------------------------
-- Técnicos
-- ---------------------------------------------------------------------
INSERT INTO tecnicos (id_tecnico, legajo, nombre, apellido, especialidad,
                      turno, telefono)
VALUES
(1, 'L-1021', 'Juan',   'Pérez',     'MECANICA',    'MAÑANA', '351-555-0101'),
(2, 'L-1034', 'María',  'González',  'ELECTRICA',   'MAÑANA', '351-555-0102'),
(3, 'L-1047', 'Carlos', 'Rodríguez', 'HIDRAULICA',  'TARDE',  '351-555-0103'),
(4, 'L-1052', 'Lucía',  'Fernández', 'ELECTRONICA', 'TARDE',  '351-555-0104'),
(5, 'L-1068', 'Diego',  'Martínez',  'MECANICA',    'NOCHE',  '351-555-0105');

-- ---------------------------------------------------------------------
-- Repuestos (stock actual y punto de reposición)
-- ---------------------------------------------------------------------
INSERT INTO repuestos (id_repuesto, codigo, descripcion, marca,
                       stock_actual, stock_minimo, costo_unitario)
VALUES
(1, 'COR-5V710', 'Correa de transmisión 5V710', 'Gates',
    2, 2, 38500.0),
(2, 'ROD-6206-2RS', 'Rodamiento rígido de bolas 6206-2RS', 'SKF',
    12, 6, 9800.0),
(3, 'FIL-AC-GA37', 'Filtro de aceite para compresor GA 37', 'Atlas Copco',
    1, 3, 52000.0),
(4, 'ACE-RIF-20L', 'Aceite para compresor de tornillo, 20 L', 'Atlas Copco',
    4, 2, 310000.0),
(5, 'PLA-SMB-IRB', 'Placa de medición serie (SMB) del robot', 'ABB',
    0, 1, 1850000.0),
(6, 'RES-800W', 'Resistencia calefactora de cilindro 800 W', 'Engel',
    3, 2, 74000.0),
(7, 'SEL-CIL-80', 'Kit de sellos para cilindro hidráulico 80', 'Parker',
    2, 2, 126000.0);

-- ---------------------------------------------------------------------
-- Planes preventivos (por calendario: DIAS; por horómetro: HORAS)
-- ---------------------------------------------------------------------
INSERT INTO planes_preventivos (id_plan, codigo, id_maquina, tarea,
                                frecuencia, unidad_frecuencia,
                                especialidad, duracion_estimada_h)
VALUES
(1, 'PM-TOR01-LUB', 1,
    'Lubricación de guías y control de nivel de aceite',
    30, 'DIAS', 'MECANICA', 1.0),
(2, 'PM-TOR01-COR', 1,
    'Inspección y tensado de correas de transmisión',
    500, 'HORAS', 'MECANICA', 1.5),
(3, 'PM-CMP01-ACE', 3,
    'Cambio de aceite y filtro',
    2000, 'HORAS', 'MECANICA', 3.0),
(4, 'PM-ROB01-INS', 4,
    'Inspección de cableado y respaldo de baterías del controlador',
    180, 'DIAS', 'ELECTRONICA', 2.0),
(5, 'PM-PRE01-HID', 5,
    'Control de presión y fugas del circuito hidráulico',
    90, 'DIAS', 'HIDRAULICA', 2.5),
(6, 'PM-FRE01-CON', 2,
    'Limpieza y verificación del cono del husillo',
    250, 'HORAS', 'MECANICA', 1.0);

-- ---------------------------------------------------------------------
-- Órdenes de trabajo
-- Las correctivas no tienen plan (id_plan NULL); las preventivas sí.
-- Las abiertas no tienen fecha de cierre.
-- ---------------------------------------------------------------------
INSERT INTO ordenes_trabajo (id_ot, nro_ot, tipo, id_maquina, id_plan,
                             id_tecnico, fecha_emision, fecha_cierre,
                             estado, tarea, horas_hombre)
VALUES
(1, 'OT-2026-0101', 'CORRECTIVA', 1, NULL, 1,
    '2026-09-02 08:40:00', '2026-09-02 12:20:00', 'CERRADA',
    'Reemplazo de correa de transmisión del husillo', 3.5),
(2, 'OT-2026-0102', 'PREVENTIVA', 3, 3, 5,
    '2026-09-04 07:00:00', '2026-09-04 10:15:00', 'CERRADA',
    'Cambio de aceite y filtro', 3.25),
(3, 'OT-2026-0103', 'CORRECTIVA', 3, NULL, 1,
    '2026-09-05 15:00:00', '2026-09-05 17:30:00', 'CERRADA',
    'Limpieza del enfriador de aceite y prueba del termostato', 2.5),
(4, 'OT-2026-0104', 'CORRECTIVA', 4, NULL, 4,
    '2026-09-10 22:30:00', '2026-09-11 03:00:00', 'CERRADA',
    'Reemplazo de placa SMB y calibración de ejes', 4.5),
(5, 'OT-2026-0105', 'PREVENTIVA', 1, 1, 1,
    '2026-09-15 07:00:00', '2026-09-15 08:00:00', 'CERRADA',
    'Lubricación de guías y control de nivel de aceite', 1.0),
(6, 'OT-2026-0106', 'CORRECTIVA', 1, NULL, 1,
    '2026-09-18 11:00:00', '2026-09-18 13:00:00', 'CERRADA',
    'Balanceo del portaherramientas y control de rodamientos', 2.0),
(7, 'OT-2026-0107', 'CORRECTIVA', 5, NULL, 3,
    '2026-09-23 07:20:00', '2026-09-23 14:00:00', 'CERRADA',
    'Reemplazo de sellos del cilindro y purga del circuito', 6.5),
(8, 'OT-2026-0108', 'PREVENTIVA', 4, 4, 4,
    '2026-09-28 14:00:00', '2026-09-28 16:00:00', 'CERRADA',
    'Inspección de cableado y respaldo de baterías', 2.0),
(9, 'OT-2026-0109', 'CORRECTIVA', 4, NULL, 2,
    '2026-10-01 16:40:00', '2026-10-01 18:00:00', 'CERRADA',
    'Reemplazo de conector de red y prueba de comunicación', 1.25),
(10, 'OT-2026-0110', 'CORRECTIVA', 1, NULL, 5,
    '2026-10-07 09:30:00', NULL, 'EN CURSO',
    'Reemplazo de rodamiento delantero del husillo', 3.0),
(11, 'OT-2026-0111', 'PREVENTIVA', 5, 5, 3,
    '2026-10-14 14:00:00', NULL, 'PENDIENTE',
    'Control de presión y fugas del circuito hidráulico', NULL),
(12, 'OT-2026-0112', 'CORRECTIVA', 2, NULL, 1,
    '2026-10-15 16:00:00', NULL, 'PENDIENTE',
    'Diagnóstico del cambiador de herramientas', NULL),
(13, 'OT-2026-0113', 'PREVENTIVA', 2, 6, 5,
    '2026-10-16 22:00:00', NULL, 'EN CURSO',
    'Limpieza y verificación del cono del husillo', 0.5);

-- ---------------------------------------------------------------------
-- Fallas
-- Las fallas 5 y 6 se atienden en la misma OT (7).
-- La falla 9 todavía no tiene OT: está pendiente (id_ot NULL).
-- ---------------------------------------------------------------------
INSERT INTO fallas (id_falla, id_maquina, id_ot, fecha_hora, descripcion,
                    tipo_falla, severidad, horas_parada)
VALUES
(1, 1, 1, '2026-09-02 08:15:00',
    'Rotura de correa de transmisión del husillo',
    'MECANICA', 'ALTA', 3.5),
(2, 3, 3, '2026-09-05 14:40:00',
    'Sobretemperatura del aceite, corte por 110 °C',
    'MECANICA', 'MEDIA', 1.5),
(3, 4, 4, '2026-09-10 22:05:00',
    'Error de encoder del eje 3, pérdida de posición',
    'ELECTRONICA', 'ALTA', 4.0),
(4, 1, 6, '2026-09-18 10:30:00',
    'Vibración excesiva del husillo a altas RPM',
    'MECANICA', 'MEDIA', 2.0),
(5, 5, 7, '2026-09-23 06:50:00',
    'Pérdida de presión en el circuito principal',
    'HIDRAULICA', 'ALTA', 6.0),
(6, 5, 7, '2026-09-23 07:05:00',
    'Fuga de aceite en sello del cilindro principal',
    'HIDRAULICA', 'MEDIA', 0.0),
(7, 4, 9, '2026-10-01 16:20:00',
    'Falla de comunicación PROFINET con el PLC',
    'ELECTRONICA', 'MEDIA', 1.0),
(8, 1, 10, '2026-10-07 09:10:00',
    'Desgaste de rodamiento delantero del husillo',
    'MECANICA', 'ALTA', 5.0),
(9, 6, NULL, '2026-10-12 11:45:00',
    'Resistencia de calefacción de zona 2 abierta',
    'ELECTRICA', 'BAJA', 0.75),
(10, 2, 12, '2026-10-15 15:30:00',
    'Atasco del cambiador automático de herramientas',
    'MECANICA', 'MEDIA', 1.2);

-- ---------------------------------------------------------------------
-- Repuestos consumidos por OT
-- ---------------------------------------------------------------------
INSERT INTO ot_repuestos (id_ot, id_repuesto, cantidad)
VALUES
(1, 1, 1),
(2, 3, 1),
(2, 4, 1),
(4, 5, 1),
(7, 7, 1),
(10, 2, 2);
