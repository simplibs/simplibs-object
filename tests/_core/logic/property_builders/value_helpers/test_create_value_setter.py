from typing import Any, TYPE_CHECKING, Callable
from operator import attrgetter
# Outers
from ...object_methods.validations import raise_class_not_decomposeable
# Inners
from .validations import raise_locked_value_error
# Annotations
if TYPE_CHECKING:
    from ....protocols.metadata import SimpleMetadataLike
    from ....protocols.instance import SimpleInstanceLike
    from ....protocols.alias_typings import PathTuple


def create_value_setter(
    meta: "SimpleMetadataLike",
    is_constant: bool = False,
    path: "PathTuple | None" = None,
) -> Callable:
    """Creates a setter for root or inner value properties (atomic or composite)."""

    # 1. Prepare inner resolver
    get_inner = attrgetter(*path) if path is not None else None

    # 2. Create setter
    def setter(self: "SimpleInstanceLike", value: Any) -> None:

        # 2.1 Locked instance cannot be modified
        if self._locked:
            raise_locked_value_error(value, self.__class__.__name__)

        # 2.2 Composite setter requires decomposeable metadata
        if not is_constant and not meta.is_decomposeable:
            raise_class_not_decomposeable(meta)

        # 2.3 Resolve target instance (root or inner)
        instance = get_inner(self) if get_inner is not None else self

        # 2.4 Write value and propagate recalculation upwards
        # noinspection PyProtectedMember
        instance._root_value_setter(value, recalculate_up=True)

        # 2.5 Recalculate inners for composite values
        if not is_constant:
            # noinspection PyProtectedMember
            instance._recalculate_inners()

        # 2.6 Log only root-level value changes
        if path is None:
            from simplibs.object.settings.logging import log_value_event
            log_value_event(self.__class__, value, event="set")

    # 3. Add annotations
    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # 4. Return setter
    return setter


_DESIGN_NOTES = """
# create_value_setter

## Purpose
Generates a unified setter function for both root-level and inner-level value
properties. The setter encapsulates all mutation semantics for atomic and
composite instances, including normalization, decomposition, recalculation, and
logging.

## Behavior
- `is_constant=True`:
  - Treats the value as atomic.
  - Writes the normalized value via `_root_value_setter`.
  - Triggers upward recalculation (`recalculate_up=True`).
- `is_constant=False`:
  - Treats the value as composite.
  - Requires `meta.is_decomposeable=True` (otherwise raises
    `raise_class_not_decomposeable`).
  - Writes the root value via `_root_value_setter`.
  - Calls `_recalculate_inners()` to distribute the value into inner nodes.

- `path is None`:
  - Operates on the root instance (`self`).
  - Logs the value change via `log_value_event`.

- `path is not None`:
  - Resolves an inner instance using `attrgetter(*path)`.
  - Operates on that inner instance without logging.

## Notes
- Locking (`self._locked`) prevents any mutation once the instance is frozen.
- Composite behavior is strictly guarded by metadata (`is_decomposeable`).
- Logging is intentionally limited to root-level changes to avoid noise from
  inner recalculations.
- The setter is side-effectful by design: it updates value, triggers recalculation,
  and optionally logs the event.
"""