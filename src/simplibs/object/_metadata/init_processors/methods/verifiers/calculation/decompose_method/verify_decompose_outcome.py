from typing import Any
# Outers
from ......._types import SimpleClassType, ClassMethodProtocol
# Inners
from .validations import (
    raise_decompose_unvalide_outcome_length,
    validate_decompose_unvalide_item_type,
    validate_decompose_unvalide_item_value
)


def verify_decompose_outcome(
    calculate_default: tuple[Any, ...],
    owner_class: SimpleClassType,
    bound_method: ClassMethodProtocol,
):

    # 1. Získání inners
    # noinspection PyProtectedMember
    inners = owner_class._inners

    # 2. Kontrola délky (počet inners musí odpovídat počtu vrácených hodnot)
    if len(calculate_default) != len(inners):
        raise_decompose_unvalide_outcome_length(calculate_default, inners, bound_method)

    # 3. Kontrola typů jednotlivých prvků
    for i, inner in enumerate(inners):
        inner: SimpleClassType  # Přetypování pro PyCharm

        # 3.1 Získání hodnot
        value = calculate_default[i]
        expected_type = inner.meta.value_type

        # 3.2 Kontrola typu a vypočítané hodnoty
        if not isinstance(value, expected_type) and value != inner.meta.default:
            validate_decompose_unvalide_item_type(value, expected_type, inner, inners, bound_method)
            validate_decompose_unvalide_item_value(value, inner, inners, bound_method)
