# -*- coding: utf-8 -*-
import ast
from textwrap import dedent

from astunparse import unparse as astunparse

from astdispatch import astdispatch


def transform(func, src_code, dest_code):
    node = ast.parse(dedent(src_code))
    func(node)
    return astunparse(node) == astunparse(ast.parse(dedent(dest_code)))


def test_transform():
    def mangle_id(id_):
        import base64
        import re
        return re.sub(r'[+/=]', '', base64.b64encode(id_))[:6].lower()
    @astdispatch(transform=True)
    def mangle(node):
        return node
    @mangle.register(ast.Name)
    def mangle_name(name):
        return ast.Name(id=mangle_id(name.id), ctx=name.ctx)
    @mangle.register(ast.FunctionDef)
    def mangle_fdef(fdef):
        return ast.FunctionDef(name=mangle_id(fdef.name),
                               args=fdef.args, body=fdef.body,
                               decorator_list=fdef.decorator_list)
    assert transform(mangle, '''
    a = 123
    b = 456
    c = a + b
    def pow(x, y):
        return x ** y
    d = pow(a, b)
    ''', '''
    yq = 123
    yg = 456
    yw = (yq + yg)
    def cg93(ea, eq):
        return (ea ** eq)
    za = cg93(yq, yg)
    ''')
