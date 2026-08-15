from typing import TYPE_CHECKING
# Outers
from ..base_class import SimpleMixin
# Inners
from ._utils._utils_for_inners_property import collect_all_nested_properties
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.instance import SimpleInstanceLike


class InnersProperty(SimpleMixin):
    """
    Mixin adding properties for inner elements.

    Dynamically extends composite instances with properties for direct,
    convenient access to their inner elements (inners), based on the
    blueprint definition.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _composite_only = True

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Hook for modifying the instance class
    # ----------------------------------------

    @staticmethod
    def __extend_instance_class__(
        instance_cls: "SimpleInstanceLike"
    ) -> "SimpleInstanceLike":
        """
        Internal method for attaching elements to the class, before the
        initialization process.
        """

        # 1. Build the required properties
        nested_props = collect_all_nested_properties(instance_cls.meta)

        # 2. Attach the attributes to the class
        for name, prop in nested_props.items():
            setattr(instance_cls, name, prop)

        # 3. Return the modified class
        return instance_cls


_DESIGN_NOTES = """
# InnersProperty

## Purpose
Generates direct-access properties for a composite's inner elements, so
`obj.first_name` works instead of requiring `obj["first_name"]` or
`obj.get("first_name")` via the `Mapping` dunder mixin. This is the
attribute-style counterpart to the dict-style access `Mapping` provides.

## Compatibility
- `_composite_only = True` — atoms have no inners to generate properties
  for.

## Logic
`__extend_instance_class__` runs once at class-creation time:
1. Calls `collect_all_nested_properties(instance_cls.meta)`, which does
   the actual work of walking the blueprint and building a `name →
   property` mapping (including, per the name "nested," properties that
   reach into deeper levels of the composite tree, not just direct
   children).
2. Attaches every returned property to `instance_cls` via `setattr`.

This mixin itself is a thin orchestrator — all the real logic of
deciding which properties to build and how they read/write values lives
in `_utils_for_inners_property.collect_all_nested_properties`.

## Notes
- Unlike `Equalizer`/`ImmutableWithInners`, which build their properties
  inline inside `__extend_instance_class__` with closures, this mixin
  delegates the whole collection step to a utility function — worth
  knowing which pattern is used where when reading the codebase, since
  they achieve similar ends differently.
- "Nested" in `collect_all_nested_properties` suggests this mixin may
  expose deep-path access (e.g. reaching two or more levels into a
  composite tree), not just immediate children — useful context to keep
  in mind since the sibling mixins here mostly only handle the direct
  inners.
"""
