from macrofor.ast import Subroutine, Assignment, Call, If, Module
from macrofor.codegen import generate_subroutine, generate_module


def test_generate_simple_subroutine():
    sub = Subroutine(name='step', args=['u', 'dt'])
    sub.body.append(Assignment(target='u(i)', expr='u(i) + dt'))
    sub.body.append(Call(name='setup', args=['n']))
    txt = generate_subroutine(sub)
    assert 'subroutine step(u, dt)' in txt
    assert 'u(i) = u(i) + dt' in txt
    assert 'call setup(n)' in txt


def test_generate_module_with_if():
    mod = Module(name='heat')
    sub = Subroutine(name='cond', args=[])
    ifnode = If(condition='x .gt. 0')
    ifnode.then_body.append(Assignment(target='y', expr='1'))
    ifnode.else_body.append(Assignment(target='y', expr='0'))
    sub.body.append(ifnode)
    mod.body.append(sub)
    out = generate_module(mod)
    assert 'module heat' in out
    assert 'if (x .gt. 0) then' in out
    assert 'end if' in out or 'end if' in out
