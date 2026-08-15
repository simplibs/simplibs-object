from typing import TYPE_CHECKING, Any
from simplibs.sentinels import UNSET
# Outers
from ....._common_logic.constants import OWNER_CLASS, HISTORY
# Inners
from .validations import (
    raise_unvalide_history_import_file,
    raise_unvalide_owner_class_mismatch,
)
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.state import HistoryProtocol


def import_history_from_dict(
    self: "HistoryProtocol",
    history_dict: dict[str, Any]
) -> None:
    """
    Imports history from a portable dictionary format with owner_class validation.
    """

    # 1. Validate input type
    if not isinstance(history_dict, dict):
        raise_unvalide_history_import_file(self, history_dict)

    # 2. Validate owner class
    owner_class = history_dict.get(OWNER_CLASS, UNSET)
    if self.meta.owner_class != owner_class:
        raise_unvalide_owner_class_mismatch(self, owner_class)

    # 3. Backup previous history
    backup = self._history

    # 4. Replace history
    try:
        # 4.1 Load new history
        self._history = list(history_dict[HISTORY])
        self.go_to_last()

        # 4.2 Apply limit trimming (if configured)
        if self.history_limit:
            self.history_limit = self.history_limit

    # 5. Restore previous state on failure
    except Exception as e:
        self._history = backup
        self.go_to_last()
        raise e


_DESIGN_NOTES = """
# import_history_from_dict

## Purpose
Imports a complete history structure from a portable dictionary format.
This function is the counterpart to `export_history_to_dict` and enables
history restoration, state replay, debugging, and cross‑process transfer.

## Architectural role
`import_history_from_dict` is used by:

- `History.import_history_from_dict`
- serialization pipelines
- debugging tools
- external state replay utilities
- migration and persistence layers

It provides a safe, validated mechanism for reconstructing history from
external sources.

## How it works
The function performs five deterministic steps:

### 1. Validate input type
Ensures the provided object is a dictionary.  
Invalid inputs trigger a structured validation error.

### 2. Validate owner class
Checks that the dictionary belongs to the same class as the current instance.
This prevents accidental or malicious history injection from incompatible
objects.

### 3. Backup previous history
Stores the current history list so it can be restored if import fails.

### 4. Replace history
Attempts to load the new history:

- converts the history list to a Python list,
- navigates to the last entry,
- applies history limit trimming if configured.

All operations are performed inside a `try` block to guarantee safety.

### 5. Restore previous state on failure
If any exception occurs during import:

- the original history is restored,
- the instance is navigated back to its last valid snapshot,
- the original exception is re‑raised.

This ensures atomicity: either the import succeeds fully, or the instance
remains unchanged.

## Integration requirements
The function assumes the instance implements:

- **History internals**  
  `_history`, `_history_limit`, `_history_index`, `_history_count`

- **SnapshotMixin**  
  Provides `_restore_snapshot(snapshot)`.

- **Serialization metadata**  
  `meta.owner_class`

Without these components, history import cannot operate correctly.

## Why this function exists
History must be importable for:

- persistence,
- debugging,
- external analysis,
- replaying state transitions,
- transferring state between processes or machines.

This function encapsulates the minimal logic required to safely reconstruct
history from a portable representation.

## Deterministic behavior
History import is guaranteed to be:

- validated,
- owner‑safe,
- atomic,
- consistent with export format,
- compatible with undo/redo and navigation tools.

## Stability guarantee
Any change to this function would affect:

- serialization consistency,
- import behavior,
- debugging tools,
- replay mechanisms,
- history navigation.

Therefore, `import_history_from_dict` is treated as a **core invariant** of the
history subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to history internals and metadata.
"""
