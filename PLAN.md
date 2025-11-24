# PLAN — MACROFOR (Entwicklung nach PDF‑Spezifikation)

Dieses Dokument beschreibt einen konkreten, prüfbaren Plan zur Entwicklung des Python‑Moduls `macrofor`, das Fortran‑Code aus Python generiert und dabei exakt die Schnittstellen und Verhaltensweisen implementiert, wie sie in `RT-0119-ocr.pdf` beschrieben sind.

**Wichtig:** Der erste, notwendige Schritt ist das präzise Extrahieren und Verifizieren aller API‑Details aus `RT-0119-ocr.pdf`. Alle nachfolgenden Implementationsschritte basieren auf dieser geprüften API‑Spec.

## 1. Kurzüberblick
- **Ziel:** Ein Python‑Paket `macrofor`, das die im PDF dokumentierten DSL‑Primitiven, Makros und API‑Signaturen exakt bereitstellt und daraus syntaktisch korrekten Fortran‑Code erzeugt.
- **Anforderungen aus dem PDF:** (werden in Schritt 2 formalisiert) — Signaturen, Kontext‑Manager/Decorator‑Semantik, Makro‑Semantik, erwartetes Codeformat.

## 2. Schritt 1 — Schnittstellen aus PDF extrahieren (Deliverable)
- **Aufgabe:** Das PDF (`RT-0119-ocr.pdf`) vollständig lesen und
  - alle API‑Funktionen, Klassen, Dekoratoren und DSL‑Konstrukte auflisten,
  - Signaturen, optionale Parameter, Rückgabewerte und Fehlerspezifikationen dokumentieren,
  - Beispielsnippets aus dem PDF 1:1 übernehmen und als Validierungsbeispiele speichern.
- **Ergebnis:** `docs/API_SPEC.md` mit einer maschinenlesbaren API‑Spec (Signaturen, Beispiele, Randfälle).

## 3. Schritt 2 — API‑Spec Review (Deliverable)
- **Aufgabe:** Die erzeugte `docs/API_SPEC.md` dem Projektverantwortlichen (Dir) zur Durchsicht vorlegen.
- **Ziel:** Abnahme oder Korrekturen festhalten, damit Implementierung exakt der gewünschten Semantik folgt.

## 4. Schritt 3 — Projekt‑Scaffold (Deliverable)
- **Aufgabe:** Basisstruktur anlegen:
  - `macrofor/` (Paket)
  - `macrofor/ast.py` (AST‑Knoten)
  - `macrofor/api.py` (DSL/Frontend)
  - `macrofor/codegen.py` (Formatter/Generator)
  - `examples/` (PDF‑Beispiele als Reproducer)
  - `tests/` (Unit & Integration)
  - `pyproject.toml` (build system + deps)
- **Ergebnis:** Minimal funktionsfähiges Paket mit `import macrofor` und leerer Test‑CI.

## 5. Schritt 4 — AST & Kernrepräsentation (Deliverable)
- **Aufgabe:** AST‑Knoten implementieren, die exakt die in der API‑Spec geforderten Konstrukte abbilden:
  - Module, Program, Subroutine, Function
  - Declarations (implicit/explicit), Typen
  - Statements: Assignment, If, Do/Loop, Call, Return
  - Makro/Template‑Nodes falls im PDF beschrieben
- **Designregeln:** Knoten sollten einen einfachen Visitor‑/Transformer‑API unterstützen; Knoten‑Konstruktoren spiegeln API‑Signaturen.

## 6. Schritt 5 — DSL/Frontend implementieren (Deliverable)
- **Aufgabe:** Nutzernahe Python‑API um die AST‑Knoten herum bauen, inklusive:
  - Context Manager und Decorators genau wie in der PDF‑Spezifikation beschrieben,
  - Hilfsfunktionen zur Erzeugung von Variablen/Arrays/Typen,
  - Mapping von DSL‑Aufrufen auf AST‑Knoten (1:1 zur API_SPEC).
- **Beispiel:** Wenn das PDF `@fortran.subroutine(name, args=...)` beschreibt, muss dieser Decorator genau diese Parameter und Randbedingungen unterstützen.

## 7. Schritt 6 — Codegen / Formatter (Deliverable)
- **Aufgabe:** AST in Fortran‑Quelltext umwandeln, unter Berücksichtigung aller in der API‑Spec geforderten Formatregeln:
  - Freiform vs feste Form, Zeilenlänge, Kontinuationskonventionen,
  - Deklarationen und Interface‑Blöcke wie im PDF gefordert,
  - Optionale Stil‑Flags (z. B. uppercase/nopadding) falls gefordert.
- **Ergebnis:** `macrofor.codegen.generate(ast, style=...) -> str` mit Tests, die PDF‑Beispiele reproduzieren.

## 8. Schritt 7 — Makros & Template‑Mechanik (Deliverable)
- **Aufgabe:** Implementiere die in der PDF beschriebenen Makromechanismen:
  - Parameterbindung und Scoping
  - Expandierbarkeit/Ad-hoc‑Erweiterungen
  - Fehlerbehandlung bei falscher Nutzung

## 9. Schritt 8 — Tests & Validierung (Deliverable)
- **Aufgabe:**
  - Unit‑Tests für jede API‑Funktion und AST‑Node.
  - Regressions‑Tests: Jedes PDF‑Beispiel wird automatisch generiert und mit einem erwarteten Fortran‑Output verglichen.
  - Optional: Kompilationstest mit `gfortran` in CI, um Syntaxfehler aufzudecken.

## 10. Schritt 9 — Dokumentation & Beispiele (Deliverable)
- **Aufgabe:**
  - `README.md` Quickstart mit den PDF‑Beispielen.
  - `docs/API_SPEC.md` (aus Schritt 1) plus `USAGE.md` mit Tutorials.

## 11. Schritt 10 — Packaging & CI (Deliverable)
- **Aufgabe:** `pyproject.toml` fertigstellen, `pytest`‑Workflow und Linting in GitHub Actions, Release‑Notes und Versioning.

## 12. Risikomanagement & Annahmen
- Wenn das PDF unklare oder mehrdeutige Stellen enthält, ist eine Review mit Dir nötig (Schritt 2).  
- Vollständige Fortran‑Semantik (z. B. komplexe generische Interfaces, C‑Interop Details) kann über den MVP hinausgehen — Priorität sind die in der PDF genannten Kernschnittstellen.

## 13. Nächste Aktionen (konkret, was ich jetzt tun kann)
- 1) Wenn Du zustimmst: Ich starte mit **Schritt 1** (PDF extrahieren) und erstelle `docs/API_SPEC.md`.  
- 2) Danach lege ich das Scaffold an (`pyproject.toml`, Verzeichnisstruktur) und setze Schritt 3 um.

Möchtest Du, dass ich jetzt sofort mit dem Extrahieren der API‑Spezifikation aus `RT-0119-ocr.pdf` beginne? Wenn ja, bestätige bitte, ob ich alle gefundenen Beispiele automatisch als Testfälle anlegen soll.
