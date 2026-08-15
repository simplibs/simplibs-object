from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from ._core.metadata import SimpleMeta
# Annotations
if TYPE_CHECKING:
    from ._core.protocols.metadata import SimpleMetadataLike


class SimpleBase(metaclass=SimpleMeta):
    """
    Root base class for all Simple system declarative classes.

    This class provides a unified identity for both constants and composite
    objects. It establishes the connection to the `SimpleMeta` metaclass and
    exposes the shared metadata interface used throughout the system.
    """

    # ----------------------------------------------------------------------
    # 1) Structural foundation
    # ----------------------------------------------------------------------

    # Slots improve memory layout and runtime performance.
    # All subclasses must define their own slots to preserve this benefit.
    __slots__ = ()

    # Metadata placeholder for system base classes.
    # Declarative user classes receive computed metadata via SimpleMeta.
    __metadata__: "SimpleMetadataLike" = UNSET


_DESIGN_NOTES = """
# SimpleBase — System Root Class

## Purpose
`SimpleBase` is the foundational class for the entire Simple object system.
Every declarative class—whether a constant (`SimpleConstant`) or a composite
(`SimpleObject`)—inherits from this base. It provides:

- a unified identity,
- a stable connection to the `SimpleMeta` metaclass,
- a shared metadata interface,
- structural guarantees for all descendants.

This class is intentionally minimal. Its role is architectural, not functional.

---

## 1. Metaclass Integration
`SimpleBase` uses `SimpleMeta` as its metaclass. This ensures that all subclasses
automatically receive:

- metadata computation,
- write-once attribute protection,
- instance creation pipeline,
- technical and user-facing representations.

The metaclass is responsible for the entire lifecycle of declarative classes.
`SimpleBase` simply establishes the connection.

---

## 2. Structural Slots
The class defines:

```
__slots__ = ()
```

This provides:

- reduced memory footprint,
- faster attribute access,
- predictable instance layout.

All subclasses must define their own `__slots__` to preserve these benefits.

---

## 3. Metadata Placeholder
The attribute:

```
__metadata__ = UNSET
```

serves as a placeholder for system base classes. Declarative user classes receive
their actual metadata during class creation via `SimpleMeta.__new__`.

This ensures:

- metadata always exists on every Simple class,
- metadata is never overwritten,
- metadata access is uniform across the system.

---

## 4. Architectural Role
`SimpleBase` is not intended for direct use. It exists to:

- unify the inheritance hierarchy,
- provide a stable anchor for metaclass behavior,
- guarantee that all Simple classes share the same structural foundation.

It is the “root node” of the Simple ecosystem.

---

## Notes
- `SimpleBase` contains no public methods; all behavior is inherited from
  `SimpleConstant`, `SimpleObject`, and the metaclass.
- This class is intentionally minimal to avoid polluting the public API.
- All future Simple system extensions will inherit from this base.
```
"""