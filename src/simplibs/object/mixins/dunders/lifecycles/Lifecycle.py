import copy as _copy

class LifecycleMixin(SimpleMixin):
    """
    Životní cyklus SimpleObject instance:
    - mělká a hluboká kopie
    - pickle podpora (__getstate__, __setstate__, __reduce__)
    - generika (__class_getitem__)
    """

    __slots__ = ()

    # ---------------------------------------------------------
    # 1) Mělká kopie
    # ---------------------------------------------------------
    def __copy__(self):
        new = self.__class__()      # vytvoří instanci přes create_instance
        new.value = self.value      # aktivuje validaci + reaktivitu
        return new

    # ---------------------------------------------------------
    # 2) Hluboká kopie
    # ---------------------------------------------------------
    def __deepcopy__(self, memo: dict) -> Any:
        new = self.__class__()
        new.value = _copy.deepcopy(self.value, memo)
        return new

    # ---------------------------------------------------------
    # 3) Pickle: získání stavu
    # ---------------------------------------------------------
    def __getstate__(self):
        """Vrací serializovatelný stav pro pickle."""
        return {"value": self.value}

    # ---------------------------------------------------------
    # 4) Pickle: obnova stavu
    # ---------------------------------------------------------
    def __setstate__(self, state):
        """Obnoví stav z pickle."""
        self.value = state["value"]

    # ---------------------------------------------------------
    # 5) Pickle: reduce protokol
    # ---------------------------------------------------------
    def __reduce__(self):
        """
        Pickle protokol:
        - konstruktor: self.__class__
        - argumenty: (value,)

        Pozor: instance se obnoví bez původních mixinů,
        protože dynamicky sestavené třídy pickle plně nepodporuje.

        """
        return (self.__class__, (), self.__getstate__())

    # ---------------------------------------------------------
    # 6) Generika: MyClass[int]
    # ---------------------------------------------------------
    @classmethod
    def __class_getitem__(cls, item):
        """
        Umožňuje zápis MyClass[int] pro type hints.
        """
        try:
            return super().__class_getitem__(item)
        except Exception:
            return cls
