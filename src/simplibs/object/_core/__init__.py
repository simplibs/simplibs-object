_DESIGN_NOTES = """
# _core_logic Package Overview

The `_core_logic` package contains the internal building blocks that power the
SimpleObject system. Each sub-package focuses on a specific part of the object
infrastructure: constants, metadata, composite logic, and property generation.

This package does not re-export any components. All functionality is accessed
directly through the corresponding sub-packages.

---

## Sub-Packages

### 1. constant_methods
Implements the core logic used by `SimpleConstant` and `SimpleObject` for:
- type validation,
- user-defined validation,
- normalization,
- structured error handling.

This package defines the functional backbone of constant behavior.

---

### 2. metadata
Contains the metadata system used to describe and configure Simple classes.
Metadata defines:
- declared types,
- default values,
- inner structure,
- decomposability,
- logic and decomposition hooks.

Metadata is the central registry that binds user-defined class attributes with
runtime behavior.

---

### 3. object_methods
Implements the functional logic used by composite objects:
- parameter processing for `_logic`,
- composite value calculation,
- composite value decomposition,
- structured validation errors for object-level operations.

This package defines how composite objects behave at runtime.

---

### 4. property_builders
Generates instance-level properties for Simple classes:
- value getters and setters,
- inner element properties,
- composite property behavior,
- validation and normalization integration.

This package transforms metadata into actual Python properties on instances.

---

## Notes
- This package is internal and not intended for direct user interaction.
- Each sub-package is self-contained and exposes its own public API.
- The structure is designed for clarity, modularity, and predictable behavior.
"""
