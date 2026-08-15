_DESIGN_NOTES = """
# Dunders Package Overview

The `dunders` package groups every mixin that implements a standard
Python "dunder" (double-underscore) protocol — the hooks Python itself
looks for to make an object iterable, comparable, callable, picklable,
printable, and so on. Each sub-package covers one coherent protocol
family.

This package does not re-export any components. All functionality is
accessed directly through the corresponding sub-packages.

---

## Sub-Packages

### 1. collections
Dict-like and iterable behavior over a composite's direct inners:
- iteration, reversed iteration, extended `dir()`,
- item access, assignment, containment, length,
- a combined bundle mixin for the full surface.

### 2. comparison
Value-based equality and magnitude ordering:
- `__eq__` / `__hash__`, mutability-aware hashing,
- `__lt__` / `__le__` / `__gt__` / `__ge__`.

### 3. generics
Generic-style subscript syntax for typing/IDE purposes:
- `__class_getitem__` fallback, no runtime effect.

### 4. interfaces
General-purpose Python object protocols:
- calling an instance like a function (`__call__`),
- context-manager support (`__enter__` / `__exit__`).

### 5. lifecycles
Object lifecycle protocols built on a shared snapshot foundation:
- `copy` / `deepcopy` support,
- full `pickle` support (`__reduce__`, `__getstate__`, `__setstate__`),
- a combined bundle mixin for both.

### 6. numeric
The full range of Python numeric protocols:
- binary and unary arithmetic, bitwise operations,
- in-place arithmetic,
- conversion to native Python numeric types.

### 7. representation
How an instance presents itself as text, bytes, and boolean:
- value-like `__repr__` / `__str__` (opt-in, constant-only),
- `format()` / `__format__` / `__bytes__` / `__bool__`.

---

## Notes
- This package is internal and not intended for direct user interaction.
- Each sub-package is self-contained and exposes its own public API.
- Mixins here implement Python protocols specifically — see `others` for
  mixins that add ecosystem-specific behavior instead.
"""
