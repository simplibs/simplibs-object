from typing import Any, Optional
from operator import attrgetter
# Outers
from ....protocols import SimpleMetadataType
# Inners
from .validations import raise_class_not_decomposeable


def create_composite_property(
    meta: SimpleMetadataType,
    *,
    mutable: bool = True,
    path: Optional[tuple[str, ...]] = None
) -> property:
    """
    Univerzální property pro kompozitní hodnotu.

    - Pokud `path is None`, jedná se o root composite property (self._value).
    - Pokud `path` obsahuje cestu, jedná se o inner-composite property.
    - Setter se generuje pouze pokud je `mutable=True` a kompozice
      podporuje dekompozici (`is_decomposeable=True`).
    """

    # -----------------------------
    # 1) Docstring (společný základ)
    # -----------------------------
    doc_string = (
        f"Kompozitní hodnota typu `{meta.value_type_name}`.\n\n"
        f"Getter vrací aktuální vypočítanou hodnotu "
        f"{'této kompozice' if path is None else 'vnitřní kompozice'}.\n"
    )

    # -----------------------------
    # 2) Getter
    # -----------------------------
    if path is None:
        # Root composite property
        def getter(self) -> Any:
            return self._value
    else:
        # Inner composite property
        get_inner_instance = attrgetter(*path)

        def getter(self) -> Any:
            return get_inner_instance(self).value

    getter.__annotations__ = {"return": meta.value_type}

    # -----------------------------
    # 3) Immutable režim → jen getter
    # -----------------------------
    if not mutable:
        return property(fget=getter, doc=doc_string)

    # -----------------------------
    # 4) Setter
    # -----------------------------
    if path is None:
        # Root composite setter
        def setter(self, value: Any) -> None:

            # 4.1 Ověření dekompozice
            if not meta.is_decomposeable:
                raise_class_not_decomposeable(meta)

            # 4.2 Zápis hodnoty
            self._root_value_setter(value, recalculate_up=True)

            # 4.3 Rozložení hodnoty do inners
            self._recalculate_inners()

            # 4.4 Logování
            self._log_outcome(value)

    else:
        # Inner composite setter
        get_inner_instance = attrgetter(*path)

        def setter(self, value: Any) -> None:

            inner_instance = get_inner_instance(self)

            # 4.1 Ověření dekompozice
            if not meta.is_decomposeable:
                raise_class_not_decomposeable(meta)

            # 4.2 Zápis hodnoty
            # noinspection PyProtectedMember
            inner_instance._root_value_setter(value, recalculate_up=True)

            # 4.3 Rozložení hodnoty do inners
            # noinspection PyProtectedMember
            inner_instance._recalculate_inners()

    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # -----------------------------
    # 5) Docstring pro mutable
    # -----------------------------
    doc_string += (
        "Setter rozloží (dekomponuje) vstupní hodnotu a distribuuje ji "
        "do vnitřních prvků kompozice."
    )

    # -----------------------------
    # 6) Finální property
    # -----------------------------
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )
