from typing import Any
# Outers
from ......._types import SimpleClassType
# Inners
from .validate_decompose_outcome_length import validate_decompose_outcome_length
from .validate_decompose_item_type import validate_decompose_item_type


def validate_decompose_outcome(
    calculate_default: tuple[Any, ...],
    owner_class: SimpleClassType,
    bound_method: classmethod,
):

    # 1. Získání inners
    inners = owner_class._inners

    # 2. Kontrola délky (počet inners musí odpovídat počtu vrácených hodnot)
    if len(calculate_default) != len(inners):
        validate_decompose_outcome_length(calculate_default, inners, bound_method)

    # 3. Kontrola typů jednotlivých prvků
    for i, inner in enumerate(inners):

        # 3.1 Získání hodnot
        value = calculate_default[i]
        expected_type = inner.meta.value_type

        # 3.2 Kontrola typu
        if not isinstance(value, expected_type):
            validate_decompose_item_type(value, expected_type, inner, inners, bound_method)

