from typing import TYPE_CHECKING, Any
from simplibs.sentinels import UNSET
# Inners
from .validations import (
    validate_inners_is_not_empty,
    validate_inners_is_defined,
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

    # 1. Acquire attribute
    raw_inners = getattr(owner_class, "_inners", UNSET)

    # 2. Check if validations are needed
    need_validations = "_inners" in owner_class.__dict__ and raw_inners is not UNSET

    # 3. Base validations
    if need_validations:
        if not raw_inners or not isinstance(raw_inners, tuple):
            validate_inners_is_defined(raw_inners, owner_class)
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
Determines whether a class behaves as a constant (no `_inners`) or a composition (with `_inners`).  
Ensures strict determinism, predictable structure, and globally unique naming across the entire tree.

## Why inners matter
Each inner must be a class inheriting from `SimpleConstant` (which includes `SimpleObject`).  
This guarantees:
- consistent metadata (`__metadata__`)
- defined type boundary (`_type`)
- default fallback (`_default`)
- unique nested identifier index (`node_names_set`)

If `_inners` is defined → class is a `SimpleObject`.  
If `_inners` is absent → class is a `SimpleConstant`.

## Control flow

### 1. Attribute extraction & validation
Checks:
- `_inners` is explicitly defined
- `_inners` is a tuple
- `_inners` is not empty

Empty tuple is invalid: a class with no inners must omit `_inners` entirely.

### 2. Namespace accumulator
`new_node_names_set` is a shallow copy of the parent namespace.  
This prevents sibling pollution and ensures deterministic propagation of names.

### 3. Local base-class imports
`SimpleConstant` and `SimpleObject` are imported lazily to avoid circular dependencies.  
Imports are skipped if early validations fail.

### 4. Iteration over inners

#### 4.1 Structural type guards
Each inner must:
- be a class (`type`)
- inherit from `SimpleConstant`
- not be the raw base classes `SimpleConstant` or `SimpleObject`

Only concrete subclasses are allowed.

#### 4.2 Name collision detection
Checks intersection between `new_node_names_set` and `inner.meta.node_names_set`.

Two types of collisions:
- **owner-class collision** → `validate_if_collision_with_owner_class`
- **sibling collision** → `validate_collision_within_inners`

Both use `_get_collision_path` to produce precise breadcrumb diagnostics.

#### 4.3 Namespace registration
`new_node_names_set.update(inner.meta.node_names_set)`  
This ensures all nested names are immediately visible to subsequent inners.

### 5. Return value
Returns:
- `raw_inners` — original tuple of inner classes
- `new_node_names_set` — fully updated namespace for this subtree

## Performance notes
The function is optimized for the “happy path”:
- early boundary checks prevent unnecessary work
- recursion only occurs on guaranteed branches (via `node_names_set`)
- no redundant buffers or allocations

## Architectural notes
- Namespace isolation via `.copy()` ensures deterministic behavior.
- Lazy imports prevent circular dependencies.
- Any structural violation stops compilation immediately with a precise error.
"""