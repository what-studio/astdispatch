# -*- coding: utf-8 -*-
import ast
import base64
import re
from textwrap import dedent

from astunparse import unparse as astunparse

from astdispatch import astdispatch


def parse(dirty_code):
    return ast.parse(dedent(dirty_code))


def to_transform(src_code, dest_code, func, *args, **kwargs):
    """Used to assert node transformation by a source and a destination code.

    ::

       assert to_transform('x = 10 ** 2', 'x = 100', inliner)

    """
    node = parse(src_code)
    func(node)
    return astunparse(node) == astunparse(parse(dest_code))


def test_transform():
    def mangle_id(id_):
        b64_id = base64.b64encode(id_.encode()).decode()
        return re.sub(r'[+/=]', '', b64_id)[:6].lower()
    @astdispatch(transform=True)
    def mangle(node):
        return node
    @mangle.register(ast.Name)
    def mangle_name(name):
        return ast.Name(id=mangle_id(name.id), ctx=name.ctx)
    @mangle.register(ast.FunctionDef)
    def mangle_func_def(func_def):
        return ast.FunctionDef(name=mangle_id(func_def.name),
                               args=func_def.args, body=func_def.body,
                               decorator_list=func_def.decorator_list)
    @mangle.register(ast.arg)
    def mangle_arg(arg):
        return ast.arg(arg=mangle_id(arg.arg), annotation=arg.annotation)
    assert to_transform('''
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
    ''', mangle)


def test_args():
    @astdispatch
    def collect_names(node, add_name):
        pass
    @collect_names.register(ast.FunctionDef)
    def collect_func_name(func_def, add_name):
        add_name(func_def.name)
    @collect_names.register(ast.ClassDef)
    def collect_cls_name(cls_def, add_name):
        add_name(cls_def.name)
    @collect_names.register(ast.Assign)
    def collect_var_name(assign, add_name):
        for expr in assign.targets:
            _collect_var_names(expr, add_name)
    @astdispatch
    def _collect_var_names(node, add_name):
        pass
    @_collect_var_names.register(ast.Name)
    def _collect_var_name(name, add_name):
        add_name(name.id)
    names = set()
    collect_names(parse('''
        x = 123
        y = 456
        a, b = -1, +1
        def f():
            pass
        class C(object):
            pass
    '''), names.add)
    assert names == set(['x', 'y', 'a', 'b', 'f', 'C'])
