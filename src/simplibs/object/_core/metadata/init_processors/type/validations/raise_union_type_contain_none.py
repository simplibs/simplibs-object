from typing import NoReturn, TYPE_CHECKING
# Outers
from ......exceptions import SimpleDefinitionError
# Inners
from ._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike



def raise_union_type_contain_none(
    owner_class: "SimpleClassLike"
) -> NoReturn:
    """Raises an error when a UnionType contains NoneType."""

    (
        class_name,
        class_parent,
        error_name,
        context,
        acceptable_definitions,
    ) = _exception_info_for_type(owner_class)

    raise SimpleDefinitionError(
        error_name=error_name,
        label="_type",
        problem=(
            f"The UnionType definition for class '{class_name}' contains NoneType.",
        ),
        expected="A UnionType without NoneType or literal None.",
        how_to_fix=(
            "Remove NoneType or literal None from the union expression.",
            "Use only real, concrete types in the union.",
        ) + acceptable_definitions,
        context=context,
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_union_type_contain_none

## Purpose
Raises a structured error when a modern Python UnionType used in `_type`
contains `NoneType` (e.g. `_type = int | None`).  
Optional or absent states are not allowed inside the core type registry.

## Pipeline context
This function is called from the `UnionType` branch of `process_type` when:

- `NoneType in raw_type.__args__` evaluates to `True`.

It does not perform any checks itself; it only formats and raises the error.

## Architectural reasoning
The metadata type system must describe concrete, fully initialized value domains.
Embedding `NoneType` inside union definitions would:

- blur the boundary between “no value” and “valid value”,
- complicate validation and normalization,
- break deterministic assumptions in internal mapping routines.

Optionality is handled at a different level, not inside `_type`.

## Notes
If absence of value is part of the business logic, it should be modeled explicitly
in higher-level structures, not by mixing `NoneType` into the core type constraint.

"""