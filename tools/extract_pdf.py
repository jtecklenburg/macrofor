"""Extract text from a PDF into a text file.

Usage:
    python tools\extract_pdf.py <input-pdf> <output-txt>

Requires: `pypdf` (install with `pip install --user pypdf`).
"""
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except Exception:
    print("pypdf not installed. Install with: python -m pip install --user pypdf")
    raise


def extract(pdf_path: Path, out_path: Path):
    reader = PdfReader(str(pdf_path))
    parts = []
    for p in reader.pages:
        try:
            text = p.extract_text() or ""
        except Exception:
            text = ""
        parts.append(text)
    out_path.write_text("\n\n".join(parts), encoding="utf-8")


def main(argv):
    if len(argv) != 3:
        print("Usage: python tools\\extract_pdf.py <input-pdf> <output-txt>")
        return 2
    inp = Path(argv[1])
    out = Path(argv[2])
    if not inp.exists():
        print(f"Input PDF not found: {inp}")
        return 2
    extract(inp, out)
    print(f"Extracted text to: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
