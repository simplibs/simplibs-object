from typing import TYPE_CHECKING
from numbers import Number
# Outers
from .._commons.constants import STEPPER
from ..core_mixins import NodesTuple
# Inners
from ._stepper_class import Stepper
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.numerical import EqualizerProtocol
    from ..._core.protocols.mixins.numerical.internal_types import SteppersMap
    from ..._core.protocols.instance import SimpleInstanceLike


class Equalizer(NodesTuple):
    """
    Poskytuje přístup k stepperu pro všechny inners.

    Garantuje přítomnost číselných ovladačů (stepperů) pro všechny sub-node prvky
    kompozice. Tyto ovladače jsou generovány dynamicky na základě blueprintu
    a jsou dostupné skrze dynamické properties s postfixem.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _composite_only = True
    _mutable_only = True
    _only_types = Number

    # Definice slotů
    __slots__ = ("_steppers",)

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

        # 1. Vytvoření potřebných properties
        for name in instance_cls.meta.node_names_set:

            # 1.1 Definice getteru
            def getter(self: "EqualizerProtocol", _name: str = name):
                return self._steppers[_name]

            # 1.2 Nastavení jména getteru a docstringu
            prop_name = f"{name}{STEPPER}"
            getter.__name__ = f"get_{prop_name}"
            getter.__doc__ = (
                f"Vrací Stepper objekt pro uzel `{name}`.\n"
                f"Generováno dynamicky podle struktury objektu."
            )

            # 1.3 Vytvoření property a uložení na třídu
            setattr(instance_cls, prop_name, property(getter))

        # 2. Navrácení pozměněné třídy
        return instance_cls

    # ----------------------------------------
    # Hook pro inicializaci
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "EqualizerProtocol"
    ) -> None:
        """
        Metoda, předávající svojí logiku do inicializačního procesu instance.
        """

        # 1. Inicializace předků
        super().init_mixins()

        # 2. Slovník se steppery pro všechny prvky
        self._steppers: "SteppersMap" = {
            instance.meta.name_snake: Stepper(instance)
            for instance, _ in self._nodes_tuple
        }
