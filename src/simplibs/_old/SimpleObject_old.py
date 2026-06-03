from __future__ import annotations
from typing import Any, ClassVar, Type, Tuple, Optional

from .mixins.base.validate_method import (
    IsValid,
    Normalize,
    Validate,
    ValidateType,
    BoolOrRaiseException,
)
from .mixins.base.base_method import (
    CreateValue,
    DecomposeValue,
    UpdateValue,
)
from .mixins.base.utils import (
    GetOrMakeCacheAttr,
    CreateMixinParameters
)
from ._metadata import (
    SimpleObjectMeta,
    SimpleObjectMetadata
)
from simplibs.sentinels import UNSET, UnsetType


class SimpleObject(
    # Validate method
    IsValid,                # is_valid(cls, value: Any) -> bool
    Normalize,              # normalize(cls, value: Any, *, process_none: bool = False) -> Any
    Validate,               # validate(cls, value: Any, *, return_bool: bool = False) -> bool
    ValidateType,           # validate_type(cls, value: Any, *, return_bool: bool = False) -> bool
    BoolOrRaiseException,   # def bool_or_raise_exception(cls, return_bool: bool = False, **kwargs) -> bool
    # Base method
    CreateValue,            # create_value(cls, **kwargs) -> Any
    DecomposeValue,         # decompose_value(cls, value: Any) -> Dict[str, Any]
    UpdateValue,            # update_value(cls, value: Any, **kwargs) -> Any
    # Utils
    GetOrMakeCacheAttr,     # _get_or_make_cache_attr(cls, cache_attr: str, method_name: str) -> Any
    CreateMixinParameters,  # MIXIN_PARAMS(cls), collect_mixin_parameters(cls)
    # Metadata
    metaclass=SimpleObjectMeta
):

    # ===================================
    # ZÁKLADNÍ ROZHRANÍ DEFINICE TŘÍDY
    # ===================================

    # Defaultní hodnota - Povinný pokud nemáme inners
    _default: ClassVar[Any] = UNSET

    # Typ - Vždy povinný
    _type: ClassVar[Optional[Type]] = UNSET

    # Inners - Uvádějí se pouze jsouli potřeba
    _inners: ClassVar[Tuple[SimpleObjectType, ...]] = UNSET

    @classmethod
    def _logic(cls, *args, **kwargs) -> UnsetType:
        """Povinná pro kompozici, vrací default pro atomy."""
        return UNSET

    @classmethod
    def _decompose(cls, value: Any) -> UnsetType:
        """Nepovinná, vrací None, pokud rozklad není podporován."""
        return UNSET

    @classmethod
    def _validate(cls, value: Any, *, return_bool: bool = False) -> bool | Exception:
        """Nepovinná doplňková validace."""
        return True

    # ===================================
    # METADATA PRO TŘÍDNÍ ATIBUTY
    # ===================================

    __metadata__: ClassVar[SimpleObjectMetadata]

