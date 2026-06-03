from typing import Any
# Inners
from .validations import validate_method_default_is_valid_type


def process_bound_method_kwargs_defaults(
    expected_kwargs_defaults: dict[str, Any],
    expected_param_types: dict[str, type],
    bound_method: classmethod,
) -> dict[str, Any]:

    # 1. Příprava dat
    method_kwargs_defaults = bound_method.__func__.__kwdefaults__ or {}

    # 2. Validace
    if method_kwargs_defaults:

        # 2.1 Cyklus skrze defaultní hodnoty
        for name, value in method_kwargs_defaults.items():

            # 2.2 Načtení očekávaného typu
            expected_type = expected_param_types.get(name)

            # 2.3 Kontrola zda hodnota odpovídá očekávanému typu
            if not isinstance(value, expected_type):
                validate_method_default_is_valid_type(value, expected_type, bound_method)

    # 3. Zápis
    final_defaults = {
        **expected_kwargs_defaults,
        **method_kwargs_defaults,
    }

    # 4. Návrat finálního slovníku
    return final_defaults