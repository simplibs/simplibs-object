from typing import TYPE_CHECKING
# Outers
from .....logic.property_builders import create_properties_for_inner
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike


def create_properties_for_inners(
    meta: "SimpleMetadataLike",
    *,
    mutable: bool = True,
) -> dict:
    """Creates property descriptors for all immediate inner nodes."""

    return {
        k: v
        for inner in meta.inners
        for k, v in create_properties_for_inner(
            inner.meta,
            path=(),
            mutable=mutable,
        ).items()
    }


_DESIGN_NOTES = """
# create_properties_for_inners

## Purpose
Generates public property descriptors for all immediate inner nodes of a composite
instance class. These properties expose inner instances through clean, stable,
snake‑case accessors.

## Behavior
1. Iterates over `meta.inners`.
2. For each inner, calls `create_properties_for_inner` with:
   - `inner.meta` — metadata of the child
   - `path=()` — root-level access
   - `mutable` — mutability configuration
3. Flattens all generated descriptors into a single dictionary.

## Notes
- Returning a dictionary allows `make_composite_class` to merge descriptors directly
  into the class namespace using `class_dict |= ...`.
- This avoids runtime `setattr` loops and ensures properties are compiled into the
  class at creation time.
- `path=()` signals that these properties map directly to private slot attributes
  (e.g., `_engine` → `engine`).
"""