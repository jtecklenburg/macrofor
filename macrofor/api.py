"""High-level DSL API (helpers returning Fortran strings).

This module implements the `*f` helper functions described in the
API specification. For the MVP these helpers return Fortran source
fragments as `str`. Later they can be adapted to build AST nodes.
"""
from __future__ import annotations
from typing import Iterable, Optional
import re


# Global label counter for automatic label management
_label_counter = 0


def _get_next_label_placeholder() -> str:
    """Get the next label placeholder (__LABEL_N__).
    
    Each call to dom(), if_then_m(), etc. receives a unique placeholder
    that will be replaced by genfor() with a sequential number.
    """
    global _label_counter
    _label_counter += 1
    return f"__LABEL_{_label_counter}__"


def _reset_label_counter():
    """Reset the label counter (called by genfor at the start of file generation)."""
    global _label_counter
    _label_counter = 0


def _replace_label_placeholders(code: str) -> str:
    """Replace __LABEL_N__ placeholders with sequential numbers (100, 200, 300, ...).
    
    Args:
        code: Fortran source code with label placeholders.
    
    Returns:
        Fortran source code with placeholders replaced by sequential labels.
    
    Example:
        Input:  "do __LABEL_1__ i=1,10\\n  x=1\\n__LABEL_1__ continue"
        Output: "do 100 i=1,10\\n  x=1\\n100 continue"
    """
    # Find all unique placeholders in order of appearance
    placeholders = []
    for match in re.finditer(r'__LABEL_\d+__', code):
        placeholder = match.group(0)
        if placeholder not in placeholders:
            placeholders.append(placeholder)
    
    # Replace each unique placeholder with a sequential label (100, 200, 300, ...)
    result = code
    for i, placeholder in enumerate(placeholders, start=1):
        label = str(100 * i)
        result = result.replace(placeholder, label)
    
    return result


def _normalize_list_arg(lst) -> str:
    """Turn a Python list/tuple or comma-separated string into a Fortran list string."""
    if lst is None:
        return ''
    if isinstance(lst, (list, tuple)):
        return ', '.join(str(x).strip() for x in lst)
    # assume string
    return str(lst).strip()


def callf(name: str, list: Iterable[str]) -> str:
    """call name (list)

    Generate a Fortran CALL statement.

    Args:
        name: Subroutine name.
        list: List of arguments.

    Returns:
        Fortran CALL statement (e.g., "call compute(x, y, z)").

    Example:
        >>> callf('compute', ['x', 'y', 'z'])
        'call compute(x, y, z)'
    """
    args = _normalize_list_arg(list)
    return f"call {name}({args})"


def closef(unit: str) -> str:
    """close (unit)

    Generate a Fortran CLOSE statement.

    Args:
        unit: Unit number (string or int).

    Returns:
        Fortran CLOSE statement (e.g., "close(10)").

    Example:
        >>> closef('10')
        'close(10)'
    """
    return f"close({unit})"


def commentf(string: str) -> str:
    """!    string

    Generate a Fortran comment line.

    Args:
        string: Comment text.

    Returns:
        Fortran comment (e.g., "!    this is a comment").

    Example:
        >>> commentf('calculate derivatives')
        '!    calculate derivatives'
    """
    # Fortran comment style (Fortran 90: use '!' for modern style)
    return f"!    {string}"


def commonf(name: str, list: Iterable[str]) -> str:
    """common /name/ list

    Generate a Fortran COMMON statement.

    Args:
        name: COMMON block name.
        list: List of variable names.

    Returns:
        Fortran COMMON statement (e.g., "common/data/x, y, z").
        Note: Maple-style without spaces around slashes.

    Example:
        >>> commonf('data', ['x', 'y'])
        'common/data/x, y'
    """
    body = _normalize_list_arg(list)
    return f"common/{name}/{body}"


def continuef(label: str) -> str:
    """label continue

    Generate a Fortran CONTINUE statement with label.

    Args:
        label: Label (e.g., "100").

    Returns:
        Fortran CONTINUE statement (e.g., "100 continue").

    Example:
        >>> continuef('100')
        '100 continue'
    """
    return f"{label} continue"


def declaref(type: str, list: Iterable[str]) -> str:
    """type list

    Generate a Fortran variable declaration.

    Args:
        type: Fortran type (e.g., "real", "integer").
        list: List of variable names.

    Returns:
        Declaration statement (e.g., "real a, b, c").

    Example:
        >>> declaref('real', ['a', 'b', 'c'])
        'real a, b, c'
        >>> declaref('implicit real*8', ['a-h', 'o-z'])
        'implicit real*8(a-h,o-z)'
    """
    names = _normalize_list_arg(list)
    
    # Special handling for implicit statements: use parentheses and no spaces after commas
    if type.lower().startswith('implicit'):
        # Remove spaces after commas for implicit statements
        names_compact = names.replace(', ', ',')
        return f"{type}({names_compact})"
    
    return f"{type} {names}"


def dof(label: Optional[str], index: str, start, end, step=None) -> str:
    """do label, index=start, end
    do label, index=start, end, step

    Generate a Fortran DO loop opening statement.

    Args:
        label: Optional label (e.g., "100").
        index: Loop variable (e.g., "i").
        start: Start value.
        end: End value.
        step: Optional step value (default 1).

    Returns:
        DO loop opening (e.g., "do 100, i=1, 100" or "do i=1, 100, 2").

    Example:
        >>> dof('100', 'i', 1, 100)
        'do 100, i=1, 100'
        >>> dof(None, 'j', 1, 50, step=2)
        'do j = 1, 50, 2'
    """
    # label optional; Fortran DO can be without label in free form
    rng = f"{index}={start}, {end}"
    if step is not None:
        rng += f", {step}"
    if label:
        return f"do {label}, {rng}"
    return f"do {index} = {start}, {end}" + (f", {step}" if step is not None else "")


def if_then_f(condition: str) -> str:
    """if (condition) then

    Generate a Fortran IF-THEN opening statement.

    Args:
        condition: Fortran condition (e.g., "x .gt. 0").

    Returns:
        IF-THEN opening (e.g., "if (x .gt. 0) then").

    Example:
        >>> if_then_f('n .eq. 0')
        'if (n .eq. 0) then'
    """
    return f"if ({condition}) then"


def elsef() -> str:
    """else

    Generate a Fortran ELSE statement.

    Returns:
        ELSE statement.

    Example:
        >>> elsef()
        'else'
    """
    return "else"


def endiff() -> str:
    """endif

    Generate a Fortran END IF statement.

    Returns:
        END IF statement.

    Example:
        >>> endiff()
        'end if'
    """
    return "end if"


def equalf(variable: str, expression: str) -> str:
    """variable=expression

    Generate a Fortran assignment statement.

    Args:
        variable: Variable name (e.g., "x", "a(i)").
        expression: RHS expression.

    Returns:
        Assignment statement (e.g., "x = 2*y + 1").

    Example:
        >>> equalf('x', '2*y + 1')
        'x = 2*y + 1'
    """
    return f"{variable} = {expression}"


def formatf(list: Iterable[str]) -> str:
    """label format (list)

    Generate a Fortran FORMAT statement with automatic label placeholder.

    Args:
        list: List of format descriptors (e.g., ["I5", "F10.2"]).

    Returns:
        FORMAT statement with label placeholder (e.g., "__LABEL_1__ format (I5, F10.2)").
        The placeholder is replaced with actual sequential labels (100, 200, 300, ...)
        by genfor() during code generation.

    Example:
        >>> formatf(['I5', 'F10.2'])
        '__LABEL_1__ format (I5, F10.2)'
    """
    label = _get_next_label_placeholder()
    items = _normalize_list_arg(list)
    return f"{label} format ({items})"


def functionf(type: str, name: str, list: Iterable[str]) -> str:
    """type function name (list)

    Generate a Fortran FUNCTION statement.

    Args:
        type: Return type (e.g., "real", "integer").
        name: Function name.
        list: List of parameters.

    Returns:
        FUNCTION opening (e.g., "real function square(x)").

    Example:
        >>> functionf('real', 'square', ['x'])
        'real function square(x)'
    """
    args = _normalize_list_arg(list)
    return f"{type} function {name}({args})"


def gotof(label: str) -> str:
    """goto label

    Generate a Fortran GOTO statement.

    Args:
        label: Target label (e.g., "100").

    Returns:
        GOTO statement (e.g., "goto 100").

    Example:
        >>> gotof('100')
        'goto 100'
    """
    return f"goto {label}"


def if_goto_f(condition: str, label: str) -> str:
    """if (condition) goto label

    Generate a Fortran computed GOTO (IF-GOTO) statement.

    Args:
        condition: Fortran condition.
        label: Target label.

    Returns:
        IF-GOTO statement (e.g., "if (x .lt. 0) goto 100").

    Example:
        >>> if_goto_f('x .lt. 0', '100')
        'if (x .lt. 0) goto 100'
    """
    return f"if ({condition}) goto {label}"


def openf(unit: str, file: str, status: str = 'unknown', access: str = None) -> str:
    """open(unit=unit, file='file', status='status'[, access='access'])

    Generate a Fortran OPEN statement.

    Args:
        unit: Unit number.
        file: Filename.
        status: File status (e.g., "old", "new", "unknown").
        access: Optional access mode (e.g., "append", "sequential").

    Returns:
        OPEN statement (e.g., "open(unit=10, file='data.txt', status='old')").

    Example:
        >>> openf('10', 'input.txt', 'old')
        "open(unit=10, file='input.txt', status='old')"
        >>> openf('11', 'output.txt', 'old', 'append')
        "open(unit=11, file='output.txt', status='old', access='append')"
    """
    if access:
        return f"open(unit={unit}, file='{file}', status='{status}', access='{access}')"
    else:
        return f"open(unit={unit}, file='{file}', status='{status}')"


def parameterf(list: Iterable[str]) -> str:
    """parameter (list)

    Generate a Fortran PARAMETER statement.

    Args:
        list: List of parameter definitions (e.g., ["pi=3.14159", "e=2.71828"]).

    Returns:
        PARAMETER statement (e.g., "parameter (pi=3.14159, e=2.71828)").

    Example:
        >>> parameterf(['pi=3.14159'])
        'parameter (pi=3.14159)'
    """
    items = _normalize_list_arg(list)
    return f"parameter ({items})"


def programf(name: str) -> str:
    """program name

    Generate a Fortran PROGRAM statement.

    Args:
        name: Program name.

    Returns:
        PROGRAM statement (e.g., "program myapp").

    Example:
        >>> programf('hello')
        'program hello'
    """
    return f"program {name}"


def readf(file: str, label: Optional[str], list: Iterable[str]) -> str:
    """read (file, label) list

    Generate a Fortran READ statement.

    Args:
        file: Unit number or filename.
        label: Optional FORMAT label.
        list: List of variables to read.

    Returns:
        READ statement (e.g., "read (5, 100) x, y" or "read (5) x, y").

    Example:
        >>> readf('5', '100', ['x', 'y'])
        'read (5, 100) x, y'
        >>> readf('5', None, ['i', 'j'])
        'read (5) i, j'
    """
    vars_s = _normalize_list_arg(list)
    if label:
        return f"read ({file}, {label}) {vars_s}"
    return f"read ({file}) {vars_s}"


def returnf() -> str:
    """return

    Generate a Fortran RETURN statement.

    Returns:
        RETURN statement.

    Example:
        >>> returnf()
        'return'
    """
    return "return"


def subroutinef(name: str, list: Iterable[str]) -> str:
    """subroutine name (list)

    Generate a Fortran SUBROUTINE statement with comment header.

    Args:
        name: Subroutine name.
        list: List of parameters.

    Returns:
        SUBROUTINE statement with comment header (e.g., "!\n! SUBROUTINE compute\n!\nsubroutine compute(x, y, z)").

    Example:
        >>> subroutinef('compute', ['x', 'y', 'z'])
        '!\\n! SUBROUTINE compute\\n!\\nsubroutine compute(x, y, z)'
    """
    args = _normalize_list_arg(list)
    return f"!\n! SUBROUTINE {name}\n!\nsubroutine {name}({args})"


def writef(file: str, label: Optional[str], list: Iterable[str]) -> str:
    """write (file, label) list

    Generate a Fortran WRITE statement.

    Args:
        file: Unit number.
        label: Optional FORMAT label.
        list: List of variables to write.

    Returns:
        WRITE statement (e.g., "write (6, 100) x, y" or "write (6) x, y").

    Example:
        >>> writef('6', '100', ['x', 'y'])
        'write (6, 100) x, y'
        >>> writef('6', None, ['iter'])
        'write (6) iter'
    """
    vars_s = _normalize_list_arg(list)
    if label:
        return f"write ({file}, {label}) {vars_s}"
    return f"write ({file}) {vars_s}"


# ============================================================================
# Macro functions (*m): generate multi-line blocks with indentation
# ============================================================================

def _indent_lines(text: str, indent: str = "  ") -> str:
    """Indent all non-empty lines in text."""
    lines = text.split("\n")
    return "\n".join(indent + line if line.strip() else "" for line in lines)


def _body_to_text(body_list) -> str:
    """Convert a body list (list of strings or nested structures) to indented text."""
    if isinstance(body_list, str):
        return body_list
    if isinstance(body_list, (list, tuple)):
        return "\n".join(str(line) for line in body_list)
    return str(body_list)


def dom(index: str, start, end, do_list, step=None) -> str:
    """do label index=start, end, step
    	do_list
    label continue

    Generate a multi-line DO loop (macro version).
    
    Uses automatic label placeholder management: each dom() call receives a unique
    placeholder (__LABEL_N__) that genfor() will replace with a sequential number (100, 200, ...).
    
    Args:
        index: Loop variable (e.g., "i").
        start: Start value.
        end: End value.
        do_list: List of body statements.
        step: Optional step value.
    
    Returns:
        Complete DO loop with label placeholder and continue (indented body).
        Labels are replaced by genfor() during file generation.
    
    Example:
        >>> dom('i', 1, 10, ['a(i) = i', 'b(i) = i*2'])
        'do __LABEL_1__ i=1, 10\\n  a(i) = i\\n  b(i) = i*2\\n__LABEL_1__ continue'
    """
    # Generate a unique label placeholder (will be replaced by genfor)
    label = _get_next_label_placeholder()
    
    rng = f"{index}={start}, {end}"
    if step is not None:
        rng += f", {step}"
    
    body_text = _body_to_text(do_list)
    body_indented = _indent_lines(body_text)
    
    return f"do {label}, {rng}\n{body_indented}\n{label} continue"


def functionm(type: str, name: str, list: Iterable[str], body_list) -> str:
    """type function name (list)
    	body_list
    end

    Generate a multi-line FUNCTION block (macro version).
    
    Args:
        type: Return type (e.g., "real", "integer").
        name: Function name.
        list: List of parameters.
        body_list: List of body statements.
    
    Returns:
        Complete FUNCTION definition (indented body).
    
    Example:
        >>> functionm('real', 'square', ['x'], ['real :: x', 'square = x*x'])
        'real function square(x)\\n  real :: x\\n  square = x*x\\nend'
    """
    args = _normalize_list_arg(list)
    body_text = _body_to_text(body_list)
    body_indented = _indent_lines(body_text)
    
    return f"{type} function {name}({args})\n{body_indented}\nend"


def if_then_m(condition: str, then_list) -> str:
    """if (condition) then
    	then_list
    endif

    Generate a multi-line IF-THEN block (macro version).
    
    Args:
        condition: Fortran condition (e.g., "x .gt. 0").
        then_list: List of statements for THEN block.
    
    Returns:
        Complete IF-THEN-END IF (indented body).
    
    Example:
        >>> if_then_m('x .gt. 0', ['a = 1', 'b = 2'])
        'if (x .gt. 0) then\\n  a = 1\\n  b = 2\\nend if'
    """
    body_text = _body_to_text(then_list)
    body_indented = _indent_lines(body_text)
    
    return f"if ({condition}) then\n{body_indented}\nend if"


def if_then_else_m(condition: str, then_list, else_list) -> str:
    """if (condition) then
    	then_list
    else
    	else_list
    endif

    Generate a multi-line IF-THEN-ELSE block (macro version).
    
    Args:
        condition: Fortran condition.
        then_list: List of statements for THEN block.
        else_list: List of statements for ELSE block.
    
    Returns:
        Complete IF-THEN-ELSE-END IF (indented bodies).
    
    Example:
        >>> if_then_else_m('n .eq. 0', ['y = 1'], ['y = 0'])
        'if (n .eq. 0) then\\n  y = 1\\nelse\\n  y = 0\\nend if'
    """
    then_text = _body_to_text(then_list)
    else_text = _body_to_text(else_list)
    then_indented = _indent_lines(then_text)
    else_indented = _indent_lines(else_text)
    
    return f"if ({condition}) then\n{then_indented}\nelse\n{else_indented}\nend if"


def programm(name: str, body_list) -> str:
    """program name
    	body_list
    end

    Generate a multi-line PROGRAM block (macro version).
    
    Args:
        name: Program name.
        body_list: List of program statements.
    
    Returns:
        Complete PROGRAM definition (indented body).
    
    Example:
        >>> programm('hello', ['implicit none', 'print *, \"Hi\"'])
        'program hello\\n  implicit none\\n  print *, \"Hi\"\\nend'
    """
    body_text = _body_to_text(body_list)
    body_indented = _indent_lines(body_text)
    
    return f"program {name}\n{body_indented}\nend"


def subroutinem(name: str, list: Iterable[str], body_list) -> str:
    """subroutine name (list)
    	body_list
    end subroutine name

    Generate a multi-line SUBROUTINE block (macro version) with comment header.
    
    Args:
        name: Subroutine name.
        list: List of parameters.
        body_list: List of body statements.
    
    Returns:
        Complete SUBROUTINE definition with comment header (indented body).
    
    Example:
        >>> subroutinem('compute', ['x', 'y'], ['integer :: i', 'i = x + y'])
        '!\\n! SUBROUTINE compute\\n!\\nsubroutine compute(x, y)\\n  integer :: i\\n  i = x + y\\nend subroutine compute'
    """
    args = _normalize_list_arg(list)
    body_text = _body_to_text(body_list)
    body_indented = _indent_lines(body_text)
    
    return f"!\n! SUBROUTINE {name}\n!\nsubroutine {name}({args})\n{body_indented}\nend subroutine {name}"


def openm(unit: str, file: str, status: str, body_list, access: str = None) -> str:
    """open(unit=unit, file='file', status='status'[, access='access'])
    	body_list
    close(unit=unit)

    Generate a multi-line OPEN-CLOSE block (macro version).
    
    Args:
        unit: Unit number.
        file: Filename.
        status: File status (e.g., "old", "new", "unknown").
        body_list: List of I/O statements.
        access: Optional access mode (e.g., "append", "sequential").
    
    Returns:
        OPEN statement, indented body, and CLOSE statement.
    
    Example:
        >>> openm('10', 'data.txt', 'old', ['read(10) x, y'])
        \"open(unit=10, file='data.txt', status='old')\\n  read(10) x, y\\nclose(unit=10)\"
        >>> openm('11', 'output.txt', 'old', ['write(11) results'], 'append')
        \"open(unit=11, file='output.txt', status='old', access='append')\\n  write(11) results\\nclose(unit=11)\"
    """
    body_text = _body_to_text(body_list)
    body_indented = _indent_lines(body_text)
    
    if access:
        return f"open(unit={unit}, file='{file}', status='{status}', access='{access}')\n{body_indented}\nclose(unit={unit})"
    else:
        return f"open(unit={unit}, file='{file}', status='{status}')\n{body_indented}\nclose(unit={unit})"


def readm(file: str, format_list: Iterable[str], var_list: Iterable[str]) -> str:
    """read(file, label) var_list
    label format (format_list)

    Generate a READ statement with FORMAT (macro version) using automatic label placeholder.
    
    Args:
        file: Unit number.
        format_list: List of format descriptors.
        var_list: List of variables to read.
    
    Returns:
        READ statement with FORMAT label placeholder (two lines).
        The placeholder is replaced with actual sequential labels (100, 200, 300, ...)
        by genfor() during code generation.
    
    Example:
        >>> readm('5', ['I5', 'F10.2'], ['i', 'x'])
        'read(5, __LABEL_1__) i, x\\n__LABEL_1__ format (I5, F10.2)'
    """
    label = _get_next_label_placeholder()
    fmt_items = _normalize_list_arg(format_list)
    var_items = _normalize_list_arg(var_list)
    
    return f"read({file}, {label}) {var_items}\n{label} format ({fmt_items})"


def writem(file: str, format_list: Iterable[str], var_list: Iterable[str]) -> str:
    """write (file, label) var_list
    label format (format_list)

    Generate a WRITE statement with FORMAT (macro version) using automatic label placeholder.
    
    Args:
        file: Unit number.
        format_list: List of format descriptors.
        var_list: List of variables to write.
    
    Returns:
        WRITE statement with FORMAT label placeholder (two lines).
        The placeholder is replaced with actual sequential labels (100, 200, 300, ...)
        by genfor() during code generation.
    
    Example:
        >>> writem('6', ['I3', 'F8.3'], ['iter', 'residual'])
        'write(6, __LABEL_1__) iter, residual\\n__LABEL_1__ format (I3, F8.3)'
    """
    label = _get_next_label_placeholder()
    fmt_items = _normalize_list_arg(format_list)
    var_items = _normalize_list_arg(var_list)
    
    return f"write({file}, {label}) {var_items}\n{label} format ({fmt_items})"


def commonm(name: str, list: Iterable[str]) -> str:
    """common /name/ list

    Generate a COMMON statement.
    
    Args:
        name: COMMON block name.
        list: List of variable names.
    
    Returns:
        COMMON statement (e.g., "common /data/ x, y, z").
    
    Example:
        >>> commonm('data', ['a', 'b'])
        'common /data/ a, b'
    """
    body = _normalize_list_arg(list)
    return f"common /{name}/ {body}"


def declarem(type: str, list: Iterable[str]) -> str:
    """type list

    Generate a declaration statement.
    
    Args:
        type: Fortran type (e.g., "real", "integer").
        list: List of variable names.
    
    Returns:
        Declaration statement (e.g., "real a, b, c").
    
    Example:
        >>> declarem('real', ['x', 'y', 'z'])
        'real x, y, z'
    """
    names = _normalize_list_arg(list)
    return f"{type} {names}"


def _wrap_long_lines(code: str, max_length: int = 72, format_style: str = 'fixed') -> str:
    """Wrap Fortran lines longer than max_length using continuation characters.
    
    Args:
        code: Fortran source code.
        max_length: Maximum line length (default: 72 for fixed format).
        format_style: 'fixed' or 'free' (default: 'fixed').
    
    Returns:
        Code with wrapped lines.
    """
    lines = code.split('\n')
    wrapped = []
    
    for line in lines:
        # Skip Fortran comments (must be at start of line, possibly with whitespace)
        stripped = line.lstrip()
        if stripped.startswith(('!', 'c ', 'C ', '* ', 'c\t', 'C\t')):
            wrapped.append(line)
            continue
        # Also check for comment-only lines (just 'c', 'C', or '*')
        if stripped in ('c', 'C', '*'):
            wrapped.append(line)
            continue
        
        # Skip short lines
        if len(line) <= max_length:
            wrapped.append(line)
            continue
        
        # Line is too long - wrap it
        indent = len(line) - len(line.lstrip())
        remaining = line.strip()
        first_line = True
       
        # Continue wrapping while remaining text (with indent) exceeds limit
        while len(remaining) + indent > max_length:
            
            # Calculate where to split (leave room for indent and continuation)
            available = max_length - indent
            if not first_line:
                available = max_length - 6  # Continuation line starts at column 7
            
            # Find a good split position (prefer operators and commas)
            split_pos = available
            
            # Try to split at logical positions
            for char in [', ', ',', ' + ', ' - ', ' * ', '/', '(', ' .and. ', ' .or. ']:
                pos = remaining[:split_pos].rfind(char)
                if pos > 0:  # Found a split point
                    split_pos = pos + len(char)
                    break
            
            # If no good split point found, force split at available position
            if split_pos >= len(remaining):
                split_pos = available
            
            # Generate continuation
            if format_style == 'free':
                # Fortran 90 Free Format: & at end of line
                wrapped.append(' ' * indent + remaining[:split_pos].rstrip() + ' &')
                remaining = remaining[split_pos:].lstrip()
                if remaining and not remaining.startswith('&'):
                    remaining = '&' + remaining
                indent = 1  # Continuation lines get minimal indent
            else:
                # Fortran 77 Fixed Format: character in column 6
                if first_line:
                    wrapped.append(' ' * indent + remaining[:split_pos].rstrip())
                    first_line = False
                else:
                    wrapped.append('     &' + remaining[:split_pos].rstrip())
                remaining = remaining[split_pos:].lstrip()
        
        # Add the last part
        if format_style == 'fixed' and not first_line:
            wrapped.append('     &' + remaining)
        else:
            wrapped.append(' ' * indent + remaining)
    
    return '\n'.join(wrapped)
    
    return '\n'.join(wrapped)


def genfor(fortranfile, statements, encoding="utf-8", line_ending="\n", 
           format_style='fixed', max_line_length=None):
    """genfor(fortranfile, statements, [encoding], [line_ending], [format_style], [max_line_length])

    Write a list of macrofor statements/blocks to a Fortran file.
    
    - Resets and assigns unique labels for DO-loops and other control structures.
    - Replaces label placeholders (__LABEL_N__) with sequential numbers (100, 200, 300, ...).
    - Automatically wraps long lines based on format style.
    - Raises clear exceptions on error.
    - Optional: select encoding, line endings, and Fortran format.

    Args:
        fortranfile (str or Path): Output file path.
        statements (list of str): List of Fortran code blocks/lines.
        encoding (str): File encoding (default: 'utf-8').
        line_ending (str): Line ending (default: '\\n').
        format_style (str): 'fixed' (F77) or 'free' (F90+) (default: 'fixed').
        max_line_length (int): Maximum line length. If None, uses 72 for fixed, 132 for free.

    Returns:
        None. Writes the Fortran code to the specified file.

    Raises:
        RuntimeError: If the file cannot be written.

    Example:
        >>> genfor('myprog.f90', [
        ...     programm('main', [
        ...         dom('i', 1, 10, [equalf('x', 'i')]),
        ...         dom('j', 1, 5, [equalf('y', 'j')])
        ...     ])
        ... ], format_style='free')
    """
    from pathlib import Path
    
    try:
        # Reset label counter at the start of file generation
        _reset_label_counter()
        
        filepath = Path(fortranfile)
        # Ensure parent directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Join all statements with the specified line ending
        code = line_ending.join(str(stmt) for stmt in statements if stmt)
        
        # Replace label placeholders with sequential numbers (100, 200, 300, ...)
        code = _replace_label_placeholders(code)
        
        # Determine max line length based on format
        if max_line_length is None:
            max_line_length = 72 if format_style == 'fixed' else 132
        
        # Wrap long lines if needed
        if max_line_length > 0:
            code = _wrap_long_lines(code, max_line_length, format_style)
        
        # Write to file with proper encoding and line endings
        with open(filepath, "w", encoding=encoding, newline="") as f:
            f.write(code)
            if code and not code.endswith(line_ending):
                f.write(line_ending)
    except Exception as e:
        raise RuntimeError(f"Could not write Fortran file '{fortranfile}': {e}")
