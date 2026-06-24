from .build_nodes_tuple import build_nodes_tuple


class SerializationMixin(SimpleMixin):
    """
    Poskytuje serializaci instance do dict/JSON a obnovu z nich.
    Základ pro HistoryMixin.
    """

    __slots__ = ("_nodes_tuple", "_structure_dict")

    def init_mixins(self):
        super().init_mixins()
        self._nodes_tuple = _build_nodes_tuple(self)
        self._structure_dict = _build_structure_dict(self._nodes_tuple)

    # -------------------------
    # Serializace
    # -------------------------
    def to_dict(self) -> dict:
        """Serializuje instanci do čitelného dict."""
        return _to_dict(self._nodes_tuple)

    def to_json(self, **kwargs) -> str:
        """Serializuje instanci do JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)

    # -------------------------
    # Obnova
    # -------------------------
    @classmethod
    def from_dict(cls, data: dict, *, validate: bool = True):
        """
        Vytvoří instanci z dict.
        validate=True  → pomalá cesta, data mohou mít libovolný původ.
        validate=False → rychlá cesta, předpokládá data z to_dict().
        """
        instance = cls()
        if validate:
            _from_dict_slow(instance, data)
        else:
            _from_dict_fast(instance, data)
        return instance

    @classmethod
    def from_json(cls, json_str: str, *, validate: bool = True):
        """Vytvoří instanci z JSON."""
        return cls.from_dict(json.loads(json_str), validate=validate)