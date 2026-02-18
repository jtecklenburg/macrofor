from macrofor import api as mf


def test_if_then_m():
    result = mf.if_then_m('x .gt. 0', ['a = 1', 'b = 2'])
    assert 'if (x .gt. 0) then' in result
    assert 'a = 1' in result
    assert 'b = 2' in result
    assert 'end if' in result
    # Note: indentation happens during genfor(), not in the raw output
    # The raw output from if_then_m will have minimal formatting


def test_if_then_else_m():
    then_body = ['y = 1']
    else_body = ['y = 0']
    result = mf.if_then_else_m('z .eq. 0', then_body, else_body)
    assert 'if (z .eq. 0) then' in result
    assert 'else' in result
    assert 'y = 1' in result
    assert 'y = 0' in result
    assert 'end if' in result


def test_programm():
    body = ['implicit none', 'integer :: i', 'i = 1']
    result = mf.programm('myprogram', body)
    assert 'program myprogram' in result
    assert 'implicit none' in result
    assert 'i = 1' in result
    assert 'end' in result


def test_subroutinem():
    body = ['integer :: n', 'n = 10', 'call helper(n)']
    result = mf.subroutinem('mysub', ['x', 'y'], body)
    assert 'subroutine mysub(x, y)' in result
    assert 'n = 10' in result
    assert 'end' in result


def test_functionm():
    body = ['integer :: res', 'res = a + b', 'return']
    result = mf.functionm('integer', 'myfunc', ['a', 'b'], body)
    assert 'integer function myfunc(a, b)' in result
    assert 'res = a + b' in result
    assert 'end' in result


def test_dom():
    mf._reset_label_counter()
    body = ['a(i) = i', 'b(i) = i * 2']
    result = mf.dom('i', 1, 10, body)
    # Correct Fortran syntax: NO comma after label
    assert 'do __LABEL_1__ i=1, 10' in result
    assert 'a(i) = i' in result
    assert '__LABEL_1__ continue' in result


def test_dom_with_step():
    mf._reset_label_counter()
    body = ['x(i) = x(i) + 1']
    result = mf.dom('i', 1, 100, body, step=2)
    # Correct Fortran syntax: NO comma after label
    assert 'do __LABEL_1__ i=1, 100, 2' in result
    assert 'x(i) = x(i) + 1' in result
    assert '__LABEL_1__ continue' in result


def test_openm():
    body = ['read(10) a, b', 'print *, a, b']
    result = mf.openm('10', 'input.txt', 'old', body)
    assert "open(unit=10, file='input.txt', status='old')" in result
    assert 'read(10) a, b' in result
    assert 'close(unit=10)' in result


def test_readm():
    mf._reset_label_counter()
    result = mf.readm('5', ['I5', 'F10.2'], ['i', 'x'])
    assert 'read(5, __LABEL_1__) i, x' in result
    assert '__LABEL_1__ format(I5, F10.2)' in result


def test_writem():
    mf._reset_label_counter()
    result = mf.writem('6', ['I3', 'A'], ['iter', 'msg'])
    assert 'write(6, __LABEL_1__) iter, msg' in result
    assert '__LABEL_1__ format(I3, A)' in result


def test_commonm():
    result = mf.commonm('data', ['a', 'b', 'c'])
    assert 'common /data/ a, b, c' in result


def test_declarem():
    result = mf.declarem('real', ['x', 'y', 'z'])
    assert 'real x, y, z' in result


def test_nested_if_in_program():
    """Test combining macro functions."""
    if_block = mf.if_then_m('n .gt. 0', ['i = n', 'call compute(i)'])
    program_body = [
        'implicit none',
        'integer :: n, i',
        if_block
    ]
    result = mf.programm('nested_prog', program_body)
    assert 'program nested_prog' in result
    assert 'if (n .gt. 0) then' in result
    assert 'i = n' in result
    assert 'end if' in result
    assert 'end' in result
