from typing import Any
# Outers
from ....._types import SimpleClassType
# Inners
from .validations import (
    validate_bound_method_outcome_type,
    validate_bound_method_raised_exceptions,
    validate_decompose_outcome
)


def try_calculate_bound_method(
    bound_method: classmethod,
    test_value: Any,
    expected_return_type: type,
    owner_class: SimpleClassType,
):
    # 1. Definice výstupní proměné
    calculate_result = None

    # 2. Zkušební výpočet
    try:
        calculate_result = bound_method(*test_value)
    except Exception as e:
        validate_bound_method_raised_exceptions(e, bound_method)

    # 3. Kontrola zda vypočítaná hodnota odpovídá očekávanému typu
    if not isinstance(calculate_result, expected_return_type):
        validate_bound_method_outcome_type(calculate_result, expected_return_type, bound_method)

    # 4. Kontrola vnitřních položek pro _decompose
    if bound_method.__func__.__name__ == "_decompose":
        validate_decompose_outcome(calculate_result, owner_class, bound_method)

    # 5. Navrácen vypočítené hodnoty
    return calculate_result