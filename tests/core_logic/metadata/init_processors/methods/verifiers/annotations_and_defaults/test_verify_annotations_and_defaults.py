from typing import Any, TYPE_CHECKING
# Outers
from .._exceptions_helpers import exception_info_for_classmethod
# Inners
from .validations import validate_args_defaults, validate_kwargs_defaults, validate_annotations
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol


def verify_annotations_and_defaults(
    bound_method: "ClassMethodProtocol",
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    bound_method_annotations: dict[str, Any],
    expected_args_defaults: tuple | None,
    expected_kwargs_defaults: dict[str, Any],
):

    # 1. Příprava dat pro výjimku
    base_info_for_exception = exception_info_for_classmethod(
        bound_method=bound_method,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count
    )

    # 2. Validace anotací (jsu-li zadané)
    if bound_method.__func__.__annotations__:
        validate_annotations(bound_method_annotations, bound_method, base_info_for_exception)

    # 3. Validace defaultních args hodnot
    if bound_method.__func__.__defaults__:
        validate_args_defaults(expected_args_defaults, expected_params, bound_method, base_info_for_exception)

    # 4. Validace defaultních kwargs hodnot
    if bound_method.__func__.__kwdefaults__:
        validate_kwargs_defaults(expected_kwargs_defaults, bound_method, base_info_for_exception)
