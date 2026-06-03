from typing import Any, NoReturn
from ......exceptions import SimpleObjectLogicError

def raise_validation_error(
    cls: type,
    value: Any,
    original_exception: Exception
) -> NoReturn:
    """
    Vyvolá standardizovanou chybu při selhání uživatelské validace.
    """
    # 1. Pokud jde o naši známou výjimku (LogicError nebo MetadataError),
    # necháme ji "letět" dál beze změny, protože už má správný formát.
    if isinstance(original_exception, SimpleObjectLogicError):
        raise

    # 2. Cizí nebo neočekávané výjimky obalíme do našeho standardu,
    # abychom zachovali jednotný formát chybových hlášení.
    raise SimpleObjectLogicError(
        error_name="VALIDATION ERROR",
        value_label="value",
        value=value,
        expected="Hodnota splňující podmínky uživatelské validace.",
        problem=f"Během interní validace třídy '{cls.__name__}' došlo k neočekávané chybě.",
        how_to_fix=(
            "Prověřte implementaci své metody '_validate' (např. zda neobsahuje chyby v logice).",
            "Pro vyvolávání chyb v '_validate' používejte 'SimpleObjectLogicError'.",
            "Zkontrolujte, zda vstupní data odpovídají předpokladům vaší validační logiky."
        ),
        context=f"Selhání uživatelské validace u {cls.__name__}",
        exception=original_exception
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