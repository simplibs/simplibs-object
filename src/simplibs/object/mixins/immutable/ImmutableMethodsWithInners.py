from typing import Any, TYPE_CHECKING
# Inners
from .ImmutableMethods import ImmutableMethods
# Annotations
if TYPE_CHECKING:
    from ...protocols.mixins.immutable import ImmutableMethodsWithInnersProtocol
    from ...protocols.instance import SimpleInstanceLike


class ImmutableWithInners(ImmutableMethods):
    """
    Přidává základní třídě kromě základních metod i metody ke všem inners.

    Garantuje přítomnost dynamicky generovaných imutabilních metod (setterů)
    pro jednotlivé vnitřní prvky (např. `obj.with_uzel(value)`).
    Všechny tyto metody produkují novou transformovanou instanci (Self).
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _immutable_only = True
    _composite_only = True

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Hook pro úpravu instanční třídy
    # ----------------------------------------

    @staticmethod
    def __extend_instance_class__(
        instance_cls: "SimpleInstanceLike"
    ) -> "SimpleInstanceLike":
        """
        Interní metoda pro připojení prvků k třídě, před inicializačním procesem.
        """

        # 1. Procházení uzlů
        for name in instance_cls.meta.node_names_set:

            # 2. Definice metody
            # (Všechny používají metodu pro kompozice protože ta konstanty předává na with_constant)
            def method(self: "ImmutableMethodsWithInnersProtocol", value: Any, _name: str=name):
                return self.with_composite(_name, value)

            # 3. Nastavení inerních prvků
            method_name = f"with_{name}"
            method.__name__ = method_name
            method.__doc__ = (
                f"Immutable setter pro hodnotu `{name}`.\n"
                f"Vrací novou immutable instanci se změněnou hodnotou `{name}`."
            )

            # 4. Vytvoření atributu metody
            setattr(instance_cls, method_name, method)

        # 5. Navrácení upravené třídy
        return instance_cls

