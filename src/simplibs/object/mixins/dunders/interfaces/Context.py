from typing import Literal, TYPE_CHECKING
from types import TracebackType
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.interfaces import ContextProtocol


class ContextManager(SimpleMixin):
    """
    Mixin providing basic support for the context manager protocol
    (`with obj:`).

    This mixin allows an instance to be used in a `with` construct
    without performing any side effects. It is fully universal — it
    works for mutable and immutable objects, atoms and composites alike,
    since it never changes the instance's state.

    Behavior:
    - `__enter__` returns the instance itself.
    - `__exit__` does not suppress exceptions (returns False), so any
      errors propagate normally.

    This mixin serves purely as a syntactic API extension and does not
    interfere with value logic, snapshots, mutability, or immutable mode.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - ENTER / EXIT
    # ----------------------------------------

    def __enter__(
        self: "ContextProtocol"
    ) -> "ContextProtocol":
        """
        Returns the instance on entering the context.

        Enables the construct:
            with obj as x:
                ...

        Without any change to the instance's state.
        """
        return self

    def __exit__(
        self: "ContextProtocol",
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> Literal[False]:
        """
        Ends the context block.

        Returns False, meaning any exceptions are NOT suppressed and
        propagate normally. The mixin performs no cleanup or state
        change — it is purely syntactic.
        """
        return False


_DESIGN_NOTES = """
# ContextManager

## Purpose
Lets a Simple instance be used in a `with obj:` block. On its own this
does nothing functional — no cleanup, no side effects — it exists so an
instance can participate in context-manager-based APIs or read naturally
in code that scopes a variable to a block.

> For newcomers: `__enter__`/`__exit__` are the two methods Python looks
> for when you write `with x:`. Here they're intentionally inert — this
> is a "no-op" context manager, not a resource-management one like a file
> handle.

## Compatibility
- No compatibility flags — safe for every instance kind, precisely
  because it never touches state.

## Logic
- `__enter__` just returns `self`, enabling `with obj as x:` to bind `x`
  to the same instance.
- `__exit__` always returns `False`, so any exception raised inside the
  `with` block propagates as normal — this mixin never swallows errors.

## Notes
- Purely syntactic — does not create a snapshot, does not lock the
  instance, does not interact with mutability at all.
- If a future use case needs an actual scoped effect (e.g. temporarily
  freezing an instance), that belongs in a separate, more specific mixin
  rather than being added here.
"""
