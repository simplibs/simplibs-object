# Outers
from ......_types import ClassMethodProtocol
from .._exceptions_helpers import exception_info_for_classmethod
# Inners
from .validations import (
    validate_method_has_exact_args_count,
    validate_method_not_use_param_placeholders,
    validate_method_param_match_expected
)


def verify_params(
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    bound_method: ClassMethodProtocol,
) -> None:

    # 1. Příprava dat
    # noinspection PyUnresolvedReferences
    code = bound_method.__func__.__code__
    total_params_count = code.co_argcount + code.co_kwonlyargcount
    method_params = code.co_varnames[:total_params_count]
    has_varargs = bool(code.co_flags & 0x04)
    has_varkwargs = bool(code.co_flags & 0x08)

    # 2. Podmínka pro Happy Path
    if (not has_varargs and
        not has_varkwargs and
        code.co_argcount == expected_args_params_count and
        method_params == expected_params):
        return

    # 3. Příprava dat pro výjimku
    base_info_for_exception = exception_info_for_classmethod(
        bound_method=bound_method,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count
    )

    # 4. Vyvolání výjimky
    validate_method_param_match_expected(method_params, expected_params, base_info_for_exception)
    validate_method_has_exact_args_count(expected_args_params_count, code.co_argcount, base_info_for_exception)
    validate_method_not_use_param_placeholders(has_varargs, has_varkwargs, base_info_for_exception)
