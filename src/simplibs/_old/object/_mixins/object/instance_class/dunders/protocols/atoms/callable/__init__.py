from .Call import CallMixin

__all__ = (
    "CallMixin",
)


__DOCT__ = """
# GROUP: `callable/`

> **Group purpose:**
> Makes an object *callable* — usable with parentheses as if it were a function.
> This is the foundation of functors, decorators-as-classes, memoization objects,
> and any pattern where state should persist across calls.
"""