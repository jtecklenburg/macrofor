"""High-level DSL API (helpers returning Fortran strings).

This module implements the `*f` helper functions described in the
API specification. For the MVP these helpers return Fortran source
fragments as `str`. Later they can be adapted to build AST nodes.
"""
from __future__ import annotations
from typing import Iterable, Optional


def _normalize_list_arg(lst) -> str:
    """Turn a Python list/tuple or comma-separated string into a Fortran list string."""
    if lst is None:
        return ''
    if isinstance(lst, (list, tuple)):
        return ', '.join(str(x).strip() for x in lst)
    # assume string
    return str(lst).strip()


def callf(name: str, list: Iterable[str]) -> str:
    args = _normalize_list_arg(list)
    return f"call {name}({args})"


def closef(unit: str) -> str:
    return f"close({unit})"


def commentf(string: str) -> str:
    # Fortran comment style (fixed: leading 'c' column; free format: '!')
    # Keep simple: use 'c    ' to match original MACROFORT style
    return f"c    {string}"


def commonf(name: str, list: Iterable[str]) -> str:
    body = _normalize_list_arg(list)
    return f"common /{name}/ {body}"


def continuef(label: str) -> str:
    return f"{label} continue"


def declaref(type: str, list: Iterable[str]) -> str:
    names = _normalize_list_arg(list)
    return f"{type} {names}"


def dof(label: Optional[str], index: str, start, end, step=None) -> str:
    # label optional; Fortran DO can be without label in free form
    rng = f"{index}={start}, {end}"
    if step is not None:
        rng += f", {step}"
    if label:
        return f"do {label}, {rng}"
    return f"do {index} = {start}, {end}" + (f", {step}" if step is not None else "")


def if_then_f(condition: str) -> str:
    return f"if ({condition}) then"


def elsef() -> str:
    return "else"


def endiff() -> str:
    return "end if"


def equalf(variable: str, expression: str) -> str:
    return f"{variable} = {expression}"


def formatf(label: str, list: Iterable[str]) -> str:
    items = _normalize_list_arg(list)
    return f"{label} format ({items})"


def functionf(type: str, name: str, list: Iterable[str]) -> str:
    args = _normalize_list_arg(list)
    return f"{type} function {name}({args})"


def gotof(label: str) -> str:
    return f"goto {label}"


def if_goto_f(condition: str, label: str) -> str:
    return f"if ({condition}) goto {label}"


def openf(unit: str, file: str, status: str = 'unknown') -> str:
    # file should be quoted by caller if needed
    return f"open (unit={unit}, file='{file}', status='{status}')"


def parameterf(list: Iterable[str]) -> str:
    items = _normalize_list_arg(list)
    return f"parameter ({items})"


def programf(name: str) -> str:
    return f"program {name}"


def readf(file: str, label: Optional[str], list: Iterable[str]) -> str:
    vars_s = _normalize_list_arg(list)
    if label:
        return f"read ({file}, {label}) {vars_s}"
    return f"read ({file}) {vars_s}"


def returnf() -> str:
    return "return"


def subroutinef(name: str, list: Iterable[str]) -> str:
    args = _normalize_list_arg(list)
    return f"subroutine {name}({args})"


def writef(file: str, label: Optional[str], list: Iterable[str]) -> str:
    vars_s = _normalize_list_arg(list)
    if label:
        return f"write ({file}, {label}) {vars_s}"
    return f"write ({file}) {vars_s}"

