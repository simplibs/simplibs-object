from typing import Any, Dict


class LogicMixin:
    """
    Instanční delegace metod create_value, decompose_value a update_value
    na classmethody třídy SimpleBase.
    """
    __slots__ = ()
    value: Any

    def create_value(self, **kwargs) -> Any:
        """Deleguje na cls.create_value(**kwargs)."""
        return self.__class__.create_value(**kwargs)

    def decompose_value(self, value: Any = None) -> Dict[str, Any]:
        """
        Deleguje na cls.decompose_value(value).
        Pokud není předaná hodnota, použije self.value.
        """
        value_to_use = self.value if value is None else value
        return self.__class__.decompose_value(value_to_use)

    def update_value(self, value: Any = None, **kwargs) -> Any:
        """
        Deleguje na cls.update_value(value, **kwargs).
        Pokud není předaná hodnota, použije self.value.
        """
        # Problém: Pokud zavolám obj.update_value(None, jmeno="Petr"),
        # tvoje logika vyhodnotí value is None jako pravdu a dosadí self.value.
        # Co když ale uživatel chce poslat None jako hodnotu k aktualizaci
        # (např. u objektu, který None povoluje)?
        value_to_use = self.value if value is None else value
        return self.__class__.update_value(value_to_use, **kwargs)