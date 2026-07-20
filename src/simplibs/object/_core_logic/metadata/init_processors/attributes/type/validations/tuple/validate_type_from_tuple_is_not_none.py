from typing import Any, TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_type_from_tuple_is_not_none(
    inner_type: Any,
    type_tuple: tuple[Any, ...],
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that a type definition within a tuple structure does not contain a literal 'None' value."""

    # 1. Exception condition
    if inner_type is None:

        # 2. Variable resolution
        (class_name,
         class_parent,
         error_name,
         context,
         acceptable_definitions
         ) = _exception_info_for_type(owner_class)

        # 3. Exception invocation
        raise SimpleMetadataError(
            error_name=error_name,
            label="Literal 'None' detected in type tuple",
            value=type_tuple,
            expected="A valid type or class reference representing the output object.",
            problem=f"The class attribute '_type' contains a literal 'None' value within its tuple definition.",
            context=context,
            how_to_fix=(
                "Modify the '_type' attribute so that it does not contain the literal value 'None'.",
                "The defined types must reflect the actual concrete instances the class represents.",
                "If you intended to allow absence of value, use 'NoneType' from the 'types' module instead of 'None'.",
                "However, note that in this architecture, representing 'None' as a core value type is generally disallowed.",
            ) + acceptable_definitions,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_type_from_tuple_is_not_none

## Purpose
Prevents a common developer misconception where `None` is used as a placeholder for 
`NoneType` inside an attribute type tuple (e.g., writing `_type = (int, None)`).

## Mechanism & Pipeline Placement
During the execution of `process_type`, if `_type` is provided as a standard Python 
`tuple`, the orchestrator iterates over its internal components. This guard intercepts 
the iteration to ensure no literal `None` elements sneak into the collection before 
it gets flattened and converted into a modern `UnionType`.

## Architectural Rules
In the SimpleObject domain, metadata parameters must represent actual types compatible 
with Python's native `isinstance()` checks. Because `isinstance(val, None)` throws a 
native `TypeError`, this validator provides a highly descriptive domain exception 
before Python's runtime fails cryptically.
"""