from simplibs.sentinels import UNSET
# Outers
from .....exceptions import SimpleObjectError
from ....._types import SimpleClassType
# Inners
from .validations.composition import (
    validate_default_matches_annotation,
    validate_default_validations,
    validate_decompose_is_set,
    validate_default_can_be_decompose,
    validate_default_validations_return_true
)


def process_default_for_composition(
    calculate_default,
    default_type,
    logic_method,
    decompose_method,
    validate_method,
    owner_class: SimpleClassType,
):

    # 1. Natažení inners
    row_default = owner_class.__dict__.get("_default", UNSET)

    # 2. Navrácení vypočítaného defaultu
    if row_default is UNSET:
        return calculate_default

    # 3. Kontrola předaného defaultu
    try:
        type_validation = isinstance(row_default, default_type)
        method_validation = validate_method(row_default)
        decompose_outcome = decompose_method(row_default)
    except (SimpleObjectError, TypeError, AttributeError):
        validate_default_validations(row_default, default_type, validate_method, calculate_default, owner_class)
        validate_decompose_is_set(decompose_method, calculate_default, owner_class)
        validate_default_can_be_decompose(row_default, decompose_method, calculate_default, owner_class)
        # Fail-safe: Pokud by náhodou validace nic nevyhodily, vyhodíme obecnou chybu
        raise

    # 4 Kontrola zda obě validace proběhli úspěšně
    if not type_validation or not method_validation:
        validate_default_matches_annotation(row_default, default_type, calculate_default, owner_class)
        validate_default_validations_return_true(
            row_default, method_validation, default_type, calculate_default, owner_class
        )

    # 5. Vytvoření nových defaultních hodnot pro logic
    logic_defaults = logic_method.__func__.__kwdefaults__
    new_logic_defaults = {
        key: value
        for key, value in zip(logic_defaults.keys(), decompose_outcome)
    }

    # 6. Zápis nových defaultních hodnot
    logic_method.__func__.__kwdefaults__ = new_logic_defaults
    decompose_method.__func__.__defaults__ = (row_default,)

    # 7. Navrácení defaultu a metod
    return row_default, logic_method, decompose_method, validate_method



