from typing import TYPE_CHECKING, Any
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_inners_is_tuple(
    inners: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that the '_inners' attribute is explicitly declared as a 'tuple'."""

    # 1. Exception condition
    if not isinstance(inners, tuple):

        # 2. Variable resolution
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = _exception_info_for_inners(owner_class)

        # 3. Exception invocation
        raise SimpleMetadataError(
            error_name=error_name,
            label="The '_inners' attribute does not reference a tuple",
            expected="A tuple containing subclasses of SimpleConstant and SimpleObject.",
            value=inners,
            problem=f"The '_inners' attribute must be explicitly defined using the tuple data type.",
            context=context,
            how_to_fix=(
                "Change the definition of '_inners' to a tuple container.",
                "Example layout: _inners = (ElementA, ElementB).",
                "If declaring only a single element, remember to include a trailing comma: _inners = (ElementA,).",
            ) + acceptable_definitions,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_inners_is_tuple

## Purpose
Acts as a core structural validation check in the composition processing pipeline. 
It strictly enforces the usage of the standard `tuple` type for defining components registered 
within the `_inners` attribute namespace.

## Rationale Behind Tuple Enforcement
1. **Immutability**: Class structural metadata definitions must remain constant. A tuple 
   guarantees that the underlying collection cannot be dynamically altered or corrupted at runtime.
2. **Deterministic Ordering**: Unlike unordered collection models (e.g., sets), a tuple preserves 
   the exact declaration order. This is highly critical because the positional ordering maps directly 
   to the automatic argument layout inside the dynamically compiled `_logic` signature.
3. **Idiomatic Design**: Using tuples aligns seamlessly with Pythonic metadata conventions 
   (e.g., standard type unions or the native `isinstance` target structure).

## Edge Case Prevention
Developers frequently forget that a single-element tuple declaration in Python requires a trailing 
comma, such as `(MyElement,)`. Without this trailing comma, Python parses the parentheses as standard 
operational grouping and yields the raw internal class instead, causing subsequent mapping loops 
to fail. This validation instantly flags this structural defect with crystal-clear directions.
"""