# -*- coding: utf-8 -*-
"""
   astdispatch
   ~~~~~~~~~~~

   :mod:`singledispatch`-like API to visit all Python AST nodes.

   :copyright: (c) 2015 by What! Studio
   :license: BSD, see LICENSE for more details.
"""
import ast
from singledispatch import singledispatch


__version__ = '0.0.1-dev'
__all__ = ['astdispatch']


class NodeVisitor(ast.NodeVisitor):
    """AST node visitor which wraps a single-dispatch function."""

    def __init__(self, dispatch, *args, **kwargs):
        self.dispatch = dispatch
        self.args = args
        self.kwargs = kwargs

    def visit(self, node):
        self.dispatch(node, *self.args, **self.kwargs)
        super(NodeVisitor, self).visit(node)


class NodeTransformer(ast.NodeTransformer, NodeVisitor):
    """AST node transformer which wraps a single-dispatch function."""

    pass


class ASTDispatch(object):

    def __init__(self, default, visitor_class=NodeVisitor):
        self.dispatch = singledispatch(default)
        self.visitor_class = visitor_class

    def __call__(self, node, *args, **kwargs):
        visitor = self.visitor_class(self.dispatch, *args, **kwargs)
        return visitor.visit(node)

    def register(self, node_class):
        return self.dispatch.register(node_class)

    def dispatch(self, node_class):
        return self.dispatch.dispatch(node_class)


def astdispatch(func=None, transform=False):
    """AST node visiting function decorator.

    :param transform: use node transformer or not.  (default: ``False``)

    """
    def decorator(func, transform=transform):
        visitor_class = NodeTransformer if transform else NodeVisitor
        return ASTDispatch(func, visitor_class=visitor_class)
    if func is None:
        return decorator
    return decorator(func)
