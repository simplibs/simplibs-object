_DESIGN_NOTES = """
# Core Mixins Utilities Overview

The `_utils` package aggregates foundational helper subsystems used by the
core mixins. Each sub-package focuses on a specific structural domain:
node traversal, serialization, and snapshot comparison.

This package does not re-export any components. All functionality is accessed
directly through the corresponding sub-packages.

---

## Sub-Packages

### 1. nodes_tuple
Provides structural traversal utilities:
- collection of node data,
- canonical tuple construction,
- foundational support for snapshot creation and immutability pipelines.

These utilities define the stable ordering of nodes inside every instance.

---

### 2. serialization
Provides import/export utilities:
- dictionary serialization,
- dictionary-based reconstruction,
- partial constant updates.

These functions form the backbone of the Serialization mixin.

---

### 3. snapshot
Provides snapshot utilities:
- structural diffing,
- compatibility validation,
- debugging support.

Snapshots are used across immutability, history tracking, and debugging tools.

---

## Notes
- This package is internal and not intended for direct user interaction.
- Each sub-package is self-contained and exposes its own public API.
- The structure is designed for clarity, modularity, and predictable behavior.
"""
