from typing import Any
from simplibs.sentinels import UNSET
# Outers
from ......protocols import SimpleClassType, ClassMethodProtocol
# Inners
from .decompose_method import verify_decompose_outcome
from .validations import raise_method_raised_exceptions, raise_method_return_unvalide_outcome_type


def verify_calculation(
    bound_method: ClassMethodProtocol,
    test_value: Any,
    expected_return_type: type,
    owner_class: SimpleClassType,
):
    # 1. Definice výstupní proměné
    calculate_result = UNSET

    # 2. Zkušební výpočet
    try:
        calculate_result = bound_method(*test_value)
    except Exception as e:
        raise_method_raised_exceptions(e, bound_method)

    # 3. Kontrola zda vypočítaná hodnota odpovídá očekávanému typu
    if not isinstance(calculate_result, expected_return_type):
        raise_method_return_unvalide_outcome_type(calculate_result, expected_return_type, bound_method)

    # 4. Kontrola vnitřních položek pro _decompose
    if bound_method.__func__.__name__ == "_decompose":
        verify_decompose_outcome(calculate_result, owner_class, bound_method)

    # 5. Navrácen vypočítené hodnoty
    return calculate_result