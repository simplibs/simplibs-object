from typing import Any, Callable
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ..SimpleConstant import SimpleConstant
# Inners
from ._process_helpers.process_validate import process_validate
from ._process_helpers.is_lambda import is_lambda


def create_constant_class(
    class_name: str,
    default: Any,
    value_type: type | UnsetType = UNSET,
    validate: Callable | UnsetType = UNSET,
):
    """
    Dynamically creates a SimpleConstant subclass.

    Parameters:
        class_name  – name of the generated class
        default     – default value of the constant
        value_type  – optional explicit type; if UNSET, inferred from default
        validate    – optional validation function or lambda

    Returns:
        Newly created SimpleConstant subclass.
    """

    # 1) Infer type if not provided
    if value_type is UNSET:
        value_type = type(default)

    # 2) Prepare namespace
    namespace = {
        "_default": default,
        "_type": value_type,
    }

    # 3) Wrap validate if provided
    if validate is not UNSET:
        _validate = process_validate(validate)
        namespace["_validate"] = classmethod(_validate)

    # 4) Create class dynamically
    new_class = type(class_name, (SimpleConstant,), namespace)

    return new_class
