"""macrofor package - Python bindings and DSL for generating Fortran code.

This package provides a comprehensive API for generating Fortran code from Python.
The main API is in `api.py` with helper functions (*f) and macro functions (*m).

Usage:
    >>> from macrofor.api import set_fortran_style, genfor, programm, commentf
    >>> set_fortran_style('f77')  # Use strict Fortran 77 style
    >>> # Now all code generation uses F77 style (c comments, 72 chars, etc.)
"""

__all__ = ["api"]
