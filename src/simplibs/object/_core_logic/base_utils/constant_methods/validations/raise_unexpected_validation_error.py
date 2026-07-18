from typing import Any, NoReturn
# Outers
from ....exceptions import SimpleLogicError

def raise_unexpected_validation_error(
    cls: type,
    value: Any,
    original_exception: Exception
) -> NoReturn:
    """
    Vyvolá standardizovanou chybu při selhání uživatelské validace.
    """

    # 1. Cizí nebo neočekávané výjimky obalíme do našeho standardu,
    # abychom zachovali jednotný formát chybových hlášení.
    raise SimpleLogicError(
        error_name="VALIDATION ERROR",
        label="value",
        value=value,
        expected="Hodnota splňující podmínky uživatelské validace.",
        problem=f"Během interní validace třídy '{cls.__name__}' došlo k neočekávané chybě.",
        how_to_fix=(
            "Prověřte implementaci své metody '_validate' (např. zda neobsahuje chyby v logice).",
            "Pro vyvolávání chyb v '_validate' používejte 'SimpleLogicError'.",
            "Zkontrolujte, zda vstupní data odpovídají předpokladům vaší validační logiky."
        ),
        context=f"Selhání uživatelské validace u {cls.__name__}",
        exception=original_exception
    )


    # raise SimpleLogicError(
    #     error_name="VALIDATION ERROR",
    #     label="value",
    #     value=value,
    #     expected="Hodnota splňující podmínky metody '_validate'",
    #     problem=f"Během interní validace třídy '{cls.__name__}' došlo k neočekávané chybě.",
    #     how_to_fix=(
    #         "Pro vyvolávání chyb v '_validate' používejte 'SimpleLogicError' "
    #         "nebo pomocnou metodu 'cls.bool_or_raise_exception()'.",
    #         "Pokud vyvoláváte výjimku manuálně, respektujte parametr 'return_bool'.",
    #         "Prověřte implementaci své metody '_validate' (např. zda neobsahuje KeyError, AttributeError).",
    #         "Zkontrolujte, zda vstupní data odpovídají předpokladům vaší validační logiky."
    #     ),
    #     exception=type(e)
    # )