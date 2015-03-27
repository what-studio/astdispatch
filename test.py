# -*- coding: utf-8 -*-
import ast
from textwrap import dedent

from astunparse import unparse as astunparse
import inflection

from astdispatch import astdispatch


def transform(func, src_code, dest_code):
    node = ast.parse(dedent(src_code))
    func(node)
    return astunparse(node) == astunparse(ast.parse(dedent(dest_code)))


def test_transform():
    @astdispatch(transform=True)
    def fix_names(node):
        return node
    @fix_names.register(ast.Name)
    def fix_name(name):
        return ast.Name(id=inflection.underscore(name.id), ctx=name.ctx)
    @fix_names.register(ast.FunctionDef)
    def fix_func_def(func_def):
        return ast.FunctionDef(
            name=inflection.underscore(func_def.name),
            args=func_def.args,
            body=map(fix_names, func_def.body),
            decorator_list=map(fix_names, func_def.decorator_list))
    assert transform(fix_names, '''
    helloWorld = 'Hello, world!'
    def getFirst(manyCharacters):
        return manyCharacters[0]
    h = getFirst(helloWorld)
    ''', '''
    hello_world = 'Hello, world!'
    def get_first(many_characters):
        return many_characters[0]
    h = get_first(hello_world)
    ''')
