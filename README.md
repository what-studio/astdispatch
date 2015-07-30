astdispatch
===========

[singledispatch][]-like API to visit all Python AST nodes.

[singledispatch]: https://docs.python.org/3/library/functools.html#functools.singledispatch

[![Build Status]
(https://travis-ci.org/what-studio/astdispatch.svg)]
(https://travis-ci.org/what-studio/astdispatch)
[![Coverage Status]
(https://img.shields.io/coveralls/what-studio/astdispatch.svg)]
(https://coveralls.io/r/what-studio/astdispatch)

```python
@astdispatch(transform=True)
def rewrite_name(node):
    return node

@rewrite_name.register(ast.Name)
def _(node):
    return ast.copy_location(ast.Subscript(
        value=ast.Name(id='data', ctx=ast.Load()),
        slice=ast.Index(value=ast.Str(s=node.id)),
        ctx=node.ctx), node)
```

Written by [Heungsub Lee] at [What! Studio] in [Nexon], and
distributed under the [BSD 3-Clause] license.

[Heungsub Lee]: http://subl.ee/
[What! Studio]: https://github.com/what-studio
[Nexon]: http://nexon.com/
[BSD 3-Clause]: http://opensource.org/licenses/BSD-3-Clause
