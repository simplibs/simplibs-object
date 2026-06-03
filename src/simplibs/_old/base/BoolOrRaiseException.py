from typing import Any, Optional, Type, Union

from simplibs.exception import SimpleException


class BoolOrRaiseException:

    @classmethod
    def bool_or_raise_exception(
        cls,
        return_bool: bool = False,
        *,
        error_name: str = "VALIDATION ERROR",
        value_label: str = "value",
        value: Any,
        expected: str,
        problem: Optional[str] = None,
        how_to_fix: Optional[Union[list[str], str]] = None,
        context: Optional[str] = None,
        exception: Optional[Union[Exception, Type[Exception]]] = None,
    ) -> bool:
        """
        Helper method for custom validation in '_validate'.
        Returns False if 'return_bool' is True, otherwise raises a formatted SimpleException.
        """

        if return_bool:
            return False

        # Zajištění, že how_to_fix má rozumný základ, pokud uživatel nic nepošle
        if how_to_fix is None:
            how_to_fix = [
                f"Ensure the data provided to '{cls.__name__}' meets the validation criteria.",
                "Verify the input source for potential data corruption or incorrect formatting."
            ]

        # Pokud uživatel pošle jen jeden string místo listu, můžeme to interně ošetřit v SimpleException,
        # ale zde to necháme v čisté podobě pro našeptávač.

        raise SimpleException(
            error_name=error_name,
            value_label=value_label,
            value=value,
            expected=expected,
            problem=problem or f"Validation failed in the custom '_validate' method of '{cls.__name__}'.",
            how_to_fix=how_to_fix,
            context=context or f"Triggered within {cls.__name__} validation logic.",
            exception=exception or ValueError,
        )


