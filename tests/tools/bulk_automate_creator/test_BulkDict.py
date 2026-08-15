from dataclasses import dataclass
from typing import Any, Callable, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType

# Inners
from ..create_simple_object import create_simple_object
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols import SimpleClassType, SimpleMixinLike

@dataclass
class BulkDict:

    class_name: str
    default: Any | UnsetType = UNSET
    inners: tuple["SimpleClassType", ...] | UnsetType = UNSET
    value_type: type | UnsetType = UNSET
    validate: Callable | UnsetType = UNSET
    logic: Callable | UnsetType = UNSET
    decompose: Callable | UnsetType = UNSET
    return_instance: bool  = False
    mixins: tuple["SimpleMixinLike", ...] = (),
    as_atom: bool = False
    mutable: bool = True

    def create_simple_object(self):
        return create_simple_object(
            class_name=self.class_name,
            default=self.default,
            inners=self.inners,
            value_type=self.value_type,
            validate=self.validate,
            logic=self.logic,
            decompose=self.decompose,
            return_instance=self.return_instance,
            as_atom=self.as_atom,
            mutable=self.mutable,
        )

    def __post_init__(self):

        # 1) Konstantní objekt
        if self.default is not UNSET:
            if (
                self.inners is not UNSET or
                self.logic is not UNSET or
                self.decompose is not UNSET
            ):
                raise ValueError(
                    "Default může být zadán pouze pro konstantu "
                    "(inners, logic, decompose musí být UNSET)."
                )
            return

        # 2) Kompozitní objekt
        if self.inners is not UNSET:
            if self.logic is UNSET:
                raise ValueError(
                    "Nevyplněné logic — pro kompozici musí být zadáno."
                )
            return

        # 3) Nevalidní vstupní data
        raise ValueError(
            "Nevalidní vstupní data — musí být zadán default pro konstantu "
            "nebo inners + logic pro kompozici."
        )
