from typing import Any

class InstanceBase:
    """Základní třída pro instanci."""

    __slots__ = ()  # Důležité! Aby základní třída nepřidávala __dict__

    def _on_update(self) -> None:
        """
        Základní implementace hooku.
        Může zůstat prázdná, slouží jako bezpečný koncový bod MRO.
        """
        pass

    def __repr__(self) -> str:
        """Univerzální náhled, který nezatěžuje továrnu."""
        return f"<{self.__class__.__name__}(value={repr(self._value)})>"
