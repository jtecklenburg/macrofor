"""Simple code generator skeleton: AST -> Fortran source text.

This generator is intentionally small: it gives a straightforward mapping
for the AST node types defined in `ast.py`. It will be extended to respect
formatting rules (free vs fixed form) and other stylistic options from the PDF.
"""
from __future__ import annotations
from typing import List
from .ast import (
    Program,
    Module,
    Subroutine,
    Assignment,
    DoLoop,
    SingleInstruction,
    MacroInstruction,
    Call,
    Read,
    Write,
    Label,
    Format,
    Parameter,
    If,
)


def generate_program(prog: Program) -> str:
    parts: List[str] = []
    for node in prog.body:
        if isinstance(node, Module):
            parts.append(generate_module(node))
        elif isinstance(node, Subroutine):
            parts.append(generate_subroutine(node))
    return "\n\n".join(parts)


def generate_module(mod: Module) -> str:
    lines = [f"module {mod.name}", "implicit none"]
    for n in mod.body:
        if isinstance(n, Subroutine):
            lines.append(generate_subroutine(n))
    lines.append(f"end module {mod.name}")
    return "\n".join(lines)


def generate_subroutine(sub: Subroutine) -> str:
    lines = [f"subroutine {sub.name}({', '.join(sub.args)})"]
    lines.append("implicit none")
    for s in sub.body:
        if isinstance(s, Assignment):
            lines.append(f"  {s.target} = {s.expr}")
        elif isinstance(s, DoLoop):
            lines.append(f"  do {s.var} = {s.start}, {s.end}")
            for inner in s.body:
                if isinstance(inner, Assignment):
                    lines.append(f"    {inner.target} = {inner.expr}")
            lines.append("  end do")
        elif isinstance(s, Call):
            lines.append(f"  call {s.name}({', '.join(s.args)})")
        elif isinstance(s, Read):
            lines.append(f"  read({s.unit}) {', '.join(s.var_list)}")
        elif isinstance(s, Write):
            lines.append(f"  write({s.unit}) {', '.join(s.var_list)}")
        elif isinstance(s, SingleInstruction):
            # Simple mapping for some common instructions
            name = s.name.lower()
            if name == 'call' and s.args:
                lines.append(f"  call {s.args[0]}({', '.join(s.args[1:])})")
            elif name == 'parameter':
                lines.append(f"  parameter ({', '.join(s.args)})")
            else:
                # fallback: join args
                lines.append(f"  {s.name} {' '.join(map(str,s.args))}".strip())
        elif isinstance(s, MacroInstruction):
            # Macros expand into inner body - generate inline with marker comment
            lines.append(f"  ! macro {s.name} start")
            for inner in s.body:
                # simple recursive handling for assignments and calls
                if isinstance(inner, Assignment):
                    lines.append(f"    {inner.target} = {inner.expr}")
                elif isinstance(inner, Call):
                    lines.append(f"    call {inner.name}({', '.join(inner.args)})")
            lines.append(f"  ! macro {s.name} end")
        elif isinstance(s, If):
            lines.append(f"  if ({s.condition}) then")
            for inner in s.then_body:
                if isinstance(inner, Assignment):
                    lines.append(f"    {inner.target} = {inner.expr}")
            if s.else_body:
                lines.append("  else")
                for inner in s.else_body:
                    if isinstance(inner, Assignment):
                        lines.append(f"    {inner.target} = {inner.expr}")
            lines.append("  end if")
    lines.append(f"end subroutine {sub.name}")
    return "\n".join(lines)
