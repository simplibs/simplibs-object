from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_inner_is_not_simple_class(
    inner: "SimpleClassLike",
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that the inner element is not the raw base class SimpleObject or SimpleConstant itself."""

    # Internal imports to avoid circular dependency states
    from ........SimpleConstant import SimpleConstant
    from ........SimpleObject import SimpleObject

    # 1. Exception condition
    if inner is SimpleConstant or inner is SimpleObject:

        # 2. Variable resolution
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = _exception_info_for_inners(owner_class)

        # 3. Exception invocation
        raise SimpleMetadataError(
            error_name=error_name,
            label="Base framework class detected inside _inners",
            expected="A concrete user-defined subclass of SimpleObject or SimpleConstant.",
            value=inner,
            problem=f"The '_inners' definition of class '{class_name}' directly contains the base class '{inner.__name__}'.",
            context=context,
            how_to_fix=(
                "Elements within the '_inners' collection must be concrete subclasses, not the base classes themselves.",
                "The core base classes (SimpleObject, SimpleConstant) serve strictly as blueprints for inheritance.",
                "Replace this structural reference with a specific subclass that represents actual system data.",
            ) + acceptable_definitions,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_inner_is_not_simple_class

## Purpose
Acts as a logical filter working alongside the subclass verification layer. While 
checking the inheritance hierarchy ensures structural compatibility, this validation 
guarantees that the abstract architectural roots are never utilized directly as functional 
data elements.

## Architectural Separation
1. **Semantic Distinction**: Being part of a subclass tree is a technical requirement 
   for runtime operation. Avoiding the exact base instance references is a functional 
   rule for meaningful domain modeling.
2. **Signature Cleanliness**: If raw base classes slipped into the compilation pipeline, 
   subsequent dynamic processors would generate non-descriptive parameter mappings 
   (e.g., matching a generic `simple_object` name inside the dynamic `_logic` method), 
   corrupting the static signature analysis.

## Execution Mechanics
Employs the Python `is` identity operator to evaluate memory addresses directly. This 
represents the most performant and deterministic mechanism to verify exact type references 
without risking inheritance resolution side-effects.
"""