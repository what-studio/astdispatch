# -*- coding: utf-8 -*-
"""
   astdispatch
   ~~~~~~~~~~~

   :mod:`singledispatch`-like API to visit all Python AST nodes.

   :copyright: (c) 2015 by What! Studio
   :license: BSD, see LICENSE for more details.
"""
import ast
try:
    from functools import singledispatch
except ImportError:
    from singledispatch import singledispatch


__version__ = '0.0.1'
__all__ = ['astdispatch']


class NodeVisitor(ast.NodeVisitor):
    """AST node visitor which wraps a single-dispatch function."""

    def __init__(self, dispatcher, *args, **kwargs):
        self.dispatcher = dispatcher
        self.args = args
        self.kwargs = kwargs

    def visit(self, node):
        rv = self.dispatcher(node, *self.args, **self.kwargs)
        super(NodeVisitor, self).visit(node)
        return rv


class NodeTransformer(ast.NodeTransformer, NodeVisitor):
    """AST node transformer which wraps a single-dispatch function."""

    pass


class ASTDispatch(object):
    """A callable object like a single-dispatch function but it visits AST
    nodes by :class:`NodeVisitor` or :class:`NodeTransformer`.
    """

    def __init__(self, default, visitor_class=NodeVisitor):
        self.dispatcher = singledispatch(default)
        self.visitor_class = visitor_class

    def __call__(self, node, *args, **kwargs):
        visitor = self.visitor_class(self.dispatcher, *args, **kwargs)
        return visitor.visit(node)

    def dispatch(self, cls):
        return self.dispatcher.dispatch(cls)

    def register(self, cls, func=None):
        return self.dispatcher.register(cls, func)

    @property
    def registry(self):
        return self.dispatcher.registry


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
