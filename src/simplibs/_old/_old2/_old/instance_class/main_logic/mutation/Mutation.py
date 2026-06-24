from typing import Any

from ..core.Logic import LogicMixin
from ..core.Validate import ValidateMixin
from ..serialization.DictSerializer import DictSerializerMixin


# mutation/Mutation.py
class MutationMixin(LogicMixin, ValidateMixin, DictSerializerMixin):
    """Kompletní mixin pro mutace objektů — kopie, modifikace, výpočty."""
    __slots__ = ()

    def copy_self(self):
        """Vytvoří identickou kopii aktuálního objektu."""
        return self.from_dict(self.to_dict())

    def create_modified_instance(self, **kwargs):
        """
        Vytvoří kopii objektu s přepsanými parametry.

        Příklad:
            user.create_modified_instance(age=31)

        Validace probíhá automaticky přes __init__ → property setter → normalize().
        """
        current_data = self.to_dict()
        current_data.update(kwargs)
        return self.from_dict(current_data)

    def get_calculated_value(self, **kwargs) -> Any:
        """
        Vypočítá a vrátí hlavní hodnotu s novými parametry.
        Původní instance zůstává nezměněna.

        Příklad:
            new_total = price.get_calculated_value(tax=0.21)
        """
        temporary_instance = self.create_modified_instance(**kwargs)
        return temporary_instance.value

    def apply_update(self, **kwargs) -> Any:
        """
        Mutuje self.value na místě pomocou update_value().

        Příklad:
            obj.apply_update(width=100, height=200)

        Spustí _on_update() hook.
        """
        new_value = self.update_value(value=self.value, **kwargs)
        self.value = new_value
        if hasattr(self, "_on_update") and callable(self._on_update):
            self._on_update()
        return new_value
