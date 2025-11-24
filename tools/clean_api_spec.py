"""Lightweight cleaner for docs/API_SPEC.md to reduce obvious OCR artifacts.

This performs a few heuristics: fix common OCR spacing issues around colons,
remove repeated punctuation, normalize unicode quotes and multiple spaces.
"""
import re
import sys
from pathlib import Path


def clean_text(s: str) -> str:
    s = s.replace('\r\n', '\n')
    # Fix 'F ortran' -> 'Fortran', 'MACRO FORT' -> 'MACROFORT'
    s = re.sub(r'F\s?ortran', 'Fortran', s, flags=re.IGNORECASE)
    s = re.sub(r'MACRO\s?FORT', 'MACROFORT', s)
    # Remove repeated punctuation
    s = re.sub(r'([:\-\.,])\1{1,}', r'\1', s)
    # Fix spaced colons
    s = re.sub(r'\s+:\s+', ': ', s)
    # Normalize multiple spaces
    s = re.sub(r' {2,}', ' ', s)
    # Normalize unicode quotes
    s = s.replace('“', '"').replace('”', '"').replace('’', "'")
    return s


def main(argv):
    if len(argv) != 2:
        print('Usage: python tools\\clean_api_spec.py <path-to-API_SPEC.md>')
        return 2
    p = Path(argv[1])
    if not p.exists():
        print('File not found:', p)
        return 2
    txt = p.read_text(encoding='utf-8')
    cleaned = clean_text(txt)
    p.write_text(cleaned, encoding='utf-8')
    print('Cleaned', p)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
