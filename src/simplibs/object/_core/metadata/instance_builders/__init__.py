_DESIGN_NOTES = """
# Instance Builders Package Overview

The `instance_builders` package contains the internal construction pipelines
responsible for generating all runtime instance classes used by the Simple
system. Each sub-package focuses on a specific structural mode: atomic,
composite, or fully compiled instance types.

This package does not re-export any components. All functionality is accessed
directly through the corresponding sub-packages.

---

## Sub-Packages

### 1. atom_class
Provides the builders for atomic instance classes:
- atomic initializer generation,
- root value setter creation,
- atomic base class definition,
- dynamic atomic class compilation.

Atomic classes represent leaf nodes with a single value.

---

### 2. composite_class
Provides the builders for composite instance classes:
- composite initializer generation,
- inner property creation,
- recalculation pipelines,
- dynamic composite class compilation.

Composite classes represent structured multi-node objects.

---

### 3. instance
Provides the unified instance factory:
- validation of class identity and mixins,
- structural mode resolution,
- base-class selection,
- dynamic class synthesis,
- mixin extension hooks,
- instance allocation and initialization.

This is the main entry point for creating runtime instances.

---

## Notes
- This package is internal and not intended for direct user interaction.
- Each builder sub-package is self-contained and exposes its own public API.
- The structure is designed for clarity, modularity, and predictable behavior.
"""
