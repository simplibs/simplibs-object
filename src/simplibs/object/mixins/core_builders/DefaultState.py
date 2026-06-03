# Outers
from ..._types import SimpleObjectInstanceType
from ..base_class import SimpleMixin
# Inners
from ._default_state_helpers import build_recursive_maps, copy_instance_values


class DefaultState(SimpleMixin):
    """
    Mixin, který instanci poskytne:
    - uložený výchozí stav (_default_state)
    - metody clone(), reset(), copy_from(), new_default_instance()
    """

    __slots__ = ("_default_state",)

    # ---------------------------------------------------------
    # 1) Hook volaný z create_instance → doplní _default_state
    # ---------------------------------------------------------
    @staticmethod
    def __extend_instance_class__(instance_cls):
        """
        Vytvoří a uloží výchozí instanci dané instanční třídy.
        """

        # 1. Vytvoření mapovacích slovníků
        if not hasattr(instance_cls, "_constants_map") or not hasattr(instance_cls, "_composites_map"):
            constants_map, composites_map = build_recursive_maps(instance_cls.meta)
            instance_cls._constants_map = constants_map
            instance_cls._composites_map = composites_map

        # 2. Přidání defaultní instance
        if not hasattr(instance_cls, "_default_state"):
            default = object.__new__(instance_cls)
            default.__init__()
            instance_cls._default_state = default

        # 3. Navrácení pozměněné třídy
        return instance_cls

    # ---------------------------------------------------------
    # 2) Vytvoří novou instanci se stejným stavem jako self
    # ---------------------------------------------------------
    def clone(self: SimpleObjectInstanceType):
        """
        Vytvoří novou instanci se stejným stavem jako tato instance.
        """
        new_instance = self._default_state.clone()
        copy_instance_values(self, new_instance)
        return new_instance

    # ---------------------------------------------------------
    # 3) Resetuje instanci do výchozího stavu
    # ---------------------------------------------------------
    def reset(self: SimpleObjectInstanceType):
        """
        Resetuje instanci do výchozího stavu (_default_state).
        """
        copy_instance_values(self._default_state, self)

    # ---------------------------------------------------------
    # 4) Vytvoří novou instanci výchozího stavu
    # ---------------------------------------------------------
    def new_default_instance(self):
        """
        Vrátí novou instanci, která odpovídá výchozímu stavu.
        """
        return self._default_state.clone()
