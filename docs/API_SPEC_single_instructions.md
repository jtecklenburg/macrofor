# API_SPEC — Single instructions (structured)

Diese Datei wurde automatisch aus `docs/spec_single_instructions.txt` erstellt. Sie listet jede "single instruction" mit einer vorgeschlagenen Signatur, dem Fortran‑Beispiel aus dem PDF/OCR, und einer kurzen TODO‑Anweisung zur Verifikation/Implementierung.

## 1) callf
 **Python API (Vorschlag):** `callf(name: str, list: list[str]) -> str`

## 2) closef
 **Python API (Vorschlag):** `closef(unit: int | str) -> str`

## 3) commentf
 **Python API (Vorschlag):** `commentf(string: str) -> str`

## 4) commonf
 **Python API (Vorschlag):** `commonf(name: str, list: list[str]) -> str`

## 5) continuef
 **Python API (Vorschlag):** `continuef(label: str) -> str`

## 6) declaref
 **Python API (Vorschlag):** `declaref(type: str, list: list[str]) -> str`

## 7) dof
 **Python API (Vorschlag):** `dof(label: str | None, index: str, start, end, step=None) -> str`

## 8) if_then_f / elsef / endiff
  - `if_then_f(condition: str) -> If`
  - `elsef()`
  - `endiff()`
 **Python API (Vorschlag):**
  - `if_then_f(condition: str) -> str`
  - `elsef() -> str`
  - `endiff() -> str`

## 9) equalf
 **Python API (Vorschlag):** `equalf(variable: str, expression: str) -> str`

## 10) formatf
 **Python API (Vorschlag):** `formatf(label: str, list: list[str]) -> str`

## 11) functionf
 **Python API (Vorschlag):** `functionf(type: str, name: str, list: list[str]) -> str`

## 12) gotof / if_goto_f
  - `gotof(label: str) -> Goto`
  - `if_goto_f(condition: str, label: str) -> Goto`
 **Python API (Vorschlag):**
  - `gotof(label: str) -> str`
  - `if_goto_f(condition: str, label: str) -> str`

## 13) openf
 **Python API (Vorschlag):** `openf(unit: int, file: str, status: str = 'unknown') -> str`

## 14) parameterf
 **Python API (Vorschlag):** `parameterf(list: list[str]) -> str`

## 15) programf
 **Python API (Vorschlag):** `programf(name: str) -> str`

## 16) readf
 **Python API (Vorschlag):** `readf(file: str | int, label: str | None, list: list[str]) -> str`

## 17) returnf
 **Python API (Vorschlag):** `returnf() -> str`

## 18) subroutinef
 **Python API (Vorschlag):** `subroutinef(name: str, list: list[str]) -> str`

## 19) writef
 **Python API (Vorschlag):** `writef(file: str | int, label: str | None, list: list[str]) -> str`

---
Nächste Schritte, die ich vorschlage und sofort ausführen kann:

- 1) Ich schreibe `docs/API_SPEC_single_instructions.md` (fertig — diese Datei),
- 2) Ich implementiere Parser‑Helfer, die von der Maple‑Liste‑Form (`[subroutinef, name, list]`) auf die vorgeschlagenen API‑Signaturen abbilden,
- 3) Ich ergänze AST‑Nodes für fehlende Typen (Return, Open, Function wenn nötig) und erweitere `codegen.py`,
- 4) Ich schreibe Unit‑Tests, die für jede Single‑Instruction einen kleinen AST bauen und den erwarteten Fortran‑Output vergleichen.

Willst Du, dass ich Punkt 2–4 jetzt automatisch ausführe (Parser + AST‑Erweiterungen + Tests)? Antworte mit "Ja, implementiere" oder "Nicht jetzt, ich prüfe zuerst". Wenn Du möchtest, kann ich außerdem die erzeugten Spezifikations‑Abschnitte in `docs/API_SPEC_structured.md` zusammenführen (falls Du eine einzelne Datei bevorzugst).
