# -*- coding: utf-8 -*-
import ast
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


def test_singledispatch_like():
    @astdispatch
    def foo(node):
        pass
    foo.register(ast.If, foo)
    foo.register(ast.For, foo)
    foo.dispatch(ast.If) is foo
    foo.dispatch(ast.For) is foo
    assert foo.registry[ast.If] is foo
    assert foo.registry[ast.For] is foo


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


def test_transform():
    @astdispatch(transform=True)
    def rewrite_name(node):
        return node
    @rewrite_name.register(ast.Name)
    def _(node):
        return ast.copy_location(ast.Subscript(
            value=ast.Name(id='data', ctx=ast.Load()),
            slice=ast.Index(value=ast.Str(s=node.id)),
            ctx=node.ctx), node)
    assert to_transform('''
        a = 123
        b = 456
        c = a + b
    ''', '''
        data['a'] = 123
        data['b'] = 456
        data['c'] = data['a'] + data['b']
    ''', rewrite_name)
