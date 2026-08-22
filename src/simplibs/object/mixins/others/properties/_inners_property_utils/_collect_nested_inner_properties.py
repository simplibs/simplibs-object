from typing import TYPE_CHECKING
# Inners
from ....._core.logic.property_builders import create_properties_for_inner
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.metadata import SimpleMetadataLike
    from ....._core.protocols.alias_typings import PathTuple


def _collect_nested_inner_properties(
    meta: "SimpleMetadataLike",
    path: "PathTuple",
    result: dict[str, property]
) -> None:
    """
    Recursively traverses all nested inners and adds their properties
    into the `result` dictionary.
    """

    # 1. Iterate through inner elements
    for inner in meta.inners:

        # 1.1 Extract metadata and extend path
        inner_meta = inner.meta
        new_path = path + (inner_meta.name_private,)

        # 1.2 Create properties (for constants and composites)
        props = create_properties_for_inner(inner_meta, new_path)
        result.update(props)

        # 1.3 Recursively process composite inners
        if not inner_meta.is_constant:
            _collect_nested_inner_properties(inner_meta, new_path, result)


_DESIGN_NOTES = """
# _collect_nested_inner_properties

## Purpose
Recursively collects properties for all nested inner elements and stores them
in the provided `result` dictionary. This function is the low‑level engine
behind nested property generation for composite structures.

It ensures that every inner element — regardless of depth — receives a
properly constructed property with a correct access path.

## Architectural role
`_collect_nested_inner_properties` is used by:

- `collect_all_nested_properties`
- property generation during class initialization
- composite structure expansion
- metadata‑driven property builders
- debugging and introspection tools

It forms the recursive backbone of nested property discovery.

## How it works
The function performs three deterministic steps:

### 1. Iterate through inner elements
For each inner element in `meta.inners`, the function extracts its metadata and
extends the current path tuple.  
The path represents the hierarchical location of the inner element inside the
composite structure.

### 2. Create properties
Calls `create_properties_for_inner(inner_meta, new_path)` which generates:

- getter/setter properties,
- composite accessors,
- constant accessors,
- metadata‑aware property wrappers.

These properties are inserted into the shared `result` dictionary.

### 3. Recursively process composite inners
If the inner element is a composite (`not inner_meta.is_constant`), the
function calls itself recursively, passing the extended path.

This ensures that nested composite structures are fully traversed and all
properties are generated.

## Integration requirements
The function assumes:

- **SimpleMetadataLike**  
  Provides `.inners`, `.name_private`, `.is_constant`.

- **property_builders.create_properties_for_inner**  
  Generates the actual property objects.

Without these components, nested property generation cannot operate correctly.

## Why this function exists
Nested composite structures require:

- deterministic property generation,
- stable hierarchical paths,
- metadata‑driven behavior,
- recursive traversal,
- consistent naming conventions.

This function encapsulates all of that in a minimal, stable utility.

## Deterministic behavior
The function guarantees:

- stable path construction,
- consistent property naming,
- predictable recursion,
- correct handling of constants and composites,
- deterministic ordering based on metadata.

This determinism is essential for introspection, debugging, and composite
behavior.

## Stability guarantee
Any change to this function would affect:

- property generation,
- composite access behavior,
- metadata consistency,
- debugging tools,
- class initialization.

Therefore, `_collect_nested_inner_properties` is treated as a **core invariant**
of the property subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to metadata and property builders.
"""