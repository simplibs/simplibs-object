from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ....protocols.metadata import SimpleMetadataLike
    from ....protocols.instance.core_classes import InstanceBaseProtocol


class InstanceBase:
    """Base class for all atomic and composite instances."""

    # 1. Metaclass bypass flag
    _is_instance_class: bool = True

    # 2. Memory-optimized layout with weakref support
    __slots__ = ("__weakref__",)

    # 3. Mixin initialization anchor
    def init_mixins(self: "InstanceBaseProtocol") -> None:
        pass

    # 4. Fast metadata access
    @property
    def meta(self: "InstanceBaseProtocol") -> "SimpleMetadataLike":
        return self.__class__.__metadata__

    # 5. Technical diagnostic representation
    def __repr__(self: "InstanceBaseProtocol") -> str:
        class_name = self.meta.class_name
        blueprint = f"blueprint='{self.meta.blueprint_path}'"
        state = f"value={self._value!r}" if hasattr(self, "_value") else "value=EMPTY"
        hex_id = f"id={hex(id(self))}"
        return f"<{class_name} {blueprint} {state} {hex_id}>"

    # 6. Clean user-facing representation
    def __str__(self: "InstanceBaseProtocol") -> str:
        return self.meta.class_name



_DESIGN_NOTES = """
# InstanceBase

## Purpose
Provides the foundational runtime identity for all instance types:
- atomic constants,
- atomic values inside compositions,
- composite instances.

## Behavior

### 1. Metaclass bypass
Defines `_is_instance_class = True` directly on the base class to prevent
`SimpleMeta.__new__` from treating runtime instance types and hierarchies
as new declarative blueprints.

### 2. Memory layout
`__slots__ = ("__weakref__",)` ensures:
- no `__dict__`,
- minimal memory footprint,
- weakref support for caching and tracking.

### 3. Mixin lifecycle
`init_mixins` acts as a stable hook for dynamically injected behaviors.

### 4. Metadata access
`meta` resolves metadata in constant time by reading `__metadata__` directly
from the class.

### 5. Introspection
`__repr__` provides a diagnostic snapshot:
- class name,
- blueprint path,
- current value (if present),
- memory address.

`__str__` returns the business name of the class.
"""