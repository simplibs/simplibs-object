from typing import Any, TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_type_tuple_is_not_nested(
    inner_type: Any,
    type_tuple: tuple[Any, ...],
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that a type definition tuple does not contain any nested tuple structures."""

    # 1. Exception condition
    if isinstance(inner_type, tuple):

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
            label=f"{class_name}._type",
            value=type_tuple,
            expected="A flat structure of types or class references.",
            problem="The class attribute '_type' is defined as a tuple that contains a nested tuple.",
            context=context,
            how_to_fix=(
                "The class type must accurately reflect the values the class represents.",
                "Multi-type definitions using a tuple must be completely flat and cannot contain internal tuples.",
                "Flatten the nested tuple structure into a single sequence.",
                "Example: Instead of '(int, (str, float))', rewrite the expression as '(int, str, float)'.",
            ) + acceptable_definitions,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_type_tuple_is_not_nested

## Purpose
Enforces a flat, non-nested structure when multiple types are supplied via a standard 
Python `tuple`. This prevents complex recursive tree evaluations during metadata 
compilation.

## Pipeline Integration
As `process_type` iterates over the user-provided `tuple` to merge it into a modern 
`UnionType`, this guard intercepts any sub-tuples. By forcing a flat schema at the 
initialization layer, the framework guarantees that downstream type checkers and 
`isinstance()` calls operate at maximum efficiency with O(1) flat lookups.

## Developer Experience
Deeply nested tuples often stem from accidental double-wrapping or copy-paste errors 
during refactoring. The error output provides an explicit syntax blueprint showing 
how to flatten the collection.
"""