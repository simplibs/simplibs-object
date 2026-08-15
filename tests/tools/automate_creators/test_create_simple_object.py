from typing import Any, Callable, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .create_constant_class import create_constant_class
from .create_object_class import create_object_class
# Annotations
if TYPE_CHECKING:
    from .._core.protocols import SimpleClassType, SimpleMixinLike


def create_simple_object(
    class_name: str,
    default: Any | UnsetType = UNSET,
    inners: tuple["SimpleClassType", ...] | UnsetType = UNSET,
    value_type: type | UnsetType = UNSET,
    validate: Callable | UnsetType = UNSET,
    logic: Callable | UnsetType = UNSET,
    decompose: Callable | UnsetType = UNSET,
    return_instance: bool = False,
    mixins: tuple["SimpleMixinLike", ...] = (),
    as_atom: bool = False,
    mutable: bool = True,
):

    # Vtyovření třídy pro konstantu
    if default is not UNSET:
        if inners is not UNSET or logic is not UNSET or decompose is not UNSET:
            raise "Default může být zadáím pouze pro konstantu"
        _class = create_constant_class(
            class_name=class_name,
            default=default,
            value_type=value_type,
            validate=validate,
        )

    # Vtyvoření třídy pro kompoizici
    elif inners is not UNSET:
        if logic is UNSET:
            raise "Nevyplněné logic"
        _class = create_object_class(
            class_name=class_name,
            inners=inners,
            logic=logic,
            value_type=value_type,
            validate=validate,
            decompose=decompose,
        )

    else:
        raise "nevalidní vstupní data - musí být zadán default pro konstantu a nebo inners a logic pro kompozicii"

    # Navrácení instance
    if return_instance:
        return _class(mixins, as_atom=as_atom, mutable=mutable)

    # Navráícení třídy
    return _class


