from typing import Any, TYPE_CHECKING
from simplibs.exception import SimpleException
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleConstantProtocol


def bool_or_raise_validate_error(
    cls: "SimpleConstantProtocol",
    value: Any,
    problem: str,
    *,
    return_bool: bool = False,
) -> bool:
    """Interní implementace sdílené validační logiky."""

    # 1. Kontrola zda se má vrátit bool
    if return_bool:
        return False

    # 2. Vyvolání předpřipravené výjimky
    raise SimpleException(
        error_name="VALIDATION ERROR",
        value_label="input_value",
        value=value,
        expected=f"Valid configuration for {cls.__name__}",
        problem=problem,
        how_to_fix=(
            f"Ensure the data provided to '{cls.__name__}' meets the validation criteria.",
            f"The expected base type or format is '{cls.meta.value_type_name}'."
        ),
        context=f"Triggered within custom validation of {cls.__name__}.",
        exception=ValueError,
    )



