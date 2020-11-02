"""
This type stub file was generated by pyright.
"""

from typing import cast

"""For neatly implementing static typing in packaging.

`mypy` - the static type analysis tool we use - uses the `typing` module, which
provides core functionality fundamental to mypy's functioning.

Generally, `typing` would be imported at runtime and used in that fashion -
it acts as a no-op at runtime and does not have any run-time overhead by
design.

As it turns out, `typing` is not vendorable - it uses separate sources for
Python 2/Python 3. Thus, this codebase can not expect it to be present.
To work around this, mypy allows the typing import to be behind a False-y
optional to prevent it from running at runtime and type-comments can be used
to remove the need for the types to be accessible directly during runtime.

This module provides the False-y guard in a nicely named fashion so that a
curious maintainer can reach here to read this.

In packaging, all static-typing related imports should be guarded as follows:

    from packaging._typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from typing import ...

Ref: https://github.com/python/mypy/issues/3216
"""
if False:
    ...
else:
    TYPE_CHECKING = False
if TYPE_CHECKING:
    ...
else:
    ...
