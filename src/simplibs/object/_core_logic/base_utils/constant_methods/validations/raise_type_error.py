from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from .....exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleConstantProtocol


def raise_type_error(
    cls: "SimpleConstantProtocol",
    value: Any,
) -> NoReturn:
    """
    Vyvolá detailní SimpleLogicError při nesouladu typů.
    """

    expected_types = cls.meta.value_type_name

    raise SimpleLogicError(
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