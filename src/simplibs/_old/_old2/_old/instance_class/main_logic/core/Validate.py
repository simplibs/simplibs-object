from typing import Any



# core/Validate.py
class ValidateMixin:
    """Instanční delegace validačních metod na classmethody."""
    __slots__ = ()
    value: Any

    # 1. Opět ten Sentinel (Strážce)
    # I tady platí moje poznámka z LogicMixin.
    # Pokud by self.value mohlo být legitimně None (např. u nepovinného pole),
    # pak value is None v podmínce neroliší mezi „uživatel nic neposlal“
    # a „uživatel poslal None“.
    # Doporučení: Pokud tvůj systém počítá s tím, že None je validní hodnota,
    # použij v metodách stejný _SENTINEL jako u logiky.


    def validate(self, value: Any = None, *, return_bool: bool = False) -> bool:
        """Deleguje na cls.validate(value)."""
        value_to_check = self.value if value is None else value
        return self.__class__.validate(value_to_check, return_bool=return_bool)

    def validate_type(self, value: Any = None, *, return_bool: bool = False) -> bool:
        """Deleguje na cls.validate_type(value)."""
        value_to_check = self.value if value is None else value
        return self.__class__.validate_type(value_to_check, return_bool=return_bool)

    def is_valid(self, value: Any = None) -> bool:
        """Deleguje na cls.is_valid(value)."""
        value_to_check = self.value if value is None else value
        return self.__class__.is_valid(value_to_check)

    def normalize(self, value: Any = None, *, process_none: bool = False) -> Any:
        """Deleguje na cls.normalize(value)."""
        value_to_check = self.value if value is None else value
        return self.__class__.normalize(value_to_check, process_none=process_none)
