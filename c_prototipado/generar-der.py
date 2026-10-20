"""Genera el diagrama entidad-relación (DER) del modelo GMAO como SVG.

Uso: python generar-der.py assets/fase2-planificacion_01.svg
"""
import sys

out = sys.argv[1]
W, HDR, ROW = 290, 32, 24
C = {'p': '#1F3A5F', 's': '#2E5A88', 'l': '#A7B4C2', 't': '#222222', 'n': '#666666', 'f': '#F3F5F8'}
F = "font-family='Liberation Sans, Arial, sans-serif'"
X1, X2, X3 = 10, 390, 770  # columnas

T = {
    'fallas': (X1, 10, [('PK', 'id_falla', 'INTEGER'), ('FK', 'id_maquina', 'INTEGER'), ('FK', 'id_ot', 'INTEGER'),
                        ('', 'fecha_hora', 'DATETIME'), ('', 'descripcion', 'VARCHAR(200)'), ('', 'tipo_falla', 'VARCHAR(15)'),
                        ('', 'severidad', 'VARCHAR(5)'), ('', 'horas_parada', 'FLOAT')]),
    'maquinas': (X1, 300, [('PK', 'id_maquina', 'INTEGER'), ('UK', 'codigo', 'VARCHAR(10)'), ('', 'nombre', 'VARCHAR(60)'),
                           ('', 'marca', 'VARCHAR(40)'), ('', 'modelo', 'VARCHAR(40)'), ('', 'sector', 'VARCHAR(40)'),
                           ('', 'fecha_instalacion', 'DATE'), ('', 'horas_operacion', 'FLOAT'), ('', 'criticidad', 'VARCHAR(5)')]),
    'planes_preventivos': (X1, 614, [('PK', 'id_plan', 'INTEGER'), ('UK', 'codigo', 'VARCHAR(15)'), ('FK', 'id_maquina', 'INTEGER'),
                                     ('', 'tarea', 'VARCHAR(200)'), ('', 'frecuencia', 'INTEGER'), ('', 'unidad_frecuencia', 'VARCHAR(5)'),
                                     ('', 'especialidad', 'VARCHAR(20)'), ('', 'duracion_estimada_h', 'FLOAT')]),
    'ordenes_trabajo': (X2, 200, [('PK', 'id_ot', 'INTEGER'), ('UK', 'nro_ot', 'VARCHAR(15)'), ('', 'tipo', 'VARCHAR(12)'),
                                  ('FK', 'id_maquina', 'INTEGER'), ('FK', 'id_plan', 'INTEGER'), ('FK', 'id_tecnico', 'INTEGER'),
                                  ('', 'fecha_emision', 'DATETIME'), ('', 'fecha_cierre', 'DATETIME'), ('', 'estado', 'VARCHAR(10)'),
                                  ('', 'tarea', 'VARCHAR(200)'), ('', 'horas_hombre', 'FLOAT')]),
    'ot_repuestos': (X2, 562, [('PK, FK', 'id_ot', 'INTEGER'), ('PK, FK', 'id_repuesto', 'INTEGER'), ('', 'cantidad', 'INTEGER')]),
    'tecnicos': (X3, 320, [('PK', 'id_tecnico', 'INTEGER'), ('UK', 'legajo', 'VARCHAR(10)'), ('', 'nombre', 'VARCHAR(40)'),
                           ('', 'apellido', 'VARCHAR(40)'), ('', 'especialidad', 'VARCHAR(20)'), ('', 'turno', 'VARCHAR(10)'),
                           ('', 'telefono', 'VARCHAR(20)')]),
    'repuestos': (X3, 586, [('PK', 'id_repuesto', 'INTEGER'), ('UK', 'codigo', 'VARCHAR(15)'), ('', 'descripcion', 'VARCHAR(100)'),
                            ('', 'marca', 'VARCHAR(40)'), ('', 'stock_actual', 'INTEGER'), ('', 'stock_minimo', 'INTEGER'),
                            ('', 'costo_unitario', 'FLOAT')]),
}


def fila(tabla, campo):
    """Coordenada y del centro de la fila de un campo."""
    x, y, campos = T[tabla]
    i = [c[1] for c in campos].index(campo)
    return y + HDR + ROW * i + 12


def alto(tabla):
    return HDR + ROW * len(T[tabla][2]) + 6


s = []
for name, (x, y, fields) in T.items():
    h = alto(name)
    s.append(f"<rect x='{x}' y='{y}' width='{W}' height='{h}' rx='4' fill='#FFFFFF' stroke='{C['s']}' stroke-width='1.5'/>")
    s.append(f"<path d='M{x} {y + HDR} V{y + 4} Q{x} {y} {x + 4} {y} H{x + W - 4} Q{x + W} {y} {x + W} {y + 4} V{y + HDR} Z' fill='{C['p']}'/>")
    s.append(f"<text x='{x + W / 2}' y='{y + 21}' text-anchor='middle' {F} font-size='16' font-weight='bold' fill='#FFFFFF'>{name}</text>")
    for i, (k, n, t) in enumerate(fields):
        ry = y + HDR + ROW * i
        if 'PK' in k:
            s.append(f"<rect x='{x + 1}' y='{ry}' width='{W - 2}' height='{ROW}' fill='{C['f']}'/>")
        cy = ry + 17
        col = C['p'] if 'PK' in k else (C['s'] if k else C['n'])
        s.append(f"<text x='{x + 8}' y='{cy}' {F} font-size='12' font-weight='bold' fill='{col}'>{k}</text>")
        bold = " font-weight='bold'" if 'PK' in k else ''
        s.append(f"<text x='{x + 62}' y='{cy}' {F} font-size='15'{bold} fill='{C['t']}'>{n}</text>")
        s.append(f"<text x='{x + W - 8}' y='{cy}' text-anchor='end' font-family='Liberation Mono, Consolas, monospace' font-size='12.5' fill='{C['n']}'>{t}</text>")

L = C['s']


def line(pts):
    d = 'M' + ' L'.join(f'{a} {b}' for a, b in pts)
    s.append(f"<path d='{d}' fill='none' stroke='{L}' stroke-width='1.6'/>")


def end(x, y, dx, dy, kind):
    """Extremo de una relación en notación pata de gallo; (dx, dy) apunta hacia afuera de la tabla."""
    px, py = -dy, dx

    def at(t):
        return x + dx * t, y + dy * t

    def bar(t):
        a, b = at(t)
        s.append(f"<line x1='{a + px * 8}' y1='{b + py * 8}' x2='{a - px * 8}' y2='{b - py * 8}' stroke='{L}' stroke-width='1.6'/>")

    def circ(t):
        a, b = at(t)
        s.append(f"<circle cx='{a}' cy='{b}' r='5' fill='#FFFFFF' stroke='{L}' stroke-width='1.6'/>")

    if kind == 'one':
        bar(7); bar(13)
    elif kind == 'zero_one':
        bar(7); circ(19)
    elif kind == 'many':
        a, b = at(14)
        for sgn in (1, 0, -1):
            s.append(f"<line x1='{a}' y1='{b}' x2='{x + px * 9 * sgn}' y2='{y + py * 9 * sgn}' stroke='{L}' stroke-width='1.6'/>")
        circ(21)


R1, L2, R2, L3 = X1 + W, X2, X2 + W, X3  # bordes derecho/izquierdo de cada columna

# maquinas 1 — N fallas (vertical, columna 1)
line([(80, 300), (80, 10 + alto('fallas'))]); end(80, 300, 0, -1, 'one'); end(80, 10 + alto('fallas'), 0, 1, 'many')
# maquinas 1 — N planes_preventivos (vertical, columna 1)
line([(80, 300 + alto('maquinas')), (80, 614)]); end(80, 300 + alto('maquinas'), 0, 1, 'one'); end(80, 614, 0, -1, 'many')
# ordenes_trabajo 0..1 — N fallas (FK fallas.id_ot)
y1, y2 = fila('fallas', 'id_ot'), fila('ordenes_trabajo', 'id_ot')
line([(R1, y1), (R1 + 20, y1), (R1 + 20, y2), (L2, y2)]); end(R1, y1, 1, 0, 'many'); end(L2, y2, -1, 0, 'zero_one')
# maquinas 1 — N ordenes_trabajo (FK ordenes_trabajo.id_maquina)
y1, y2 = fila('maquinas', 'id_maquina'), fila('ordenes_trabajo', 'id_maquina')
line([(R1, y1), (R1 + 45, y1), (R1 + 45, y2), (L2, y2)]); end(R1, y1, 1, 0, 'one'); end(L2, y2, -1, 0, 'many')
# planes_preventivos 0..1 — N ordenes_trabajo (FK ordenes_trabajo.id_plan)
y1, y2 = fila('planes_preventivos', 'id_plan'), fila('ordenes_trabajo', 'id_plan')
line([(R1, y1), (R1 + 70, y1), (R1 + 70, y2), (L2, y2)]); end(R1, y1, 1, 0, 'zero_one'); end(L2, y2, -1, 0, 'many')
# tecnicos 1 — N ordenes_trabajo (FK ordenes_trabajo.id_tecnico)
y = fila('ordenes_trabajo', 'id_tecnico')
line([(R2, y), (L3, y)]); end(L3, y, -1, 0, 'one'); end(R2, y, 1, 0, 'many')
# ordenes_trabajo 1 — N ot_repuestos (vertical, columna 2)
xm = X2 + W / 2
line([(xm, 200 + alto('ordenes_trabajo')), (xm, 562)]); end(xm, 200 + alto('ordenes_trabajo'), 0, 1, 'one'); end(xm, 562, 0, -1, 'many')
# repuestos 1 — N ot_repuestos (FK ot_repuestos.id_repuesto)
y = fila('ot_repuestos', 'id_repuesto')
line([(R2, y), (L3, y)]); end(L3, y, -1, 0, 'one'); end(R2, y, 1, 0, 'many')

ALTO = 614 + alto('planes_preventivos') + 10
svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1070 {ALTO}' width='1070' height='{ALTO}'>\n"
       f"<rect width='1070' height='{ALTO}' fill='#FFFFFF'/>\n" + '\n'.join(s) + "\n</svg>\n")
open(out, 'w', encoding='utf-8').write(svg)
