from .export_history_to_dict import export_history_to_dict
from .import_history_from_dict import import_history_from_dict


_DESIGN_NOTES = """
# History Transfer Utilities

## Purpose
Provides import/export helpers used by the History mixin to serialize and
restore historical state. These utilities implement the core mechanics of:

- exporting history into a portable dictionary format,
- importing history with owner-class validation,
- restoring snapshots safely and atomically.

They form the transfer layer of the history subsystem and are used by
serialization pipelines, debugging tools, external replay utilities, and
cross‑process state transfer.

## Components

| Component                 | Type     | Description                                              |
| :------------------------ | :--------| :------------------------------------------------------- |
| `export_history_to_dict`  | Function | Exports history into a stable, portable dictionary.      |
| `import_history_from_dict`| Function | Imports history with validation and atomic restoration.  |

## Notes
- These utilities are internal and not part of the public API.
- They rely on History internals, SnapshotMixin, and serialization metadata.
- They are treated as core invariants of the history subsystem.
"""
