"""Arma la presentación final y las notas de los oradores.

  python armar.py

Salidas:
  d_presentacion/presentacionTp3.pdf          presentación (diseño B, Ingeniería)
  d_presentacion/exposicion/miniaturas/       una imagen por diapositiva
  d_presentacion/exposicion/nota<Orador>.pdf  notas de cada orador (notas.py)
"""
from pathlib import Path

from generar import a_pdf

AQUI = Path(__file__).parent
PRESENTACION = AQUI.parent.parent / "d_presentacion"
EXPOSICION = PRESENTACION / "exposicion"


def miniaturas(pdf: Path, carpeta: Path) -> int:
    import pymupdf
    carpeta.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(pdf)
    for i, pagina in enumerate(doc, 1):
        pagina.get_pixmap(dpi=48).save(carpeta / f"diapo-{i:02d}.png")
    return len(doc)


if __name__ == "__main__":
    pdf = PRESENTACION / "presentacionTp3.pdf"
    a_pdf(AQUI / "presentacion.html", pdf)
    total = miniaturas(pdf, EXPOSICION / "miniaturas")
    print(f"{pdf} ({total} diapositivas)")
    import notas
    notas.armar(EXPOSICION)
