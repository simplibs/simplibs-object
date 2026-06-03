import inspect
from typing import Any, NoReturn, Type
# Outers
from ....exceptions import SimpleObjectLogicError
# Inners
from .utils.extract_clean_code_lines import extract_clean_code_lines

def raise_validation_error(
    cls: type,
    value: Any,
) -> NoReturn:
    """
    Vyvolá standardizovanou chybu při selhání uživatelské validace.
    """

    # 1. Příprava dat:
    try:
        validate_func = cls.meta.validate.__func__
        validate_source_list = extract_clean_code_lines(validate_func)
    except Exception:
        validate_source_list = ["    <source code not available>"]

    # 2. Výjimka pro případ že uživatelem definovaná validace vrátila false
    # a požadované je vyvolání výjimky.
    raise SimpleObjectLogicError(
        error_name="VALIDATION ERROR",
        value_label="value",
        value=value,
        expected="Hodnota splňující podmínky uživatelské validace.",
        problem=f"Hodnota nesplňuje podmínky validního objektu.",
        how_to_fix=(
            "Hodnota vyhovuje validaci skrze typ, ale nevyhovuje specifické vylidaci.",
            "Zkontrolujte, zda vstupní hodnota odpovídají předpokladům validační logiky.",
            "Přepis validační logiky:",
            *validate_source_list
        ),
        context=f"Selhání uživatelské validace u {cls.__name__}",
        exception=ValueError
    )


    # raise SimpleObjectLogicError(
    #     error_name="VALIDATION ERROR",
    #     value_label="value",
    #     value=value,
    #     expected="Hodnota splňující podmínky metody '_validate'",
    #     problem=f"Během interní validace třídy '{cls.__name__}' došlo k neočekávané chybě.",
    #     how_to_fix=(
    #         "Pro vyvolávání chyb v '_validate' používejte 'SimpleObjectLogicError' "
    #         "nebo pomocnou metodu 'cls.bool_or_raise_exception()'.",
    #         "Pokud vyvoláváte výjimku manuálně, respektujte parametr 'return_bool'.",
    #         "Prověřte implementaci své metody '_validate' (např. zda neobsahuje KeyError, AttributeError).",
    #         "Zkontrolujte, zda vstupní data odpovídají předpokladům vaší validační logiky."
    #     ),
    #     exception=type(e)
    # )