from typing import TYPE_CHECKING, Any
from simplibs.sentinels import UNSET
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_inners_is_defined(
    attribute_value: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that the '_inners' attribute is explicitly defined on the class."""

    # 1. Exception condition
    if attribute_value is UNSET:

        # 2. Variable resolution
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = _exception_info_for_inners(owner_class)

        # 3. Exception invocation
        raise SimpleMetadataError(
            error_name=error_name,
            label="The '_inners' attribute is not defined",
            expected="An explicit '_inners' attribute containing the composition elements tuple.",
            problem=f"The required '_inners' attribute is completely missing from the class structure of '{class_name}'.",
            context=context,
            how_to_fix=(
                "A composition class (SimpleObject) must explicitly declare the '_inners' attribute.",
                f"Define the '_inners' tuple within the body of class '{class_name}'.",
            ) + acceptable_definitions,
            exception=AttributeError
        )


_DESIGN_NOTES = """
# validate_inners_is_defined

## Purpose
Acts as a safety backup guard ensuring that the target class definition actually 
contains the `_inners` attribute slot. It prevents downstream processing errors 
caused by missing attributes when handling composite object types.

## Runtime Context & Edge Cases
Under standard architectural flows, this exception state should theoretically never 
be reached. The higher-level orchestration layers typically route the class initialization 
based on whether `_inners` is declared in the class namespace. However, this guard 
is preserved to guarantee absolute structural deterministic isolation and protect the 
pipeline from manual manipulation or dynamic `delattr` interventions.

## Exception Mapping
Unlike other structural validators that map to `TypeError`, this specific validation 
leverages a standard `AttributeError` wrapper, precisely matching native Python expectations 
when a required attribute token is missing from a class context.
"""