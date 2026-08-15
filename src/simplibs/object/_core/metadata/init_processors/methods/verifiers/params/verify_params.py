from typing import TYPE_CHECKING
# Outers
from .._exceptions_helpers import (
    exception_info_for_classmethod,
    expected_structure_for_classmethod,
)
# Inners
from .validations import (
    validate_method_param_match_expected,
    validate_method_has_exact_args_count,
    validate_method_not_use_param_placeholders,
)
# Annotations
if TYPE_CHECKING:
    from ......protocols.methods import ClassMethodProtocol


def verify_params(
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    bound_method: "ClassMethodProtocol",
) -> None:
    """Verifies classmethod bytecode signature parameters."""

    # 1. Extract bytecode metadata
    code = bound_method.__func__.__code__
    total_params_count = code.co_argcount + code.co_kwonlyargcount
    method_params = code.co_varnames[:total_params_count]
    has_varargs = bool(code.co_flags & 0x04)
    has_varkwargs = bool(code.co_flags & 0x08)

    # 2. Short-circuit: happy path
    if (
        not has_varargs
        and not has_varkwargs
        and code.co_argcount == expected_args_params_count
        and method_params == expected_params
    ):
        return

    # 3. Build exception metadata
    exception_info = exception_info_for_classmethod(bound_method)
    expected_structure = expected_structure_for_classmethod(
        bound_method,
        expected_params,
        expected_args_params_count,
    )

    # 4. Run micro-validations
    validate_method_param_match_expected(
        method_params,
        expected_params,
        exception_info,
        expected_structure,
    )

    validate_method_has_exact_args_count(
        expected_args_params_count,
        code.co_argcount,
        exception_info,
        expected_structure,
    )

    validate_method_not_use_param_placeholders(
        has_varargs,
        has_varkwargs,
        exception_info,
        expected_structure,
    )



_DESIGN_NOTES = """
# verify_params

## Purpose
Validates the bytecode-level parameter signature of a classmethod.  
Ensures that the method uses the correct parameter names, correct argument count,
and does not use dynamic placeholders (`*args`, `**kwargs`).

## Step-by-step behavior

### 1. Bytecode extraction
The function reads:
- positional argument count (`co_argcount`)
- keyword-only argument count (`co_kwonlyargcount`)
- parameter names (`co_varnames`)
- varargs / varkwargs flags (`co_flags`)

This avoids expensive `inspect` parsing.

### 2. Short-circuit path
If:
- no `*args`
- no `**kwargs`
- argument count matches
- parameter names match

→ the function returns immediately.

This is the fast path for correct signatures.

### 3. Exception metadata
If the signature is incorrect:
- `exception_info` → (class_name, method_name, context)
- `expected_structure` → blueprint of the correct method signature

Both are passed to validators.

### 4. Micro-validations
Three validators isolate the exact failure:
- wrong parameter names or order  
- wrong argument count  
- use of `*args` or `**kwargs`

Each produces a precise `SimpleDefinitionError` with a copy‑paste blueprint.

## Notes
This function is used for all classmethod types:
- `_validate`
- `_logic`
- `_decompose`
"""