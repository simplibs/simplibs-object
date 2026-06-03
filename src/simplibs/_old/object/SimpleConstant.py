from typing import Any
from simplibs.sentinels import UNSET
# Inners
from .SimpleBase import SimpleBase
from ._mixins.constant.ValidateType import ValidateType
from ._mixins.constant.Validate import Validate
from ._mixins.constant.IsValid import IsValid
from ._mixins.constant.Normalize import Normalize



class SimpleConstant(
    # Validate method
    IsValid,                # is_valid(cls, value: Any) -> bool
    Normalize,              # normalize(cls, value: Any, *, process_none: bool = False) -> Any
    Validate,               # validate(cls, value: Any, *, return_bool: bool = False) -> bool
    ValidateType,           # validate_type(cls, value: Any, *, return_bool: bool = False) -> bool
    # Základní třída
    SimpleBase,
):

    # ===================================
    # ZÁKLADNÍ ROZHRANÍ DEFINICE KONSTANTNÍ TŘÍDY
    # ===================================

    # Defaultní hodnota - Povinný pokud nemáme inners
    _default: Any = UNSET

    # Typ - Vždy povinný
    _type: type = UNSET

    @classmethod
    def _validate(cls, value: Any, *, return_bool: bool = False) -> bool | Exception:
        """Nepovinná doplňková validace."""
        return True

