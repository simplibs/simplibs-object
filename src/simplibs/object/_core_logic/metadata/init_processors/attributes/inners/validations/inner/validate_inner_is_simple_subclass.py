from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_inner_is_simple_subclass(
    inner: "SimpleClassLike",
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that the inner element correctly inherits from the required base framework classes."""

    # Internal import to prevent circular dependency bugs
    from ........SimpleConstant import SimpleConstant

    # 1. Exception condition
    inner: type
    if not issubclass(inner, SimpleConstant):

        # 2. Variable resolution
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = _exception_info_for_inners(owner_class)

        # 3. Exception invocation
        raise SimpleMetadataError(
            error_name=error_name,
            label="Invalid class hierarchy detected inside _inners",
            expected="The inner element must inherit from SimpleObject or SimpleConstant.",
            value=inner,
            problem="The provided element is not a recognized subclass of either SimpleObject or SimpleConstant.",
            context=context,
            how_to_fix=(
                "Elements declared inside the '_inners' attribute must belong to the SimpleObject/SimpleConstant family.",
                "Verify the inheritance tree of the failing class to ensure it derives from a supported base class.",
                "Check your import statements to confirm that you are referencing the correct class definition.",
            ) + acceptable_definitions,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_inner_is_simple_subclass

## Purpose
Acts as a core pillar of system runtime integrity. It verifies that every nested 
element implements the standard contract of the framework. This guarantees that downstream 
pipeline processors can confidently access properties like `.meta` or node names, 
which only exist on classes created via this specific metaclass architecture.

## Pipeline Relationships & Boundaries
This validation is highly specialized and follows strict isolation rules:
1. It operates under the safe assumption that the input has already passed the 
   `validate_inner_is_class` barrier.
2. It focuses exclusively on the **inheritance relationship**.
3. **Behavioral Note**: The built-in `issubclass` function evaluates to `True` when a class 
   is compared against itself. Therefore, this check allows raw base classes like `SimpleConstant` 
   or `SimpleObject` to pass through. Excluding those raw roots is explicitly delegated 
   to the adjacent `validate_inner_is_not_simple_class` step, keeping both components 
   completely atomic.

## Import Strategy
To protect the runtime environment from circular dependency hazards, the core base class 
reference is loaded lazily inside the local execution block right before the condition check.
"""