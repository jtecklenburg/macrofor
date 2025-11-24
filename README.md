# macrofor

`macrofor` is a prototype Python package to generate Fortran code from a
Python DSL inspired by the MACROFORT descriptions in `RT-0119-ocr.pdf`.

This repository currently contains scaffolding: AST, DSL facade and a
very small code generator. The development plan and extracted API
specification are in `docs/`.

Next steps: implement AST nodes to exactly match the PDF spec, extend
the DSL and improve code generation/formatting.
