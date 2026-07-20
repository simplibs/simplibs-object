from typing import NoReturn, TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def raise_union_type_contain_none(
    owner_class: "SimpleClassLike"
) -> NoReturn:
    """Raises an exception indicating that the defined UnionType expression contains an invalid 'NoneType' reference."""

    # 1. Variable resolution
    (class_name,
     class_parent,
     error_name,
     context,
     acceptable_definitions
     ) = _exception_info_for_type(owner_class)

    # 2. Exception invocation
    raise SimpleMetadataError(
        error_name=error_name,
        label="NoneType detected within Union expression",
        expected="A clean UnionType expression completely free of NoneType or explicit None definitions.",
        problem=f"The modern union expression within the '_type' attribute of class '{class_name}' contains a 'NoneType' reference.",
        context=context,
        how_to_fix=(
            "Modify the '_type' union expression to completely remove 'NoneType' or 'None' elements.",
            "The defined type boundaries must accurately reflect real, fully initialized instance values.",
            "In this domain model architecture, representing a core metadata type constraint as optional or absent is fundamentally disallowed.",
        ) + acceptable_definitions,
        exception=TypeError
    )


_DESIGN_NOTES = """
# raise_union_type_contain_none

## Purpose
Enforces absolute type validation strictness by preventing optional type structures 
or absence markers (`NoneType`) from being embedded inside modern Python union type 
expressions (e.g., preventing configurations like `_type = int | None`).

## Pipeline Context & Invocation Strategy
This function functions as an explicit error factory within the `UnionType` parsing 
block of the `process_type` orchestrator. It is explicitly invoked when the orchestrator 
discovers that `NoneType in raw_type.__args__` evaluates to `True`. Because the condition 
is fully processed at the higher structural layer, this module contains no conditional 
logic of its own.

## Architectural Enforcement
The framework operates under a deterministic validation rule: metadata types must map 
to explicit runtime domains that can undergo clear value processing loops. Allowing 
undefined/optional states inside the type registry would violate core safety assumptions 
relied upon by internal mapping routines.
"""