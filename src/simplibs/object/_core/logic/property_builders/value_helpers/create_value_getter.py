from typing import Any, TYPE_CHECKING, Callable
from operator import attrgetter
# Annotations
if TYPE_CHECKING:
    from ....protocols.metadata import SimpleMetadataLike
    from ....protocols.instance import SimpleInstanceLike
    from ....protocols.alias_typings import PathTuple


def create_value_getter(
    meta: "SimpleMetadataLike",
    path: "PathTuple | None",
) -> Callable:
    """Creates a getter for root or inner value access."""

    # Root getter
    if path is None:
        def getter(self: "SimpleInstanceLike") -> Any:
            return self._value

    # Inner getter
    else:
        get_inner_instance = attrgetter(*path)

        def getter(self: "SimpleInstanceLike") -> Any:
            return get_inner_instance(self).value

    getter.__annotations__ = {"return": meta.value_type}
    return getter


_DESIGN_NOTES = """
# create_value_getter

## Purpose
Generates a unified getter function for both root-level and inner-level value
properties. The getter is intentionally identical for atomic and composite
instances: it always returns the current normalized value stored in the instance.

## Behavior
- If `path is None`, the getter returns `self._value`.
- If `path` is provided, the getter resolves the inner instance using
  `operator.attrgetter` and returns its `.value`.
- The return type annotation is injected dynamically based on metadata.

## Notes
- Getter logic is intentionally minimal and side-effect free.
- Composite vs atomic behavior is handled entirely in the setter; the getter
  remains uniform across all instance types.
- Using `attrgetter` avoids repeated attribute traversal and keeps the getter
  fast and allocation-free.
"""