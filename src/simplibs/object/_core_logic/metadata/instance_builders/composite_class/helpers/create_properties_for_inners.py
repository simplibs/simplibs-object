from typing import TYPE_CHECKING
# Outers
from .....properties import create_properties_for_inner
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike


def create_properties_for_inners(
    meta: "SimpleMetadataLike",
    *,
    mutable: bool = True
) -> dict:
    """Generates property descriptors for all immediate internal child nodes (inners).

    Compiles an interface dictionary mapping public names to specialized descriptor instances
    tailored to the mutability constraints of the composition layer.
    """

    return {
        k: v
        for inner in meta.inners
        for k, v in create_properties_for_inner(
            inner.meta,
            path=(),
            mutable=mutable
        ).items()
    }


_DESIGN_NOTES = """
# create_properties_for_inners

## Purpose
Acts as an interface compilation adapter during the synthesis of dynamic composite classes. It flattens and maps structural child node definition frameworks into standard Python descriptor bindings (`property`), exposing clean public access paths to nested child instances located within slot targets.

## Architectural Design Decisions

### 1. Direct Hierarchy Proxying via Dictionary Unpacking
* The function utilizes a double-loop dictionary comprehension pattern to collect property bindings directly from an upstream factory wrapper `create_properties_for_inner`.
* By supply-routing an empty tuple `path=()`, it signals to the underlying property generator that these descriptors are root-level accessors for immediate children, mapping directly to private structural layout slots (e.g., exposing `self._engine` through a public `self.engine` interface).

### 2. Encapsulated Class Compilation Delivery
* Returning a raw `dict` object allows the parent orchestrator (`make_composite_class`) to safely merge these attributes directly into the final class dictionary payload using pipe merge operators (`class_dict |= ...`).
* This approach prevents runtime property injection overhead via subsequent `setattr` loops at class level, compiling all interface access paths directly at type initialization.
"""