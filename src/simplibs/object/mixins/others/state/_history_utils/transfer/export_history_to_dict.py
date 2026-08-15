from typing import TYPE_CHECKING
# Outers
from ....._common_logic.constants import OWNER_CLASS, HISTORY
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.state import HistoryProtocol
    from ......_core.protocols.alias_typings import HistoryDict


def export_history_to_dict(
    self: "HistoryProtocol"
) -> "HistoryDict":
    """
    Exports the history into a portable dictionary format:
        { _owner_class: ..., history: ( (timestamp, [values...]), ... ) }
    """
    return {
        OWNER_CLASS: self.meta.owner_class,
        HISTORY: self.history
    }


_DESIGN_NOTES = """
# export_history_to_dict

## Purpose
Exports the entire history of the instance into a portable, serialization‑friendly
dictionary format. This representation is used for:

- persistence,
- debugging,
- external tooling,
- state replay,
- cross‑process or cross‑machine transfer.

The exported structure is stable, deterministic, and independent of internal
implementation details.

## Architectural role
`export_history_to_dict` is used by:

- `History.export_history_to_dict`
- serialization pipelines
- debugging tools
- history import/export utilities
- snapshot diffing and replay mechanisms

It provides a clean, minimal, and predictable representation of the history.

## How it works
The function performs a single deterministic step:

### 1. Build dictionary representation
Creates a dictionary containing:

- `_owner_class` — the class that owns the history (used for validation during import)
- `history` — a tuple of history entries, each entry being:
  - a timestamp (`datetime`)
  - a snapshot tuple of raw values

This structure is fully portable and safe for serialization.

## Integration requirements
The function assumes the instance implements:

- **History internals**  
  `_history`, `_history_index`, `_history_count`

- **Serialization metadata**  
  `meta.owner_class`

Without these components, history export cannot operate correctly.

## Why this function exists
History must be exportable for:

- debugging,
- persistence,
- external analysis,
- replaying state transitions,
- transferring state between processes or machines.

This function encapsulates the minimal logic required to produce a stable,
portable representation.

## Deterministic behavior
The exported dictionary is guaranteed to be:

- stable across runs,
- independent of internal representation,
- safe for serialization,
- compatible with import pipelines,
- predictable for debugging and diffing.

## Stability guarantee
Any change to this function would affect:

- serialization consistency,
- import behavior,
- debugging tools,
- replay mechanisms.

Therefore, `export_history_to_dict` is treated as a **core invariant** of the
history subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to history internals and metadata.
"""
