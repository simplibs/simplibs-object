_DESIGN_NOTES = """
# _history_utils Package Overview

The `_history_utils` package contains the internal helper subsystems used by
the History mixin. Each sub‑package focuses on a specific operational domain:
core history mechanics, navigation utilities, and import/export pipelines.

This package does not re‑export any components. All functionality is accessed
directly through the corresponding sub‑packages.

---

## Sub‑Packages

### 1. core
Provides the foundational history operations:
- snapshot creation and recording,
- snapshot lookup by index or timestamp,
- history limit enforcement.

These utilities form the backbone of the History mixin’s state‑management logic.

---

### 2. navigations
Implements navigation helpers:
- undo and redo traversal,
- jumping to specific history entries,
- restoring the latest snapshot.

These functions provide the operational navigation API of the History mixin.

---

### 3. transfer
Implements import/export utilities:
- exporting history into dictionary structures,
- importing history with owner‑class validation,
- safe and atomic restoration of historical state.

These utilities support persistence, debugging, external tooling, and
cross‑process state transfer.

---

## Notes
- This package is internal and not intended for direct user interaction.
- Each sub‑package is self‑contained and exposes its own public API.
- The structure is designed for clarity, modularity, and predictable behavior.
"""
