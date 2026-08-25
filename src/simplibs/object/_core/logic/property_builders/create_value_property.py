from typing import Optional, TYPE_CHECKING
# Inners
from .value_helpers import create_value_getter
from .value_helpers import create_value_setter
# Annotations
if TYPE_CHECKING:
    from ...protocols.metadata import SimpleMetadataLike


def create_value_property(
    meta: "SimpleMetadataLike",
    *,
    is_constant: bool = True,
    mutable: bool = True,
    path: Optional[tuple[str, ...]] = None,
) -> property:
    """Creates a unified value property for atomic and composite instances."""

    # 1. Create getter
    getter = create_value_getter(meta, path)

    # 2. Build docstring (getter part)
    doc_string = (
        f"Value of type `{meta.value_type_name}`.\n\n"
        f"Getter returns the value "
        f"{'of this element' if path is None else 'of the inner element'}.\n"
    )

    # 3. Immutable → getter only
    if not mutable:
        return property(
            fget=getter,
            doc=doc_string,
        )

    # 4. Create setter
    setter = create_value_setter(meta, is_constant, path)

    # 5. Extend docstring (setter part)
    if is_constant:
        doc_string += (
            "The setter normalizes the value, stores it, and "
            "triggers an update cascade upwards."
        )
    else:
        doc_string += (
            "The setter decomposes the input value and distributes it "
            "among the internal elements of the composition."
        )

    # 6. Return full property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string,
    )


_DESIGN_NOTES = """
# create_value_property

## Purpose
Creates the public-facing `value` property for both atomic and composite
instances. This property is the primary interface through which users read or
modify the value of an instance or any of its inner elements.

## Behavior
1. **Getter**
   - Always returns the normalized value.
   - If `path is None`, it reads `self._value` (root value).
   - If `path` is provided, it resolves the inner instance and returns its `.value`.

2. **Setter**
   - Generated only when `mutable=True`.
   - Atomic mode (`is_constant=True`):
     - Writes the value via `_root_value_setter`.
     - Triggers upward recalculation.
   - Composite mode (`is_constant=False`):
     - Requires `meta.is_decomposeable=True`.
     - Writes the root value.
     - Decomposes the value into inner nodes via `_recalculate_inners`.

3. **Inner Properties**
   - Composite instances generate additional `value` properties for each inner
     element using the same mechanism.
   - This ensures that every node in the composite tree exposes a consistent
     `value` interface.

## Notes
- The property is intentionally thin: all mutation logic is delegated to
  `create_value_setter`, and all read logic to `create_value_getter`.
- Atomic and composite instances share the same property interface, making the
  system uniform and predictable.
- Composite setters are guarded by `meta.is_decomposeable` to prevent invalid
  direct assignments.
- Inner properties behave identically to root properties, enabling recursive
  value manipulation throughout the composite tree.
"""