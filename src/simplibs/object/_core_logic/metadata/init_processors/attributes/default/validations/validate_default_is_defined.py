from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from .......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_default import _exception_info_for_default
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike


def validate_default_is_defined(
    default_value: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that the '_default' attribute has been explicitly defined for a constant leaf node."""
    if default_value is UNSET:
        (
            class_name,
            class_parent,
            error_name,
            context,
        ) = _exception_info_for_default(owner_class)

        raise SimpleMetadataError(
            error_name=error_name,
            label="Attribute '_default' is not defined",
            expected="The '_default' attribute must contain a concrete default value for the constant.",
            problem="The required '_default' attribute is missing from the class definition.",
            context=context,
            how_to_fix=(
                "A constant leaf structure (SimpleConstant) must explicitly declare a '_default' value.",
                "Add the '_default = <value>' attribute directly to the body of your class definition.",
                "If this object was intended to be a structured compound entity instead, add an '_inners' mapping and a '_logic' method.",
                "Verify that the default value expression was not accidentally stripped or removed during runtime modification.",
            ),
            exception=ValueError
        )


_DESIGN_NOTES = """
# validate_default_is_defined

## Purpose
Ensures that no node within the operational architecture is left in an uninitialized or ambiguous state. If an entity does not declare inner structural composition (meaning it is not a compound object), the system processes it as a pure constant leaf and strictly demands a baseline value.

## Why UNSET and not None?
We leverage our native `UNSET` sentinel because `None` represents a fully valid payload value in many runtime domains. By tracking the absolute absence of the attribute via `UNSET`, we can unequivocally detect when a developer genuinely forgot to provide a value.

## Role in the Structural Decision Tree
This validation acts as a core behavioral safety net. If an engineer omits compound mechanics and simultaneously forgets to bind a default constant value, this error message intercept points them precisely toward both corrective architectural paths.
"""