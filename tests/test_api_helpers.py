from macrofor import api


def test_callf_and_subroutinef():
    s = api.callf('foo', ['a', 'b'])
    assert s == 'call foo(a, b)'
    h = api.subroutinef('mysub', ['n', 'm'])
    # subroutinef now includes F77-compatible header comments
    assert 'c\nc SUBROUTINE mysub\nc' in h
    assert 'subroutine mysub(n, m)' in h


def test_equalf_and_declaref():
    eq = api.equalf('x', 'y+1')
    assert eq == 'x = y+1'
    dec = api.declaref('real', ['a', 'b'])
    assert dec.startswith('real') and 'a' in dec


def test_io_and_format():
    r = api.readf('5', None, ['i', 'j'])
    assert 'read (5) i, j' in r
    w = api.writef('6', 'fmt', ['x'])
    assert w == 'write (6, fmt) x'
    # Reset label counter before testing formatf
    api._reset_label_counter()
    fmt = api.formatf(['I5', 'F10.2'])
    assert 'format' in fmt and 'I5' in fmt and '__LABEL_1__' in fmt


def test_control_flow():
    d = api.dof(None, 'i', 1, 'n')
    assert 'do i = 1, n' in d
    it = api.if_then_f('x .gt. 0')
    assert it == 'if (x .gt. 0) then'
    g = api.if_goto_f('i .eq. 0', '100')
    assert g == 'if (i .eq. 0) goto 100'
