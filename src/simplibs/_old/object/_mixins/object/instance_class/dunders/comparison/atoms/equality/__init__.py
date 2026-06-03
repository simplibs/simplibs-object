from .Eq import EqMixin

__all__ = (
    "EqMixin",
)


__DOCT__ = """
## `comparison/equality/`

> **Subgroup purpose:**
> The equality pair. `__eq__` and `__ne__` define what it means for two objects to be
> "the same value" (as opposed to `is`, which tests identity). In Python 3, `__ne__`
> automatically returns `not self.__eq__(other)` if you only define `__eq__`, so you
> rarely need to define both.
"""