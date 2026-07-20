from typing import TYPE_CHECKING, Any
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike


def validate_hashing_for_immutable_value(
    cls: "SimpleClassLike"
) -> Any:
    """
    Ověří, že defaultní hodnota třídy je hashovatelná
    a může být použita v immutable instanci.

    - Pokusí se zavolat hash() nad cls.meta.default.
    - Pokud je hodnota nehashovatelná, vyvolá TypeError
      s informací o konkrétní třídě.
    - Používá se pouze při vytváření immutable instancí.
    """

    try:
        return hash(cls.meta.default)
    except TypeError:
        raise TypeError(
            f"Immutable instance '{cls.meta.class_name}' "
            f"cannot wrap non-hashable default value"
        )