from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_inner_is_class(
    inner: "SimpleClassLike",
    inners: tuple["SimpleClassLike", ...],
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that a specific element within the '_inners' collection is an actual data type (class)."""

    # 1. Exception condition
    if not isinstance(inner, type):

        # 2. Variable resolution
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = _exception_info_for_inners(owner_class)

        # 3. Exception invocation
        raise SimpleMetadataError(
            error_name=error_name,
            label="Element inside _inners is not a valid class",
            value=inner,
            expected="Every inner element must be a class definition inheriting from SimpleObject or SimpleConstant.",
            problem=f"The inner element '{inner}' discovered within the collection '{inners}' is an instance or a raw data value, not a class type.",
            context=context,
            how_to_fix=(
                "Ensure that the '_inners' attribute contains only raw class references, not instantiated objects.",
                "Remove trailing parentheses from the element definition (e.g., use 'MyElement' instead of 'MyElement()').",
                "Verify that the provided item is not a string, primitive datatype, or the output of a function execution.",
            ) + acceptable_definitions,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_inner_is_class

## Purpose
Acts as the ultimate entry gatekeeper for composition integrity. Its primary role 
is to ensure that every entry registered within the `_inners` container represents 
a structural blueprint (`type`), rather than an active state instance.

## Crucial Execution Ordering
1. **Downstream Safety**: Sub-sequence routines such as `issubclass` lookups or 
   accessing the `.meta` descriptor namespace fail hard with unreadable runtime 
   exceptions if executed against an instantiated object. This guard isolates the input.
2. **Developer UX**: A common syntax pitfall is accidental instantiation during 
   declaration. This validation explicitly identifies this mismatch immediately.

## Explicit Verification Strategy
Using an explicit `isinstance(inner, type)` check before any other processing 
guarantees that formatting targets are completely valid. It keeps the framework 
predetermined and ensures errors are captured precisely at initialization time.
"""