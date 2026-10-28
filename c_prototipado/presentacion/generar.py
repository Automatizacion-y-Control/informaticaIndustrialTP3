"""Genera los PDF de la presentación con Chrome sin interfaz.

Uso:  python generar.py <archivo.html> <salida.pdf> [--png carpeta]
Con --png, además guarda cada página como imagen para revisarla.
"""
import subprocess
import sys
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def a_pdf(html: Path, pdf: Path) -> None:
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--allow-file-access-from-files", "--virtual-time-budget=10000",
                    f"--print-to-pdf={pdf}",
                    html.resolve().as_uri()], check=True, capture_output=True)


def a_png(pdf: Path, carpeta: Path) -> None:
    import pymupdf
    carpeta.mkdir(parents=True, exist_ok=True)
    for i, pagina in enumerate(pymupdf.open(pdf), 1):
        pagina.get_pixmap(dpi=72).save(carpeta / f"{pdf.stem}-{i:02d}.png")


if __name__ == "__main__":
    html, pdf = Path(sys.argv[1]), Path(sys.argv[2]).resolve()
    a_pdf(html, pdf)
    if "--png" in sys.argv:
        a_png(pdf, Path(sys.argv[sys.argv.index("--png") + 1]))
    print(pdf)
