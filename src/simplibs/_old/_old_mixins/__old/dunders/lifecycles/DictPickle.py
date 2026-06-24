class DictPickleMixin(SimpleMixin):
    """
    Pickle přes to_dict/from_dict — vyžaduje SerializationMixin.
    """
    __slots__ = ()

    def __getstate__(self) -> dict:
        return self.to_dict()

    def __setstate__(self, state: dict) -> None:
        restored = self.__class__.from_dict(state)
        self.value = restored.value