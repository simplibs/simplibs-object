
from typing import Optional, TYPE_CHECKING
from .value_helpers import create_value_getter
from .value_helpers import create_value_setter
if TYPE_CHECKING:
    from ....protocols.metadata import SimpleMetadataLike


def create_value_property(
    meta: "SimpleMetadataLike",
    *,
    is_constant: bool = True,
    mutable: bool = True,
    path: Optional[tuple[str, ...]] = None
) -> property:
    """
    Univerzální property pro atomickou i kompozitní hodnotu.

    - Pokud `is_composite=False`, jedná se o atomickou (constant) property.
    - Pokud `is_composite=True`, jedná se o kompozitní property.
    - Pokud `path is None`, property operuje přímo na self._value (root).
    - Pokud `path` obsahuje cestu, property operuje na vnitřní instanci.
    - Setter se generuje pouze pokud je `mutable=True`. U kompozitní property
      navíc vyžaduje `meta.is_decomposeable=True`.
    """

    # 1. Vytvoření getteru
    getter = create_value_getter(meta, path)

    # 2. Vytvoření docstringu pro getter
    doc_string = (
        f"Hodnota typu `{meta.value_type_name}`.\n\n"
        f"Getter vrací hodnotu "
        f"{'tohoto prvku' if path is None else 'vnitřního prvku'}.\n"
    )

    # 3. Navrácení getteru pro immutable verzy (nepoužívá setter)
    if not mutable:
        return property(
            fget=getter,
            doc=doc_string
        )

    # 4. Vytvoření setteru
    setter = create_value_setter(meta, is_constant, path)

    # 5. Doplnění docstring pro setter
    if is_constant:
        doc_string += (
            "Setter provádí normalizaci hodnoty, uložení a "
            "spouští aktualizační kaskádu směrem nahoru."
        )
    else:
        doc_string += (
            "Setter rozloží (dekomponuje) vstupní hodnotu a distribuuje ji "
            "do vnitřních prvků kompozice."
        )

    # 6. Vytvoření a navrácení property pro mutable verzy
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )