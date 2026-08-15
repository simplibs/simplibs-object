from typing import Any, Callable, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ...SimpleConstant import SimpleConstant
# Inners
from ._helpers.process_validate import process_validate
from ._validations import (
    validate_class_name_is_str,
    validate_constant_has_default,
)
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols import SimpleClassLike


def create_constant_class(
    class_name: str,
    default: Any,
    value_type: type | UnsetType = UNSET,
    validate: Callable | UnsetType = UNSET,
) -> "SimpleClassLike":
    """Dynamically creates a SimpleConstant leaf subclass.

    Args:
        class_name: Target name of the generated class.
        default: Mandatory initial default value for the constant.
        value_type: Explicit value type override; if UNSET, inferred from default type.
        validate: Optional validation function or lambda rule.

    Returns:
        Newly created SimpleConstant subclass blueprint.

    Raises:
        SimpleDefinitionError: If class_name is invalid or default is UNSET.
    """

    # 1. Parameter boundary validations
    if not (
        isinstance(class_name, str)
        and class_name.strip()
        and default not in (None, UNSET)
    ):
        validate_class_name_is_str(class_name)
        validate_constant_has_default(class_name, default)

    # 2. Infer value type if omitted
    if value_type is UNSET:
        value_type = type(default)

    # 3. Prepare class namespace blueprint
    namespace = {
        "_default": default,
        "_type": value_type,
    }

    # 4. Attach normalized validation handler if provided
    if validate is not UNSET:
        # noinspection PyTypeChecker
        _validate = process_validate(validate)
        namespace["_validate"] = classmethod(_validate)

    # 5. Dynamically instantiate subclass and return
    new_class = type(class_name, (SimpleConstant,), namespace)
    new_class: "SimpleClassLike"
    return new_class


_DESIGN_NOTES = """
# create_constant_class (Creator Engine)

## Purpose
Dynamically constructs a `SimpleConstant` subclass at runtime without requiring explicit class 
statement declarations. Used for generating atomic leaf node blueprints programmatically.

## Execution Workflow
1. Validates `class_name` and ensures `default` is non-UNSET using guard functions.
2. Infers `_type` from `type(default)` if `value_type` is `UNSET`.
3. Constructs standard namespace dictionary containing `_default` and `_type`.
4. Wraps and attaches `_validate` as a `classmethod` if a validation callable was provided.
5. Invokes `type(class_name, (SimpleConstant,), namespace)` to create the class definition.

## Framework Usage
- Called directly by developers or internally via `create_simple_object`.
"""