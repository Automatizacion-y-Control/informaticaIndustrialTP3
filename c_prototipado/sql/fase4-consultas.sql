-- =====================================================================
-- TP N.º 3 — Base de datos GMAO (SQLite)
-- Fase IV: Consultas (Pasos 7, 8 y 9)
-- Cada consulta responde a una necesidad del supervisor de planta.
-- =====================================================================

-- ---------------------------------------------------------------------
-- Consulta 7.1 — Fallas entre dos fechas
-- Fallas de severidad ALTA o MEDIA registradas entre el 15/09 y el 10/10.
-- ---------------------------------------------------------------------
SELECT id_falla, fecha_hora, id_maquina, descripcion, tipo_falla,
       severidad, horas_parada
FROM fallas
WHERE fecha_hora BETWEEN '2026-09-15 00:00:00' AND '2026-10-10 23:59:59'
  AND severidad IN ('ALTA', 'MEDIA')
ORDER BY fecha_hora;

-- ---------------------------------------------------------------------
-- Consulta 7.2 — Repuestos con stock crítico
-- Repuestos en el punto de reposición o por debajo. Primero los que
-- más faltan.
-- ---------------------------------------------------------------------
SELECT codigo, descripcion, stock_actual, stock_minimo,
       stock_minimo - stock_actual AS faltante
FROM repuestos
WHERE stock_actual <= stock_minimo
ORDER BY faltante DESC, codigo;

-- ---------------------------------------------------------------------
-- Consulta 7.3 — Órdenes correctivas abiertas
-- Correctivas que no están cerradas, de la más antigua a la más nueva.
-- ---------------------------------------------------------------------
SELECT nro_ot, fecha_emision, id_maquina, id_tecnico, estado, tarea
FROM ordenes_trabajo
WHERE tipo = 'CORRECTIVA'
  AND NOT estado = 'CERRADA'
ORDER BY fecha_emision;

-- ---------------------------------------------------------------------
-- Consulta 8.1 — Fallas por máquina (activo más crítico)
-- Cantidad de fallas y horas de parada acumuladas por máquina.
-- ---------------------------------------------------------------------
SELECT id_maquina,
       COUNT(*)          AS cantidad_fallas,
       SUM(horas_parada) AS horas_parada_total,
       MAX(fecha_hora)   AS ultima_falla
FROM fallas
GROUP BY id_maquina
ORDER BY cantidad_fallas DESC, horas_parada_total DESC;

-- ---------------------------------------------------------------------
-- Consulta 8.2 — Horas-hombre por tipo de mantenimiento
-- Órdenes emitidas y horas-hombre registradas, correctivo vs preventivo.
-- ---------------------------------------------------------------------
SELECT tipo,
       COUNT(*)                    AS cantidad_ot,
       SUM(horas_hombre)           AS horas_hombre_total,
       ROUND(AVG(horas_hombre), 2) AS horas_hombre_promedio,
       MAX(horas_hombre)           AS horas_hombre_maxima
FROM ordenes_trabajo
GROUP BY tipo
ORDER BY horas_hombre_total DESC;

-- ---------------------------------------------------------------------
-- Consulta 9.1 — Órdenes con máquina, falla y técnico
-- Para las correctivas se muestra la falla y para las preventivas, la
-- tarea del plan. Una OT que atiende dos fallas aparece dos veces.
-- ---------------------------------------------------------------------
SELECT ot.nro_ot,
       ot.tipo,
       m.nombre                            AS maquina,
       COALESCE(f.descripcion,
                'Plan ' || p.codigo || ': ' || p.tarea) AS motivo,
       t.apellido || ', ' || t.nombre      AS tecnico,
       ot.estado
FROM ordenes_trabajo AS ot
INNER JOIN maquinas AS m           ON m.id_maquina = ot.id_maquina
INNER JOIN tecnicos AS t           ON t.id_tecnico = ot.id_tecnico
LEFT JOIN fallas AS f              ON f.id_ot = ot.id_ot
LEFT JOIN planes_preventivos AS p  ON p.id_plan = ot.id_plan
ORDER BY ot.nro_ot, f.fecha_hora;

-- ---------------------------------------------------------------------
-- Consulta 9.2 — Repuestos consumidos por orden de trabajo
-- Con la máquina, la cantidad y el costo de cada consumo.
-- ---------------------------------------------------------------------
SELECT ot.nro_ot,
       m.nombre                        AS maquina,
       r.descripcion                   AS repuesto,
       otr.cantidad,
       r.costo_unitario,
       otr.cantidad * r.costo_unitario AS costo_total
FROM ot_repuestos AS otr
INNER JOIN ordenes_trabajo AS ot ON ot.id_ot = otr.id_ot
INNER JOIN maquinas AS m         ON m.id_maquina = ot.id_maquina
INNER JOIN repuestos AS r        ON r.id_repuesto = otr.id_repuesto
ORDER BY ot.nro_ot, r.descripcion;
