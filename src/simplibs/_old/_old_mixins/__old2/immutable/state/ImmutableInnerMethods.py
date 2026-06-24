# Inners
from .ImmutableMethods import ImmutableMethods


class ImmutableInnerMethods(ImmutableMethods):

    # Definice určení
    _immutable_only = True
    _composite_only = True

    # Definice slotů
    __slots__ = ()

    # ---------------------------------------------------------
    # Hook volaný z create_instance
    # ---------------------------------------------------------
    @staticmethod
    def __extend_instance_class__(instance_cls):

        # 1. Procházení uzlů
        for name in instance_cls.meta.node_names_tuple:

            # 2. Definice metody(
            # )Všechny používají metodu pro kompozice protože ta konstanty předává na with_constant
            def method(self, value, _name=name):
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

