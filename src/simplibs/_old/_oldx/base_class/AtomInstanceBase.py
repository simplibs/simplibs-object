class AtomInstanceBase:
    """Základní třída pro Atomickou instanci."""

    __slots__ = ()  # Důležité! Aby základní třída nepřidávala __dict__

    def _on_update(self) -> None:
        """
        Základní implementace hooku.
        Může zůstat prázdná, slouží jako bezpečný koncový bod MRO.
        """
        pass

    def __repr__(self) -> str:
        """Univerzální náhled, který nezatěžuje továrnu."""
        # Zde můžeme využít introspekci, abychom ukázali jméno a hodnotu
        return f"<{self.__class__.__name__}>"