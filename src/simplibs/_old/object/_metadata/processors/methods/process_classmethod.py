from simplibs.sentinels import UNSET
from typing import Any
from types import UnionType
# Outers
from ...._types import SimpleClassType
# Inners
from .classmethod import verify_classmethod_existence
from .params import validate_bound_method_params
from .defaults import process_bound_method_kwargs_defaults
from .annotations import process_bound_method_annotations
from .testing import try_calculate_bound_method


def process_classmethod(
    method_name: str,
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    expected_args_defaults: tuple | None,
    expected_kwargs_defaults: dict[str, Any],
    expected_param_types: dict[str, type],
    expected_return_type: type | UnionType,
    owner_class: SimpleClassType,
    test_value:tuple = (),
    return_calculated_value: bool = False,
) -> classmethod | tuple:

    # 1. Základní ověření uživatelem definované metody
    need_validations, bound_method = verify_classmethod_existence(
        method_name=method_name,
        owner_class=owner_class,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count,
    )

    # 2. Pokud je metoda nově definovaná
    if need_validations:

        # 2.1 Validace parametrů metody
        validate_bound_method_params(
            expected_params=expected_params,
            expected_args_params_count=expected_args_params_count,
            bound_method=bound_method,
        )

        # 2.2 Zpracování defaultních hodnot metody
        bound_method_kwargs_defaults = process_bound_method_kwargs_defaults(
            expected_kwargs_defaults=expected_kwargs_defaults,
            expected_param_types=expected_param_types,
            bound_method=bound_method,
        )

        # 2.3 Zpracování anotací
        bound_method_annotations = process_bound_method_annotations(
            expected_param_types=expected_param_types,
            expected_return_type=expected_return_type,
            bound_method=bound_method,
        )

        # 2.4 Zapsání zpracovaných dat
        bound_method.__func__.__defaults__ = expected_args_defaults
        bound_method.__func__.__kwdefaults__ = bound_method_kwargs_defaults
        bound_method.__func__.__annotations__ = bound_method_annotations

    # 3. Ověření logiky - Zkušební výpočet pro ověření logiky
    calculated_value = try_calculate_bound_method(
        bound_method=bound_method,
        test_value=test_value,
        expected_return_type=expected_return_type,
        owner_class=owner_class
    )

    # 4. Navrácení vypočtených hodnot
    if return_calculated_value:
        return bound_method, calculated_value,
    return bound_method

