from typing import Any, Optional
from operator import attrgetter


def create_constant_property(
    meta: SimpleMetadataType,
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

    # -----------------------------
    # 1) Docstring (společný základ)
    # -----------------------------
    doc_string = (
        f"Hodnota typu `{meta.value_type_name}`.\n\n"
        f"Getter vrací normalizovanou hodnotu uloženou "
        f"{'v atomu' if path is None else 've vnitřním atomu'}.\n"
    )

    # -----------------------------
    # 2) Getter
    # -----------------------------
    if path is None:
        # Atomická property
        def getter(self) -> Any:
            return self._value
    else:
        # Inner atom property
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
        # Atomická property → zapisujeme do self
        def setter(self, value: Any) -> None:
            if self._locked:
                raise ValueError(f"{self.__class__.__name__} is locked.")
            self._root_value_setter(value, recalculate_up=True)
            self._log_outcome(value)
    else:
        # Inner atom property → zapisujeme do inner instance
        get_inner_instance = attrgetter(*path)

        def setter(self, value: Any) -> None:
            inner_instance = get_inner_instance(self)
            inner_instance._root_value_setter(value, recalculate_up=True)

    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # -----------------------------
    # 5) Docstring pro mutable
    # -----------------------------
    doc_string += (
        "Setter provádí normalizaci hodnoty, uložení a "
        "spouští aktualizační kaskádu směrem nahoru."
    )

    # -----------------------------
    # 6) Finální property
    # -----------------------------
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )
