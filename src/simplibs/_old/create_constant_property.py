from typing import Any, Optional, TYPE_CHECKING
from operator import attrgetter
# Anotations
if TYPE_CHECKING:
    from ....protocols.metadata import SimpleMetadataLike
    from ....protocols.instance import SimpleInstanceLike


def create_constant_property(
    meta: "SimpleMetadataLike",
    *,
    mutable: bool = True,
    path: Optional[tuple[str, ...]] = None
) -> property:
    """
    Univerzální property pro atomickou hodnotu.

    - Pokud `path is None`, jedná se o atomickou property (self._value).
    - Pokud `path` obsahuje cestu, jedná se o inner-atom property.
    - Setter se generuje pouze pokud je `mutable=True`.
    """

    # 1. Docstring (společný základ)
    doc_string = (
        f"Hodnota typu `{meta.value_type_name}`.\n\n"
        f"Getter vrací normalizovanou hodnotu uloženou "
        f"{'v atomu' if path is None else 've vnitřním atomu'}.\n"
    )

    # 2. Definice getteru
    if path is None:

        # 2.1 Root property
        def getter(self: "SimpleInstanceLike") -> Any:
            return self._value
    else:
        # 2.2 Inner property
        get_inner_instance = attrgetter(*path)
        def getter(self: "SimpleInstanceLike") -> Any:
            return get_inner_instance(self).value

    # 2.3 Přidání anotace
    getter.__annotations__ = {"return": meta.value_type}

    # 3. Vyřízení pro immutable režim → jen getter
    if not mutable:
        return property(fget=getter, doc=doc_string)

    # 4. Definice setteru
    if path is None:

        # 4.1 Root property → zapisujeme do self
        def setter(self: "SimpleInstanceLike", value: Any) -> None:

            # 4.1.1 Ověření zda hodnota není zamčená
            if self._locked:
                raise ValueError(f"{self.__class__.__name__} is locked.")

            # 4.1.2 Zápis hodnoty
            self._root_value_setter(value, recalculate_up=True)

            # 4.1.3 Logování
            self._log_outcome(value)

    else:

        # 4.2 Inner property
        get_inner_instance = attrgetter(*path)
        def setter(self: "SimpleInstanceLike", value: Any) -> None:

            # 4.2.1 Načtení instance
            inner_instance: "SimpleInstanceLike" = get_inner_instance(self)

            # 4.2.3 Zápis hodnoty
            # noinspection PyProtectedMember
            inner_instance._root_value_setter(value, recalculate_up=True)

    # 4.3  Přidání anotace
    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # 5. Doplnění docstring pro mutable
    doc_string += (
        "Setter provádí normalizaci hodnoty, uložení a "
        "spouští aktualizační kaskádu směrem nahoru."
    )

    # 6. Vytvoření a navrácení property se setterem
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )
