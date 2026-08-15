from typing import Any, Callable, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ..SimpleObject import SimpleObject
# Inners
from ._process_helpers.process_validate import process_validate
from ._process_helpers.load_parameters_from_inners import load_parameters_from_inners
from ._process_helpers.process_logic import process_logic
from ._process_helpers.calculate_default import calculate_default
from ._process_helpers.process_decompose import process_decompose
# Annotations
if TYPE_CHECKING:
    from .._core.protocols import SimpleClassType


def create_object_class(
    class_name: str,
    inners: tuple["SimpleClassType", ...],
    logic: Callable,
    value_type: type | UnsetType = UNSET,
    validate: Callable | UnsetType = UNSET,
    decompose: Callable | UnsetType = UNSET,
):

    # 1. Zpracování logic
    _params = load_parameters_from_inners(inners)
    _logic = process_logic(logic, _params.keys())

    # 2. Infer type if not provided
    if value_type is UNSET:
        _default_value = calculate_default(logic, _params.values())
        value_type = type(_default_value)

    # 3. Prepare namespace
    namespace = {
        "_inners": inners,
        "_type": value_type,
        "_logic": _logic
    }

    # 4. Wrap validate if provided
    if validate is not UNSET:
        _validate = process_validate(validate)
        # noinspection PyTypeChecker
        namespace["_validate"] = classmethod(_validate)

    # 5. Wrap decompose if needed
    if decompose is not UNSET:
        _decompose = process_decompose(decompose)
        namespace["_decompose"] = classmethod(_decompose)

    # 6. Create class dynamically
    new_class = type(class_name, (SimpleObject,), namespace)

    return new_class