from .Dir import DirMixin

__all__ = (
    "DirMixin",
)


__DOCT__ = """
## `attributes/dir/`

> **Subgroup purpose:**
> Controls what `dir(obj)` returns — the list of "visible" attributes and methods.
> Especially important when you use `__getattr__` to generate dynamic attributes,
> because those won't appear in `dir()` unless you add them here.
"""