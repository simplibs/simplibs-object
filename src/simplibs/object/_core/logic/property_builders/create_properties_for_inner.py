from typing import TYPE_CHECKING
# Inners
from .create_value_property import create_value_property
from .create_instance_property import create_instance_property
# Annotations
if TYPE_CHECKING:
    from ...protocols.metadata import SimpleMetadataLike
    from ...protocols.alias_typings import PathTuple


def create_properties_for_inner(
    inner_meta: "SimpleMetadataLike",
    path: "PathTuple | ()" = (),
    *,
    mutable: bool = True,
) -> dict[str, property]:
    """Generates value and instance properties for a single inner element."""

    # 1. Prepare output dictionary
    property_dict = {}

    # 2. Resolve names and path
    name_snake = inner_meta.name_snake
    instance_path = path + (inner_meta.name_private,)

    # 3. Create value property
    value_property = create_value_property(
        inner_meta,
        is_constant=inner_meta.is_constant,
        mutable=mutable,
        path=instance_path,
    )

    # 4. Create instance property
    instance_property = create_instance_property(
        inner_meta,
        instance_path,
    )

    # 5. Insert properties into dictionary
    property_dict[name_snake] = value_property
    property_dict[f"{name_snake}_instance"] = instance_property

    # 6. Return property mapping
    return property_dict


_DESIGN_NOTES = """
# create_properties_for_inner

## Purpose
Generates the two public properties associated with every inner element of a
composite instance:

1. `<inner_name>` — exposes the value of the inner element (read/write depending
   on mutability).
2. `<inner_name>_instance` — exposes the inner instance object (read-only).

These properties form the public API for navigating and manipulating composite
structures.

---

## Behavior
1. **Path Resolution**
   - The function receives a `path` representing the attribute chain leading to
     the inner element.
   - It extends the path with the inner's private slot name, producing the full
     lookup path for both properties.

2. **Value Property**
   - Created via `create_value_property`.
   - Provides access to the normalized value of the inner element.
   - Supports mutation only when the instance is mutable.
   - Composite setters automatically decompose values into deeper inner nodes.

3. **Instance Property**
   - Created via `create_instance_property`.
   - Provides read-only access to the inner instance object.
   - Essential for introspection and advanced manipulation.

4. **Dictionary Output**
   - Returns a dictionary mapping:
     - `<name_snake>` → value property
     - `<name_snake>_instance` → instance property
   - This dictionary is consumed by composite class builders and mixins.

---

## Notes
- This function is used both for direct inners and for nested inners when mixins
  expand the composite tree.
- The separation of value and instance properties ensures a clean and predictable
  API: values are mutable (when allowed), instances are not.
- The function is intentionally minimal; all logic is delegated to the underlying
  property builders.
"""
