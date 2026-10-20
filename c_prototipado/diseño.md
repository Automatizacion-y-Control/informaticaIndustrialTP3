# Diseño del documento: Informe TP Nº 3 — GMAO

Hereda el diseño académico de `a_requisitos/diseno-utn.md`, que arma la portada con los datos de la cátedra y del Grupo Nº 4. Los títulos ya traen la numeración de fases y pasos del enunciado («Paso 1 — …»), por eso `numeracion` queda en `false`. El PDF se guarda en `../d_presentacion/`.

```yaml
titulo: Informe técnico
base: diseno-utn
pie: TP Nº 3 — Base de Datos GMAO
salida: tp3-gmao-informe.pdf
fuentes:
  - fase1-investigacion.md
  - fase2-planificacion.md
  - fase3-construccion.md
  - fase4-explotacion.md
  - referencias.md
portada: true
fecha: Octubre de 2026
indice: true
numeracion: false
```
