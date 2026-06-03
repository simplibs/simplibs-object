from .Add import AddMixin
from .Div import DivMixin
from .Floordiv import FloordivMixin
from .Mod import ModMixin
from .Mul import MulMixin
from .Pow import PowMixin
from .Sub import SubMixin

__all__ = (
    "AddMixin",
    "DivMixin",
    "FloordivMixin",
    "ModMixin",
    "MulMixin",
    "PowMixin",
    "SubMixin",
)


__DOCT__ = """
## `numeric/arithmetic/`

> **Subgroup purpose:**
> Binary arithmetic operators. Python calls the left operand's method first; if it returns
> `NotImplemented`, Python tries the right operand's reflected method (`__radd__`, etc.).
"""