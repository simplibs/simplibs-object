# Outers
from ...._metadata.instance_builders.instance import create_instance
from ...common.core_logic import Snapshot


# noinspection PyAttributeOutsideInit
# noinspection PyProtectedMember
class DefaultState(Snapshot):
    """
    Mixin, který instanci poskytne:
    - uložený výchozí stav (_default_state)
    - metody clone_instance(), reset_to_default_values(), create_new_default_instance()
    """

    # Definice určení
    _mutable_only = True

    # Definice slotů
    __slots__ = ("_default_state_snapshot",)

    # Inicializace mixinu
    def init_mixins(self):
        super().init_mixins()
        self._default_state_snapshot = self._build_snapshot()

    # ---------------------------------------------------------
    # Klonování aktuální instance
    # ---------------------------------------------------------
    def clone_instance(self):
        """Vytvoří novou instanci se stejným stavem jako tato instance."""
        new_instance = self.create_new_default_instance()
        new_instance._restore_snapshot(self._build_snapshot())
        return new_instance

    # ---------------------------------------------------------
    # Reset hodnot do výchoz podoby
    # ---------------------------------------------------------
    def reset_to_default_values(self):
        """Resetuje instanci do výchozího stavu (_default_state)."""
        self._restore_snapshot(self._default_state_snapshot)

    # ---------------------------------------------------------
    # Vrátí novou instanci s defaultními hodnotami
    # ---------------------------------------------------------
    def create_new_default_instance(self):
        """
        Vrátí novou instanci stejného typu se stejným výchozím stavem,
        jaký měla tato instance při svém vzniku.

        Třída je zrekonstruována pomocí metadat:
        - owner_class (meta.owner_class)
        - __mixins__ (tuple mixinů použitých při vytvoření instance)
        - __is_constant__ (atom/composite režim)
        - __is_mutable__ (mutable/immutable režim)
        """
        return create_instance(
            cls=self.__class__.meta.owner_class,
            mixins=self.__class__.__mixins__,
            as_atom=self.__class__.__is_constant__,
            mutable=self.__class__.__is_mutable__,
            validate=False
        )

