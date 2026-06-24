from numbers import Number
# Outers
from ....protocols import SimpleInstanceType
from .._shared_logic.constants import STEPPER
from ..core_mixins import NodesTuple
# Inners
from ._utils.stepper_class import Stepper



# noinspection PyAttributeOutsideInit
class Equalizer(NodesTuple):

    # Definice určení
    _composite_only = True
    _mutable_only = True
    _only_types = Number

    # Definice slotů
    __slots__ = ("_steppers",)

    # Akce na instanční třídě před inicializací
    @staticmethod
    def __extend_instance_class__(instance_cls):

        # 1. Vytvoření potřebných properties
        for name in instance_cls.meta.node_names_set:

            # 1.1 Definice getteru
            def getter(self, _name=name):
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

    # Inicializace mixinu
    def init_mixins(self):
        super().init_mixins()
        self._steppers = {
            instance.meta.name_snake: Stepper(instance)
            for instance, _ in self.nodes_tuple
        }
