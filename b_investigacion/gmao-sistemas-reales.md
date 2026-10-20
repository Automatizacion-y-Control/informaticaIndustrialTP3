# Cómo modelan el mantenimiento los gestores reales

Investigación para revisar el modelo de la Fase II antes de implementarlo. Se relevaron tres sistemas de uso real: **SAP PM** (módulo de mantenimiento de SAP, el más difundido en la industria), **Odoo Maintenance** (código abierto, se puede leer su modelo de datos) e **IBM Maximo** (gestor de activos empresarial). Las referencias [n] están al final.

## 1. SAP PM

### Correctivo: aviso → orden

- El **aviso** (*notification*) describe el estado de un objeto técnico o informa una avería, y pide al área de mantenimiento que la repare. Es la puerta de entrada del trabajo **no planificado** [1].
- Tipos estándar de aviso [2]:
  - **M1 — Solicitud de mantenimiento:** pedido de trabajo que no es una avería en curso.
  - **M2 — Aviso de avería:** registra la falla con **inicio y fin de la avería**, para medir el tiempo de parada [3].
  - **M3 — Informe de actividad:** documenta un trabajo ya realizado.
- La **orden de mantenimiento** se crea a partir del aviso y sirve para planificar el trabajo en detalle, seguir su avance y cargar y liquidar costos [1].
- **Una orden puede agrupar varios avisos** [1]. Es decir, el vínculo va del aviso hacia la orden (N avisos : 1 orden).
- Cuando el aviso se cierra técnicamente, sus datos pasan al **historial de mantenimiento** del equipo, que se usa para evaluaciones a largo plazo [1].

### Preventivo: plan → orden

- El preventivo no nace de una falla: nace de un **plan de mantenimiento**.
- Cuando el plan vence, el sistema genera automáticamente un **objeto de llamada**: una orden (si el trabajo requiere planificación detallada) o un aviso (si alcanza con una planificación somera, como un recordatorio de inspección) [4].
- Tipos de plan [5][6]:
  - **Por tiempo** (ciclo único): cada N días, semanas o meses.
  - **Por rendimiento** (contador): cuando el contador del equipo alcanza una lectura, por ejemplo cada 100 horas de operación. El contador es un punto de medida del equipo y hay que cargar sus lecturas en forma periódica [6].
  - **Por estrategia:** varios ciclos combinados (por ejemplo, inspección mensual y revisión general anual).
- La **posición de mantenimiento** indica sobre qué equipo se hace el trabajo y con qué prioridad, y la **hoja de ruta** (*task list*) indica qué tareas hay que hacer [4][7].

## 2. Odoo Maintenance (modelo de datos leído del código fuente) [8]

| Modelo | Campos relevantes |
|---|---|
| `maintenance.equipment` | nombre, categoría, ubicación, modelo, n.º de serie (único), fecha de puesta en servicio, costo, equipo de mantenimiento, técnico. Calcula **MTBF**, **MTTR**, fecha de la última falla y fecha estimada de la próxima. |
| `maintenance.request` | asunto, descripción, equipo, **tipo** (`corrective` / `preventive`), **técnico** (uno solo), equipo de mantenimiento, **etapa** (estado), prioridad, fecha de solicitud, fecha programada, **fecha de cierre**, **duración en horas**. |
| Campos de recurrencia en `maintenance.request` | `repeat_interval` (cada cuánto), `repeat_unit` (día, semana, mes, año), `repeat_type` (para siempre / hasta), `repeat_until`. Solo se usan en las preventivas. |
| `maintenance.team` | equipo de mantenimiento con sus integrantes. |
| `maintenance.stage` | etapas del flujo (por defecto: nueva, en curso, reparada, desechada [9]). |

- Odoo **simplifica**: una misma tabla es la solicitud y la orden de trabajo. El tipo distingue correctivo de preventivo, y en el preventivo la periodicidad se guarda en la propia orden [8][10].
- El módulo base no maneja repuestos: eso se resuelve con el módulo de inventario.

## 3. IBM Maximo [11][12]

- **Solicitud de servicio** (*service request*): la carga un usuario y suele ser el primer paso hacia una orden de trabajo.
- **Orden de trabajo**: lleva el tipo de trabajo, la clase de falla y el código de problema; el técnico se guía por un plan de trabajo.
- **Registro PM** (*PM record*): genera las órdenes preventivas en forma periódica.
- **Plan de trabajo** (*job plan*): paquete predefinido de tareas, herramientas, mano de obra y materiales para un tipo de trabajo repetitivo.
- **Códigos de falla**: jerarquía de clase de falla → problema → causa → solución, para analizar causas raíz.
- El correctivo necesita análisis antes de ejecutarse; el preventivo ya viene planificado y en general se ejecuta sin planificación adicional [11].

## 4. Lo que tienen en común

| Concepto | SAP PM | Odoo | Maximo | En nuestro modelo |
|---|---|---|---|---|
| Activo | Equipo / ubicación técnica | `maintenance.equipment` | Activo | `maquinas` |
| Origen del correctivo | Aviso de avería (M2) | Solicitud tipo *corrective* | Solicitud de servicio | `fallas` |
| Origen del preventivo | Plan de mantenimiento (tiempo o contador) | Solicitud *preventive* con recurrencia | Registro PM | **falta** |
| Ejecución | Orden de mantenimiento | La misma solicitud | Orden de trabajo | `ordenes_trabajo` |
| Responsable | Puesto de trabajo / técnico | Técnico (uno) + equipo | Mano de obra | `tecnicos` (uno por OT) |
| Materiales | Componentes de la orden | Módulo de inventario | Materiales del plan / orden | `repuestos` + `ot_repuestos` |
| Indicadores | Historial | MTBF y MTTR por equipo | Códigos de falla | `fallas.fecha_hora` + `horas_parada` |

**Conclusiones para el modelo:**

1. **El correctivo y el preventivo tienen orígenes distintos.** Los tres sistemas separan el pedido o la avería (correctivo) del plan periódico (preventivo). Al modelo le falta la entidad del plan preventivo.
2. **El plan preventivo se define por equipo, con una tarea y una frecuencia**, que puede ser por calendario (días) o por uso (horas de operación).
3. **La OT es la unidad de ejecución:** técnico, fechas de emisión y cierre, estado, horas y materiales consumidos. Sirve para los dos tipos.
4. **El sentido del vínculo falla–OT.** En SAP el aviso apunta a la orden (varios avisos en una orden). El modelo actual hace lo contrario (la OT apunta a la falla). Hay que decidir cuál se usa.
5. **La falla registra inicio y duración de la parada.** Es lo que permite calcular MTTR y MTBF, que es lo que hacen Odoo y SAP con el historial.

## Referencias

Consultadas el 2026-10-19.

1. SAP. *Maintenance Notifications (PM-WOC-MN).* https://help.sap.com/doc/b183ce53118d4308e10000000a174cb4/700_SFIN3E%20006/en-US/238bb6535fe6b74ce10000000a174cb4.html
2. SAP. *Notification Type.* https://help.sap.com/saphelp_470/helpdata/EN/32/543d3854126956e10000009b38f842/content.htm
3. OXMAINT. *SAP PM Notification to Work Order Integration Guide* (proveedor; fuente secundaria). https://oxmaint.com/industries/manufacturing-plant/sap-pm-notification-to-work-order-integration-guide
4. SAP. *Maintenance Plan Category.* https://help.sap.com/saphelp_46C/helpdata/EN/3c/abb1c5413911d1893d0000e8323c4f/content.htm
5. SAP. *Maintenance Strategy.* https://help.sap.com/saphelp_46c/helpdata/en/3c/abaf72413911d1893d0000e8323c4f/content.htm
6. SAP. *Performance-Based Maintenance Plan.* https://help.sap.com/saphelp_46c/helpdata/en/3c/abb1ec413911d1893d0000e8323c4f/content.htm
7. SAP. *Maintenance Call Object.* https://help.sap.com/saphelp_46c/helpdata/en/d2/a7bf76de7f11d1951b00a0c93029cf/content.htm
8. Odoo S.A. *Código fuente del módulo Maintenance, versión 17.0* (`addons/maintenance/models/maintenance.py`). https://github.com/odoo/odoo/blob/17.0/addons/maintenance/models/maintenance.py
9. Cybrosys. *Odoo 16 Enterprise Book: Maintenance requests.* https://www.cybrosys.com/odoo/odoo-books/odoo-book-v16/maintenance/maintenance-request/
10. Odoo. *Maintenance requests* (documentación oficial). https://www.odoo.com/documentation/master/applications/inventory_and_mrp/maintenance/maintenance_requests.html
11. University of Delaware Facilities. *Maximo Work Management Training Guide.* https://web.facilities.udel.edu/docs/Sharepoint/MO/Maximo/NexusMaximoWorkManagementTrainingGuide.pdf
12. Programmed. *NextGen Glossary MAS v1* (glosario de Maximo). https://info.programmed.com.au/hubfs/PFM/PFM%20NextGen/NextGen_Glossary_MAS_v1.pdf
