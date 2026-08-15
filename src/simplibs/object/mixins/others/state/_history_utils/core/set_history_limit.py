from typing import TYPE_CHECKING
# Outers
from .validations import raise_history_limit_not_positive_integer
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.state import HistoryProtocol


def set_history_limit(
    self: "HistoryProtocol",
    value: int
) -> None:
    """
    Sets the maximum allowed size of the history list.
    """

    # 1. Validate value
    if not isinstance(value, int) or value < 1:
        raise_history_limit_not_positive_integer(self, value)

    # 2. Adjust history to the new limit
    if self._history_count > value:
        del self._history[:(self._history_count - value)]
        self._history_count = len(self._history)
        self._history_index = self._history_count - 1

    # 3. Store limit
    self._history_limit = value


_DESIGN_NOTES = """
# set_history_limit

## Purpose
Sets a maximum size for the history list and trims older entries if necessary.
This function ensures that history tracking remains memory‑efficient and
predictable, especially for long‑running or frequently mutated objects.

## Architectural role
`set_history_limit` is used by:

- the `History.history_limit` property setter,
- initialization routines,
- debugging tools,
- import/export pipelines (when restoring history limits).

It provides a deterministic mechanism for bounding the history size.

## How it works
The function performs three deterministic steps:

### 1. Validate value
Ensures the limit is a positive integer (`value >= 1`).  
Invalid values trigger a structured validation error.

### 2. Trim history if needed
If the current history contains more entries than the new limit:
- the oldest entries are removed,
- `_history_count` is updated,
- `_history_index` is set to the last valid entry.

This guarantees that the history always respects the configured limit.

### 3. Store limit
Updates `_history_limit` with the validated value.

## Integration requirements
The function assumes the instance implements:

- **History internals**  
  `_history`, `_history_limit`, `_history_count`, `_history_index`

- **SnapshotMixin**  
  History entries contain snapshot tuples created by `_build_snapshot()`.

Without these components, the history subsystem cannot enforce limits correctly.

## Why this function exists
History tracking can grow indefinitely if not bounded.  
A configurable limit allows:

- predictable memory usage,
- stable performance,
- safe long‑term operation,
- controlled undo/redo depth.

This function encapsulates the trimming logic in a single, stable utility.

## Deterministic behavior
History trimming is guaranteed to be:

- stable,
- predictable,
- index‑safe,
- consistent across all history operations.

This determinism is essential for undo/redo, navigation, and debugging.

## Stability guarantee
Any change to this function would affect:

- undo/redo behavior,
- navigation correctness,
- history import/export,
- initialization behavior.

Therefore, `set_history_limit` is treated as a **core invariant** of the
history subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to history internals.
"""
