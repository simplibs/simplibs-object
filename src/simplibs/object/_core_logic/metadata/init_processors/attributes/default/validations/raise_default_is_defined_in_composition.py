from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_default import _exception_info_for_default
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike


def raise_default_is_defined_in_composition(
    owner_class: "SimpleClassLike"
) -> None:
    """Raises an exception indicating that explicit '_default' attributes are forbidden on composite objects."""

    # 1. Variable resolution for the exception
    (class_name,
     class_parent,
     error_name,
     context,
     ) = _exception_info_for_default(owner_class)

    # 2. Exception invocation
    raise SimpleMetadataError(
        error_name=error_name,
        label="Forbidden attribute '_default' on composite structure",
        expected="A composite class definition completely free of an explicit '_default' attribute.",
        problem=f"The composite class '{class_name}' explicitly defines a '_default' attribute, which is strictly prohibited for structures managing '_inners'.",
        context=context,
        how_to_fix=(
            f"Remove the '_default' attribute directly from the definition of class '{class_name}'.",
            "To steer the default state of this composite object, modify the individual fallback defaults within its component definitions inside '_inners'.",
            "If this structure is intended to act as a terminal leaf (SimpleConstant) holding its own explicit value, remove the '_inners' attribute and the '_logic' method entirely.",
        ),
        exception=TypeError
    )


_DESIGN_NOTES = """
# raise_default_is_defined_in_composition

## Purpose
Enforces architectural boundaries by blocking developers from explicitly setting a 
`_default` attribute on composite structures (`SimpleObject`). 

## Architectural Rationalization
In the SimpleObject ecosystem, composite nodes must remain strictly deterministic. 
Their initial fallback state is derived entirely by aggregating the nested states 
of their inner elements (`_inners`) and feeding them through the `_logic` method. 
Allowing a manual `_default` bypasses this chain, introduces competing sources 
of truth, and compromises metadata integrity.

## Guard Mechanism Placement
This validator is triggered directly within the `_process_user_data` lifecycle of 
`SimpleObjectMetadata`. By intercepting the class definition right before inner 
parameters are parsed and mapped to the `_logic` signature, it guarantees that any 
hybrid or invalid state definition is rejected as early as possible.
"""