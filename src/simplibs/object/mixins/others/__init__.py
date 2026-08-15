_DESIGN_NOTES = """
# Others Package Overview

The `others` package groups every mixin that adds Simple-ecosystem-
specific behavior rather than implementing a standard Python protocol.
Where `dunders` covers hooks Python itself looks for, `others` covers
capabilities the Simple system defines on its own terms: immutable
change methods, numeric stepping, property ergonomics, and state
management.

This package does not re-export any components. All functionality is
accessed directly through the corresponding sub-packages.

---

## Sub-Packages

### 1. immutable
The "change without mutating" API for immutable instances:
- generic core methods (`with_constant`, `with_composite`, ...),
- per-inner generated setters (`with_<name>(value)`).

### 2. numerical
Safe, bounded numeric stepping via `Stepper` controllers:
- one stepper for an atom's own value,
- one stepper per inner of a composite.

### 3. properties
Ergonomic property-based access:
- direct attribute access to a composite's inners,
- shortcut properties over frequently used metadata fields.

### 4. state
State management for mutable instances:
- remembering construction-time state,
- dirty tracking,
- full undo/redo history,
- runtime read-only locking.

---

## Notes
- This package is internal and not intended for direct user interaction.
- Each sub-package is self-contained and exposes its own public API.
- `core_mixins` is deliberately kept at the package root rather than
  under `others`, since it is shared infrastructure used by both
  `dunders` and `others` alike, not a sibling category of either.
"""
