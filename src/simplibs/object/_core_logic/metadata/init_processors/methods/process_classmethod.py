from typing import Any, TYPE_CHECKING
from types import UnionType
# Inners
from .verifiers import (
    verify_classmethod,
    verify_params,
    verify_calculation,
    verify_annotations_and_defaults
)
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def process_classmethod(
    method_name: str,
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    expected_args_defaults: tuple | None,
    expected_kwargs_defaults: dict[str, Any],
    expected_param_types: dict[str, type | UnionType],
    expected_return_type: type | UnionType,
    owner_class: "SimpleClassLike",
    test_value:tuple = (),
    return_calculated_value: bool = False,
) -> Any:

    # 1. Základní ověření uživatelem definované metody
    need_validations, bound_method = verify_classmethod(
        method_name=method_name,
        owner_class=owner_class,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count,
    )

    # 2. Pokud je metoda nově definovaná
    if need_validations:

        # 2.1 Validace parametrů metody
        verify_params(
            expected_params=expected_params,
            expected_args_params_count=expected_args_params_count,
            bound_method=bound_method,
        )

        # 2.2 Příprava anotací anotací
        bound_method_annotations = {
            **expected_param_types,
            "return": expected_return_type
        }

        # 2.3 Validace defaultních hodnot a anotací (jsu-li zadané)
        if (bound_method.__func__.__annotations__ or
            bound_method.__func__.__defaults__ or
            bound_method.__func__.__kwdefaults__):
            verify_annotations_and_defaults(
                bound_method=bound_method,
                expected_params=expected_params,
                expected_args_params_count=expected_args_params_count,
                bound_method_annotations=bound_method_annotations,
                expected_args_defaults=expected_args_defaults,
                expected_kwargs_defaults=expected_kwargs_defaults
            )

        # 2.4 Zapsání zpracovaných dat
        bound_method.__func__.__defaults__ = expected_args_defaults
        bound_method.__func__.__kwdefaults__ = expected_kwargs_defaults
        bound_method.__func__.__annotations__ = bound_method_annotations

    # 3. Ověření logiky - Zkušební výpočet pro ověření logiky
    calculated_value = verify_calculation(
        bound_method=bound_method,
        test_value=test_value,
        expected_return_type=expected_return_type,
        owner_class=owner_class
    )

    # 4. Navrácení vypočtených hodnot
    if return_calculated_value:
        return bound_method, calculated_value
    return bound_method

