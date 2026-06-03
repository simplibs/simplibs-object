# Outers
from ..utils import exception_info_for_classmethod
# Inners
from .validations import (
    validate_row_method_is_defined,
    validate_row_method_is_callable,
    validate_row_method_is_classmethod
)


def verify_classmethod_existence(
    method_name: str,
    must_exist: bool,
    owner_class: type,
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
) -> bool:

    # 1. Příprava dat
    row_method = owner_class.__dict__.get(method_name, None)

    # 2. Validace existence
    if not row_method and not must_exist:
        return False

    # 3. Validace dekorátoru
    if isinstance(row_method, classmethod):
        return True

    # 4. Příprava dat pro výjimku
    bound_method = getattr(owner_class, method_name)
    base_info_for_exception = exception_info_for_classmethod(
        bound_method=bound_method,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count
    )

    # 5. Vyvolání výjimky
    validate_row_method_is_defined(method_name, owner_class, base_info_for_exception)
    validate_row_method_is_callable(row_method, base_info_for_exception)
    validate_row_method_is_classmethod(row_method, base_info_for_exception)
    return False


def verify_classmethod_existence(
    method_name: str,
    owner_class: type,
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
) -> bool:

    # 1. Příprava dat
    row_method = owner_class.__dict__.get(method_name, None)

    # 2. Validace existence
    if not row_method:
        return False

    # 3. Validace dekorátoru
    if isinstance(row_method, classmethod):
        return True

    # 4. Příprava dat pro výjimku
    bound_method = getattr(owner_class, method_name)
    base_info_for_exception = exception_info_for_classmethod(
        bound_method=bound_method,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count
    )

    # 5. Vyvolání výjimky
    validate_row_method_is_defined(method_name, owner_class, base_info_for_exception)
    validate_row_method_is_callable(row_method, base_info_for_exception)
    validate_row_method_is_classmethod(row_method, base_info_for_exception)
    return False