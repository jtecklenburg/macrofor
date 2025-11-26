# macrofor

**Generate Fortran code from Python using a simple DSL.**

`macrofor` is a Python library that provides a domain-specific language (DSL) for
generating Fortran source code. The library implements a set of `*f` helper functions
(single-line Fortran instructions) and `*m` macro functions (multi-line Fortran blocks),
allowing you to programmatically compose Fortran programs directly from Python.

## Overview

This module is inspired by the **MACROFORT** system described in foundational research on automatic Fortran code generation from symbolic computation.

The `macrofor` Python package applies these ideas in a modern, Pythonic API, making it easy to:
- Compose Fortran declarations, assignments, loops, and control structures using Python,
- Generate complete Fortran programs or include fragments dynamically,
- Combine symbolic computation (e.g., SymPy) with Fortran code generation.

## Quick Start

### Single-Line Instructions (`*f` functions)

```python
from macrofor.api import callf, equalf, writef, declaref

# Generate a Fortran CALL statement
callf('compute', ['x', 'y', 'z'])      # => "call compute(x, y, z)"

# Generate an assignment
equalf('x', '2*y + 1')                 # => "x = 2*y + 1"

# Generate variable declarations
declaref('real', ['a', 'b', 'c'])      # => "real a, b, c"

# Generate WRITE statements with format labels
writef('6', '100', ['x', 'y'])         # => "write (6, 100) x, y"
```

### Multi-Line Blocks (`*m` macros)

```python
from macrofor.api import programm, if_then_m, dom

# Generate a complete IF-THEN block
if_then_m('x .gt. 0', ['a = 1', 'b = 2'])
# =>
# if (x .gt. 0) then
#   a = 1
#   b = 2
# endif

# Generate a DO loop with multiple statements
dom('i', 1, 100, ['x(i) = i', 'y(i) = i*2'])
# =>
# do 1 i=1, 100
#   x(i) = i
#   y(i) = i*2
# 1 continue

# Wrap everything in a PROGRAM block
programm('myapp', [
    'implicit none',
    'real :: x, y',
    equalf('x', '1.0'),
    equalf('y', '2.0 * x')
])
# =>
# program myapp
#   implicit none
#   real :: x, y
#   x = 1.0
#   y = 2.0 * x
# end
```

### Writing Generated Code to Files (`genfor`)

Use `genfor` to write complete Fortran programs directly to a file:

```python
from macrofor.api import genfor, programm, equalf, declaref

# Generate and write a complete Fortran program to a file
genfor('output.f90', [
    programm('simple_calc', [
        declaref('real', ['x', 'y', 'result']),
        equalf('x', '3.0'),
        equalf('y', '4.0'),
        equalf('result', 'sqrt(x**2 + y**2)'),
        writef('*', None, ["'Result = ', result"])
    ])
])
# Creates output.f90 with the complete program ready to compile!
```

The `genfor` function:
- Writes Fortran code to a file with proper formatting
- Automatically creates parent directories if needed
- Supports custom encoding (default: UTF-8) and line endings (Windows/Unix)

## Documentation

- **Quick Reference:** See `docs/MACROFOR_CHEATSHEET.md` for a complete, auto-generated table of all
  available `*f` (single-instruction) and `*m` (macro) functions with signatures and examples.
- **API Specification:** `docs/API_SPEC.md` contains detailed function descriptions extracted from docstrings.
- **Examples:** 
  - `docs/newton_fractal_example.ipynb` — Real-world example: generate Fortran code for computing Newton fractals using SymPy and macrofor with `genfor()`.

## Installation

```bash
pip install -e .
```

Or, to run the development version:

```bash
python -c "import sys; sys.path.insert(0, '.'); from macrofor import api"
```

## Testing

Run the test suite with:

```bash
python -m pytest tests/
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## References

This implementation is based on the ideas and techniques described in the original MACROFORT research:

Claude Gomez. MACROFORT: a Fortran code generator in MAPLE. [Research Report] RT-0119, INRIA. 1990, pp.14. ([https://inria.hal.science/inria-00070047](https://inria.hal.science/inria-00070047)
