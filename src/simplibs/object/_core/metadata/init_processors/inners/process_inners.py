from typing import TYPE_CHECKING, Any
# Inners
from .validations import (
    validate_inners_is_not_empty,
    validate_inners_is_tuple,
    validate_inner_is_simple_subclass,
    validate_inner_is_not_simple_class,
    validate_inner_is_class,
    validate_collision_within_inners,
    validate_if_collision_with_owner_class,
)
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleClassLike


def process_inners(
    node_names_set: set,
    name_snake: str,
    owner_class: "SimpleClassLike",
) -> tuple[tuple["SimpleClassLike", ...], set]:
    """Validates and processes _inners for a composite class."""

    # 1. Acquire attribute (Guaranteed to exist by SimpleMeta routing)
    raw_inners = getattr(owner_class, "_inners")

    # 2. Check if validations are needed (only for locally declared _inners)
    need_validations = "_inners" in owner_class.__dict__

    # 3. Base validations
    if need_validations:
        validate_inners_is_tuple(raw_inners, owner_class)
        validate_inners_is_not_empty(raw_inners, owner_class)

        from .....SimpleConstant import SimpleConstant
        from .....SimpleObject import SimpleObject

    # 4. Prepare namespace accumulator
    new_node_names_set = node_names_set.copy()

    # 5. Iterate inners
    raw_inners: tuple["SimpleClassLike", ...]
    for inner in raw_inners:
        inner: type["SimpleClassLike"]

        # 5.1 Type and hierarchy checks
        if need_validations:
            # noinspection PyUnboundLocalVariable
            if (
                not isinstance(inner, type)
                or not issubclass(inner, SimpleConstant)
                or inner is SimpleConstant
                or inner is SimpleObject
            ):
                validate_inner_is_class(inner, raw_inners, owner_class)
                validate_inner_is_simple_subclass(inner, owner_class)
                validate_inner_is_not_simple_class(inner, owner_class)

        # 5.2 Name collision checks
        node_name_collisions = new_node_names_set & inner.meta.node_names_set
        if node_name_collisions:
            collision_name = next(iter(node_name_collisions))
            validate_if_collision_with_owner_class(
                collision_name,
                name_snake,
                inner,
                owner_class,
            )
            if need_validations:
                validate_collision_within_inners(
                    collision_name,
                    name_snake,
                    raw_inners,
                    inner,
                    owner_class,
                )

        # 5.3 Register names
        new_node_names_set.update(inner.meta.node_names_set)

    # 6. Return results
    return raw_inners, new_node_names_set



_DESIGN_NOTES = """
# process_inners

## Purpose
Validates and processes `_inners` for composite classes.
Ensures strict determinism, predictable structure, and globally unique naming across the entire tree.

## Architectural Context & Routing
`SimpleMeta.__new__` routes class creation strictly based on the presence of `_inners`:
- If `_inners` is present -> routed to `SimpleObjectMetadata` -> invokes `process_inners`.
- If `_inners` is absent -> routed to `SimpleConstantMetadata` -> treats class as atomic.

Because of this top-level meta routing, `process_inners` operates under the strict invariant 
that `_inners` **always exists** on `owner_class` (it is never `UNSET`). Consequently, checking 
for missing `_inners` or fallback sentinel handling is intentionally omitted as redundant.

## Why inners matter
Each inner must be a concrete class inheriting from `SimpleConstant` (which includes `SimpleObject`).
This guarantees:
- consistent metadata (`__metadata__`)
- defined type boundary (`_type`)
- default fallback (`_default`)
- unique nested identifier index (`node_names_set`)

## Control flow

### 1. Attribute extraction & validation
Extracts `_inners` and validates that local declarations:
- are structured as a `tuple`
- are not empty (an empty tuple `_inners = ()` is invalid; classes without inners omit `_inners`)

### 2. Namespace accumulator
`new_node_names_set` is a shallow copy of the parent namespace.
This prevents sibling pollution and ensures deterministic propagation of names.

### 3. Local base-class imports
`SimpleConstant` and `SimpleObject` are imported lazily to avoid circular dependencies.

### 4. Iteration over inners

#### 4.1 Structural type guards
Each inner must:
- be a class (`type`)
- inherit from `SimpleConstant`
- not be the raw base classes `SimpleConstant` or `SimpleObject`

#### 4.2 Name collision detection
Checks intersection between `new_node_names_set` and `inner.meta.node_names_set`.
Distinguishes between owner-class collisions and sibling collisions.

#### 4.3 Namespace registration
Updates `new_node_names_set` so all nested names are immediately visible to subsequent inners.

### 5. Return value
Returns:
- `raw_inners` — verified tuple of inner classes
- `new_node_names_set` — fully updated namespace for this subtree
"""