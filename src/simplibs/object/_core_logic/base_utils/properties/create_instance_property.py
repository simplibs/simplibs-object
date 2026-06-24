from typing import Any
from operator import attrgetter
# Outers
from ....protocols import SimpleMetadataType


def create_instance_property(
    inner_meta: SimpleMetadataType,
    path: tuple[str, ...]
) -> property:
    """
    Vytváří read-only property pro přístup k instanci inneru
    (atomu nebo kompozice) přes veřejné API.
    Např. <obj>.motor_instance → <obj>._motor
    """

    # 1. Rychlý přístup k privátnímu slotu
    get_inner_instance = attrgetter(*path)

    # 2. Getter
    def getter(self) -> Any:
        return get_inner_instance(self)

    # 3. Anotace getteru (pokud nemáš instanční typ, necháme Any)
    getter.__annotations__ = {"return": Any}

    # 4. Docstring
    doc_string = (
        f"Instance vnitřního prvku `{inner_meta.name_snake}`.\n"
        f"\n"
        f"Getter vrací instanci atomu nebo kompozice uloženou v privátním slotu "
        f"`{inner_meta.name_private}`.\n"
        f"Tato property je read-only – přiřazení nové instance není povoleno."
    )

    # 5. Read-only property (bez setteru)
    return property(
        fget=getter,
        doc=doc_string,
    )


