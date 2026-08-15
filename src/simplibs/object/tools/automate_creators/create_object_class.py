from typing import Callable, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ...SimpleObject import SimpleObject
# Inners
from ._helpers.process_validate import process_validate
from ._helpers.load_parameters_from_inners import load_parameters_from_inners
from ._helpers.process_logic import process_logic
from ._helpers.calculate_default import calculate_default
from ._helpers.process_decompose import process_decompose
from ._validations import (
    validate_class_name_is_str,
    validate_composite_has_logic,
    validate_composite_has_inners
)
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols import SimpleClassType, SimpleClassLike


# noinspection PyTypeChecker
def create_object_class(
    class_name: str,
    inners: tuple["SimpleClassType", ...],
    logic: Callable,
    value_type: type | UnsetType = UNSET,
    validate: Callable | UnsetType = UNSET,
    decompose: Callable | UnsetType = UNSET,
) -> "SimpleClassLike":
    """Dynamically creates a SimpleObject composite subclass.

    Args:
        class_name: Target name of the generated composite class.
        inners: Tuple of inner child component blueprint classes.
        logic: Functional calculation rule deriving value from inner components.
        value_type: Explicit value type override; if UNSET, inferred from logic default result.
        validate: Optional user validation function or lambda rule.
        decompose: Optional top-down value decomposition function or lambda handler.

    Returns:
        Newly created SimpleObject subclass blueprint.

    Raises:
        SimpleDefinitionError: If class_name is invalid or required logic parameter is UNSET.
    """

    # 1. Parameter boundary validations
    if not (
        isinstance(class_name, str)
        and class_name.strip()
        and inners not in (None, UNSET)
        and logic not in (None, UNSET)
    ):
        validate_class_name_is_str(class_name)
        validate_composite_has_inners(class_name, inners)
        validate_composite_has_logic(class_name, logic)

    # 2. Extract inner parameter names and defaults
    _params = load_parameters_from_inners(class_name, inners)

    # 3. Normalize logic signature
    _logic = process_logic(logic, _params.keys())

    # 4. Infer output value_type if omitted
    if value_type is UNSET:
        _default_value = calculate_default(logic, tuple(_params.values()))
        value_type = type(_default_value)

    # 5. Prepare class namespace blueprint
    namespace = {
        "_inners": inners,
        "_type": value_type,
        "_logic": _logic,
    }

    # 6. Attach normalized validation handler if provided
    if validate is not UNSET:
        _validate = process_validate(validate)
        namespace["_validate"] = classmethod(_validate)

    # 7. Attach normalized decomposition handler if provided
    if decompose is not UNSET:
        _decompose = process_decompose(decompose)
        namespace["_decompose"] = classmethod(_decompose)

    # 8. Dynamically instantiate subclass and return
    new_class = type(class_name, (SimpleObject,), namespace)

    return new_class


_DESIGN_NOTES = """
# create_object_class (Creator Engine)

## Purpose
Dynamically constructs a `SimpleObject` composite subclass at runtime without requiring explicit 
class blueprint statements. Programmatically builds reactive object tree nodes.

## Execution Workflow
1. Validates `class_name` and ensures `logic` is not `UNSET` via guard functions.
2. Extracts inner component parameter names and default values via `load_parameters_from_inners`.
3. Normalizes `logic` callable signature to accept `(cls, *args)` via `process_logic`.
4. Executes `calculate_default` to derive the composite default value and infers `value_type` if `UNSET`.
5. Prepares class `namespace` dictionary with `_inners`, `_type`, and `_logic`.
6. Wraps and attaches optional `_validate` and `_decompose` methods using `process_validate` and `process_decompose`.
7. Calls `type(class_name, (SimpleObject,), namespace)` to generate and return the class blueprint.

## Framework Usage
- Called directly by developers or internally via `create_simple_object`.
"""