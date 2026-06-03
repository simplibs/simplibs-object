from typing import Any, NoReturn
# Outers
from ......exceptions import SimpleObjectLogicError

def raise_type_error(
    cls: type,
    value: Any,
    value_type: type | tuple
) -> NoReturn:
    """
    Vyvolá detailní SimpleObjectLogicError při nesouladu typů.
    """
    # Příprava popisu očekávaných typů
    if isinstance(value_type, tuple):
        expected_types = ", ".join(t.__name__ for t in value_type)
    else:
        expected_types = value_type.__name__

    raise SimpleObjectLogicError(
        error_name="TYPE ERROR",
        value_label="value",
        value=value,
        expected=f"Instance typu '{expected_types}'",
        problem=f"Předaná hodnota neodpovídá vyžadovanému typu pro třídu '{cls.__name__}'.",
        how_to_fix=(
            f"Ujistěte se, že předávaná hodnota je instancí: {expected_types}.",
            "Zkontrolujte, zda nedochází k nechtěné konverzi typu před touto validací."
        ),
        context=f"Runtime vynucení typu pro {cls.__name__}",
        exception=TypeError
    )