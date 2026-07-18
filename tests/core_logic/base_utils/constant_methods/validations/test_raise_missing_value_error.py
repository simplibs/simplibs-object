from typing import TYPE_CHECKING, NoReturn
# Outers
from .....exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleConstantProtocol


def raise_missing_value_error(
    cls: "SimpleConstantProtocol"
) -> NoReturn:
    """
    Vyvolá chybu, pokud je předáno None tam, kde je vyžadována hodnota.
    """
    raise SimpleLogicError(
        error_name="MISSING VALUE ERROR",
        label="value",
        value=None,
        expected=f"Platná instance typu {cls.meta.value_type_name} (nikoliv None)",
        problem=f"Třída '{cls.__name__}' vyžaduje konkrétní hodnotu, ale obdržela 'None'.",
        how_to_fix=(
            "Předejte platnou hodnotu nebo instanci vyžadovaného typu.",
            "Pokud chcete, aby systém při zadání 'None' automaticky použil výchozí hodnotu, "
            "nastavte při volání 'process_none=True'."
        ),
        context=f"Fáze normalizace třídy {cls.__name__}",
        exception=ValueError
    )