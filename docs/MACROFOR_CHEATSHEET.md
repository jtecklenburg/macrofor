# MACROFOR Quick Reference

Auto-generated from `macrofor/api.py` docstrings.

## Single-Instruction Functions (*f)

| Function | Signature | Description |
|----------|-----------|-------------|
| `callf` | `callf(name: 'str', list: 'Iterable[str]') -> 'str'` | call name (list) Generate a Fortran CALL statement. |
| `closef` | `closef(unit: 'str') -> 'str'` | close (unit) Generate a Fortran CLOSE statement. |
| `commentf` | `commentf(string: 'str') -> 'str'` | c    string Generate a Fortran comment line. |
| `commonf` | `commonf(name: 'str', list: 'Iterable[str]') -> 'str'` | common /name/ list Generate a Fortran COMMON statement. |
| `continuef` | `continuef(label: 'str') -> 'str'` | label continue Generate a Fortran CONTINUE statement with label. |
| `declaref` | `declaref(type: 'str', list: 'Iterable[str]') -> 'str'` | type list Generate a Fortran variable declaration. |
| `dof` | `dof(label: 'Optional[str]', index: 'str', start, end, step=None) -> 'str'` | do label, index=start, end do label, index=start, end, step Generate a Fortran DO loop opening statement. |
| `elsef` | `elsef() -> 'str'` | else Generate a Fortran ELSE statement. |
| `endiff` | `endiff() -> 'str'` | endif Generate a Fortran END IF statement. |
| `equalf` | `equalf(variable: 'str', expression: 'str') -> 'str'` | variable=expression Generate a Fortran assignment statement. |
| `formatf` | `formatf(label: 'str', list: 'Iterable[str]') -> 'str'` | label format (list) Generate a Fortran FORMAT statement. |
| `functionf` | `functionf(type: 'str', name: 'str', list: 'Iterable[str]') -> 'str'` | type function name (list) Generate a Fortran FUNCTION statement. |
| `gotof` | `gotof(label: 'str') -> 'str'` | goto label Generate a Fortran GOTO statement. |
| `if_goto_f` | `if_goto_f(condition: 'str', label: 'str') -> 'str'` | if (condition) goto label Generate a Fortran computed GOTO (IF-GOTO) statement. |
| `if_then_f` | `if_then_f(condition: 'str') -> 'str'` | if (condition) then Generate a Fortran IF-THEN opening statement. |
| `openf` | `openf(unit: 'str', file: 'str', status: 'str' = 'unknown') -> 'str'` | open (unit=unit, file='file' ,status='status') Generate a Fortran OPEN statement. |
| `parameterf` | `parameterf(list: 'Iterable[str]') -> 'str'` | parameter (list) Generate a Fortran PARAMETER statement. |
| `programf` | `programf(name: 'str') -> 'str'` | program name Generate a Fortran PROGRAM statement. |
| `readf` | `readf(file: 'str', label: 'Optional[str]', list: 'Iterable[str]') -> 'str'` | read (file, label) list Generate a Fortran READ statement. |
| `returnf` | `returnf() -> 'str'` | return Generate a Fortran RETURN statement. |
| `subroutinef` | `subroutinef(name: 'str', list: 'Iterable[str]') -> 'str'` | subroutine name (list) Generate a Fortran SUBROUTINE statement. |
| `writef` | `writef(file: 'str', label: 'Optional[str]', list: 'Iterable[str]') -> 'str'` | write (file, label) list Generate a Fortran WRITE statement. |

## Macro Functions (*m)

| Function | Signature | Description |
|----------|-----------|-------------|
| `commonm` | `commonm(name: 'str', list: 'Iterable[str]') -> 'str'` | common /name/ list Generate a COMMON statement. |
| `declarem` | `declarem(type: 'str', list: 'Iterable[str]') -> 'str'` | type list Generate a declaration statement. |
| `dom` | `dom(index: 'str', start, end, do_list, step=None) -> 'str'` | do label index=start, end, step do_list label continue Generate a multi-line DO loop (macro version). |
| `functionm` | `functionm(type: 'str', name: 'str', list: 'Iterable[str]', body_list) -> 'str'` | type function name (list) body_list end Generate a multi-line FUNCTION block (macro version). |
| `if_then_else_m` | `if_then_else_m(condition: 'str', then_list, else_list) -> 'str'` | if (condition) then then_list else else_list endif Generate a multi-line IF-THEN-ELSE block (macro version). |
| `if_then_m` | `if_then_m(condition: 'str', then_list) -> 'str'` | if (condition) then then_list endif Generate a multi-line IF-THEN block (macro version). |
| `openm` | `openm(unit: 'str', file: 'str', status: 'str', body_list) -> 'str'` | open(unit=unit, file='file', status='status') body_list close(unit=unit) Generate a multi-line OPEN-CLOSE block (macr... |
| `programm` | `programm(name: 'str', body_list) -> 'str'` | program name body_list end Generate a multi-line PROGRAM block (macro version). |
| `readm` | `readm(file: 'str', format_list: 'Iterable[str]', var_list: 'Iterable[str]') -> 'str'` | read(file, label) var_list label format (format_list) Generate a READ statement with FORMAT (macro version). |
| `subroutinem` | `subroutinem(name: 'str', list: 'Iterable[str]', body_list) -> 'str'` | subroutine name (list) body_list end Generate a multi-line SUBROUTINE block (macro version). |
| `writem` | `writem(file: 'str', format_list: 'Iterable[str]', var_list: 'Iterable[str]') -> 'str'` | write (file, label) var_list label format (format_list) Generate a WRITE statement with FORMAT (macro version). |

---

## Detailed Function Reference

### Single-Instruction Functions (*f)

#### `callf(name: 'str', list: 'Iterable[str]') -> 'str'`

call name (list)

Generate a Fortran CALL statement.

**Args:**
name: Subroutine name. list: List of arguments.

**Returns:**
Fortran CALL statement (e.g., "call compute(x, y, z)").

**Example:**
```fortran
>>> callf('compute', ['x', 'y', 'z'])
'call compute(x, y, z)'
```

#### `closef(unit: 'str') -> 'str'`

close (unit)

Generate a Fortran CLOSE statement.

**Args:**
unit: Unit number (string or int).

**Returns:**
Fortran CLOSE statement (e.g., "close(10)").

**Example:**
```fortran
>>> closef('10')
'close(10)'
```

#### `commentf(string: 'str') -> 'str'`

c    string

Generate a Fortran comment line.

**Args:**
string: Comment text.

**Returns:**
Fortran comment (e.g., "c    this is a comment").

**Example:**
```fortran
>>> commentf('calculate derivatives')
'c    calculate derivatives'
```

#### `commonf(name: 'str', list: 'Iterable[str]') -> 'str'`

common /name/ list

Generate a Fortran COMMON statement.

**Args:**
name: COMMON block name. list: List of variable names.

**Returns:**
Fortran COMMON statement (e.g., "common /data/ x, y, z").

**Example:**
```fortran
>>> commonf('data', ['x', 'y'])
'common /data/ x, y'
```

#### `continuef(label: 'str') -> 'str'`

label continue

Generate a Fortran CONTINUE statement with label.

**Args:**
label: Label (e.g., "100").

**Returns:**
Fortran CONTINUE statement (e.g., "100 continue").

**Example:**
```fortran
>>> continuef('100')
'100 continue'
```

#### `declaref(type: 'str', list: 'Iterable[str]') -> 'str'`

type list

Generate a Fortran variable declaration.

**Args:**
type: Fortran type (e.g., "real", "integer"). list: List of variable names.

**Returns:**
Declaration statement (e.g., "real a, b, c").

**Example:**
```fortran
>>> declaref('real', ['a', 'b', 'c'])
'real a, b, c'
```

#### `dof(label: 'Optional[str]', index: 'str', start, end, step=None) -> 'str'`

do label, index=start, end
do label, index=start, end, step

Generate a Fortran DO loop opening statement.

**Args:**
label: Optional label (e.g., "100"). index: Loop variable (e.g., "i"). start: Start value. end: End value. step: Optional step value (default 1).

**Returns:**
DO loop opening (e.g., "do 100 i=1, 100" or "do i=1, 100, 2").

**Example:**
```fortran
>>> dof('100', 'i', 1, 100)
'do 100 i=1, 100'
>>> dof(None, 'j', 1, 50, step=2)
'do j = 1, 50, 2'
```

#### `elsef() -> 'str'`

else

Generate a Fortran ELSE statement.

**Returns:**
ELSE statement.

**Example:**
```fortran
>>> elsef()
'else'
```

#### `endiff() -> 'str'`

endif

Generate a Fortran END IF statement.

**Returns:**
END IF statement.

**Example:**
```fortran
>>> endiff()
'end if'
```

#### `equalf(variable: 'str', expression: 'str') -> 'str'`

variable=expression

Generate a Fortran assignment statement.

**Args:**
variable: Variable name (e.g., "x", "a(i)"). expression: RHS expression.

**Returns:**
Assignment statement (e.g., "x = 2*y + 1").

**Example:**
```fortran
>>> equalf('x', '2*y + 1')
'x = 2*y + 1'
```

#### `formatf(label: 'str', list: 'Iterable[str]') -> 'str'`

label format (list)

Generate a Fortran FORMAT statement.

**Args:**
label: Statement label (e.g., "100"). list: List of format descriptors (e.g., ["I5", "F10.2"]).

**Returns:**
FORMAT statement (e.g., "100 format (I5, F10.2)").

**Example:**
```fortran
>>> formatf('100', ['I5', 'F10.2'])
'100 format (I5, F10.2)'
```

#### `functionf(type: 'str', name: 'str', list: 'Iterable[str]') -> 'str'`

type function name (list)

Generate a Fortran FUNCTION statement.

**Args:**
type: Return type (e.g., "real", "integer"). name: Function name. list: List of parameters.

**Returns:**
FUNCTION opening (e.g., "real function square(x)").

**Example:**
```fortran
>>> functionf('real', 'square', ['x'])
'real function square(x)'
```

#### `gotof(label: 'str') -> 'str'`

goto label

Generate a Fortran GOTO statement.

**Args:**
label: Target label (e.g., "100").

**Returns:**
GOTO statement (e.g., "goto 100").

**Example:**
```fortran
>>> gotof('100')
'goto 100'
```

#### `if_goto_f(condition: 'str', label: 'str') -> 'str'`

if (condition) goto label

Generate a Fortran computed GOTO (IF-GOTO) statement.

**Args:**
condition: Fortran condition. label: Target label.

**Returns:**
IF-GOTO statement (e.g., "if (x .lt. 0) goto 100").

**Example:**
```fortran
>>> if_goto_f('x .lt. 0', '100')
'if (x .lt. 0) goto 100'
```

#### `if_then_f(condition: 'str') -> 'str'`

if (condition) then

Generate a Fortran IF-THEN opening statement.

**Args:**
condition: Fortran condition (e.g., "x .gt. 0").

**Returns:**
IF-THEN opening (e.g., "if (x .gt. 0) then").

**Example:**
```fortran
>>> if_then_f('n .eq. 0')
'if (n .eq. 0) then'
```

#### `openf(unit: 'str', file: 'str', status: 'str' = 'unknown') -> 'str'`

open (unit=unit, file='file' ,status='status')

Generate a Fortran OPEN statement.

**Args:**
unit: Unit number. file: Filename. status: File status (e.g., "old", "new", "unknown").

**Returns:**
OPEN statement (e.g., "open (unit=10, file='data.txt', status='old')").

**Example:**
```fortran
>>> openf('10', 'input.txt', 'old')
"open (unit=10, file='input.txt', status='old')"
```

#### `parameterf(list: 'Iterable[str]') -> 'str'`

parameter (list)

Generate a Fortran PARAMETER statement.

**Args:**
list: List of parameter definitions (e.g., ["pi=3.14159", "e=2.71828"]).

**Returns:**
PARAMETER statement (e.g., "parameter (pi=3.14159, e=2.71828)").

**Example:**
```fortran
>>> parameterf(['pi=3.14159'])
'parameter (pi=3.14159)'
```

#### `programf(name: 'str') -> 'str'`

program name

Generate a Fortran PROGRAM statement.

**Args:**
name: Program name.

**Returns:**
PROGRAM statement (e.g., "program myapp").

**Example:**
```fortran
>>> programf('hello')
'program hello'
```

#### `readf(file: 'str', label: 'Optional[str]', list: 'Iterable[str]') -> 'str'`

read (file, label) list

Generate a Fortran READ statement.

**Args:**
file: Unit number or filename. label: Optional FORMAT label. list: List of variables to read.

**Returns:**
READ statement (e.g., "read (5, 100) x, y" or "read (5) x, y").

**Example:**
```fortran
>>> readf('5', '100', ['x', 'y'])
'read (5, 100) x, y'
>>> readf('5', None, ['i', 'j'])
'read (5) i, j'
```

#### `returnf() -> 'str'`

return

Generate a Fortran RETURN statement.

**Returns:**
RETURN statement.

**Example:**
```fortran
>>> returnf()
'return'
```

#### `subroutinef(name: 'str', list: 'Iterable[str]') -> 'str'`

subroutine name (list)

Generate a Fortran SUBROUTINE statement.

**Args:**
name: Subroutine name. list: List of parameters.

**Returns:**
SUBROUTINE statement (e.g., "subroutine compute(x, y, z)").

**Example:**
```fortran
>>> subroutinef('compute', ['x', 'y', 'z'])
'subroutine compute(x, y, z)'
```

#### `writef(file: 'str', label: 'Optional[str]', list: 'Iterable[str]') -> 'str'`

write (file, label) list

Generate a Fortran WRITE statement.

**Args:**
file: Unit number. label: Optional FORMAT label. list: List of variables to write.

**Returns:**
WRITE statement (e.g., "write (6, 100) x, y" or "write (6) x, y").

**Example:**
```fortran
>>> writef('6', '100', ['x', 'y'])
'write (6, 100) x, y'
>>> writef('6', None, ['iter'])
'write (6) iter'
```

### Macro Functions (*m)

#### `commonm(name: 'str', list: 'Iterable[str]') -> 'str'`

common /name/ list

Generate a COMMON statement.

**Args:**
name: COMMON block name. list: List of variable names.

**Returns:**
COMMON statement (e.g., "common /data/ x, y, z").

**Example:**
```fortran
>>> commonm('data', ['a', 'b'])
'common /data/ a, b'
```

#### `declarem(type: 'str', list: 'Iterable[str]') -> 'str'`

type list

Generate a declaration statement.

**Args:**
type: Fortran type (e.g., "real", "integer"). list: List of variable names.

**Returns:**
Declaration statement (e.g., "real a, b, c").

**Example:**
```fortran
>>> declarem('real', ['x', 'y', 'z'])
'real x, y, z'
```

#### `dom(index: 'str', start, end, do_list, step=None) -> 'str'`

do label index=start, end, step
do_list
label continue

Generate a multi-line DO loop (macro version).

**Args:**
index: Loop variable (e.g., "i"). start: Start value. end: End value. do_list: List of body statements. step: Optional step value.

**Returns:**
Complete DO loop with label and continue (indented body).

**Example:**
```fortran
>>> dom('i', 1, 10, ['a(i) = i', 'b(i) = i*2'])
'do 1 i=1, 10
  a(i) = i
  b(i) = i*2
1 continue'
```

#### `functionm(type: 'str', name: 'str', list: 'Iterable[str]', body_list) -> 'str'`

type function name (list)
body_list
end

Generate a multi-line FUNCTION block (macro version).

**Args:**
type: Return type (e.g., "real", "integer"). name: Function name. list: List of parameters. body_list: List of body statements.

**Returns:**
Complete FUNCTION definition (indented body).

**Example:**
```fortran
>>> functionm('real', 'square', ['x'], ['real :: x', 'square = x*x'])
'real function square(x)
  real :: x
  square = x*x
end'
```

#### `if_then_else_m(condition: 'str', then_list, else_list) -> 'str'`

if (condition) then
then_list
else
else_list
endif

Generate a multi-line IF-THEN-ELSE block (macro version).

**Args:**
condition: Fortran condition. then_list: List of statements for THEN block. else_list: List of statements for ELSE block.

**Returns:**
Complete IF-THEN-ELSE-END IF (indented bodies).

**Example:**
```fortran
>>> if_then_else_m('n .eq. 0', ['y = 1'], ['y = 0'])
'if (n .eq. 0) then
  y = 1
else
  y = 0
end if'
```

#### `if_then_m(condition: 'str', then_list) -> 'str'`

if (condition) then
then_list
endif

Generate a multi-line IF-THEN block (macro version).

**Args:**
condition: Fortran condition (e.g., "x .gt. 0"). then_list: List of statements for THEN block.

**Returns:**
Complete IF-THEN-END IF (indented body).

**Example:**
```fortran
>>> if_then_m('x .gt. 0', ['a = 1', 'b = 2'])
'if (x .gt. 0) then
  a = 1
  b = 2
end if'
```

#### `openm(unit: 'str', file: 'str', status: 'str', body_list) -> 'str'`

open(unit=unit, file='file', status='status')
body_list
close(unit=unit)

Generate a multi-line OPEN-CLOSE block (macro version).

**Args:**
unit: Unit number. file: Filename. status: File status (e.g., "old", "new", "unknown"). body_list: List of I/O statements.

**Returns:**
OPEN statement, indented body, and CLOSE statement.

**Example:**
```fortran
>>> openm('10', 'data.txt', 'old', ['read(10) x, y'])
"open(unit=10, file='data.txt', status='old')
  read(10) x, y
close(unit=10)"
```

#### `programm(name: 'str', body_list) -> 'str'`

program name
body_list
end

Generate a multi-line PROGRAM block (macro version).

**Args:**
name: Program name. body_list: List of program statements.

**Returns:**
Complete PROGRAM definition (indented body).

**Example:**
```fortran
>>> programm('hello', ['implicit none', 'print *, "Hi"'])
'program hello
  implicit none
  print *, "Hi"
end'
```

#### `readm(file: 'str', format_list: 'Iterable[str]', var_list: 'Iterable[str]') -> 'str'`

read(file, label) var_list
label format (format_list)

Generate a READ statement with FORMAT (macro version).

**Args:**
file: Unit number. format_list: List of format descriptors. var_list: List of variables to read.

**Returns:**
READ statement with FORMAT label (two lines).

**Example:**
```fortran
>>> readm('5', ['I5', 'F10.2'], ['i', 'x'])
'read(5, 1) i, x
1 format (I5, F10.2)'
```

#### `subroutinem(name: 'str', list: 'Iterable[str]', body_list) -> 'str'`

subroutine name (list)
body_list
end

Generate a multi-line SUBROUTINE block (macro version).

**Args:**
name: Subroutine name. list: List of parameters. body_list: List of body statements.

**Returns:**
Complete SUBROUTINE definition (indented body).

**Example:**
```fortran
>>> subroutinem('compute', ['x', 'y'], ['integer :: i', 'i = x + y'])
'subroutine compute(x, y)
  integer :: i
  i = x + y
end'
```

#### `writem(file: 'str', format_list: 'Iterable[str]', var_list: 'Iterable[str]') -> 'str'`

write (file, label) var_list
label format (format_list)

Generate a WRITE statement with FORMAT (macro version).

**Args:**
file: Unit number. format_list: List of format descriptors. var_list: List of variables to write.

**Returns:**
WRITE statement with FORMAT label (two lines).

**Example:**
```fortran
>>> writem('6', ['I3', 'F8.3'], ['iter', 'residual'])
'write(6, 1) iter, residual
1 format (I3, F8.3)'
```
