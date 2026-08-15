from typing import TYPE_CHECKING, Any
# Outers
from ..._common_logic.immutability import with_any
from ...core_mixins import Infrastructure
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.interfaces import CallProtocol


class Call(Infrastructure):
    """
    Mixin providing support for calling an instance like a function
    (`obj(...)`).

    This mixin acts as syntactic sugar over the immutable API. It allows
    changes to be expressed using tuple notation:

        obj("a", 10)
        obj(("a", 10), ("b", 20))
        obj((("a", 10), ("b", 20)))

    Logic:
    - All processing is delegated to the internal `with_any` engine.
    - Adds no validation or logic of its own.
    - Universal for both mutable and immutable objects.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - CALL
    # ----------------------------------------

    def __call__(
        self: "CallProtocol",
        *changes: Any,
        **kwargs: Any
    ) -> "CallProtocol":
        """
        Allows the instance to be called like a function.

        Supported forms:
            obj("a", 10)
            obj(("a", 10))
            obj(("a", 10), ("b", 20))
            obj((("a", 10), ("b", 20)))

        If keyword arguments are used, they are converted to tuple form.
        """

        # 1. If keyword arguments are used → convert them to tuple form
        if kwargs:
            # kwargs always take the form of constants
            changes = tuple(kwargs.items())

        # 2. If a single tuple was passed → normalize the shape
        elif len(changes) == 1 and isinstance(changes[0], tuple):
            changes = changes[0]

        # 3. Delegate to the engine
        return with_any(self, changes)


_DESIGN_NOTES = """
# Call

## Purpose
Lets a Simple instance be called like a function — `obj("a", 10)` — as a
compact, expressive shortcut for producing a changed instance. Think of
it as a one-line alternative to writing out an explicit "with a=10" call.

> For newcomers: this is the classic Python "make objects callable"
> trick (`__call__`), the same mechanism functions and lambdas use under
> the hood. Here it's repurposed as sugar for expressing value changes.

## Compatibility
- No compatibility flags — works uniformly for mutable and immutable
  instances, since it delegates entirely to `with_any`, which already
  knows how to handle both.

## Logic
- No logic of its own beyond normalizing the call's argument shape:
  keyword args become tuple pairs, a single passed-in tuple is unwrapped,
  everything else is passed through as-is.
- All actual work — validation, applying changes, returning a new vs.
  mutated instance — happens inside `with_any`. This mixin exists purely
  to give that engine a friendlier call syntax.

## Notes
- Because this is "just" a syntactic front end, any change to
  `with_any`'s underlying semantics (e.g. immutable-vs-mutable behavior)
  is automatically reflected here without needing changes to this file.
- Inherits from `Infrastructure` rather than `SimpleMixin` directly,
  since it needs the shared plumbing that mixin provides for
  reading/applying changes.
"""
