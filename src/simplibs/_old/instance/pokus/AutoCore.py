# class_name: AutoCore
# class_parents: (Auto,)
class AutoCore(Auto):
    __slots__ = ("_value",)

    def __init__(self, new_value: Any = None):
        # self.normalize je dostupné díky dědičnosti z Auto
        self._value = self.normalize(new_value, process_none=True)

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        # Tady se uplatňuje ten cls._mutable z definice Auto
        if not Auto._mutable:
            raise SimpleObjectLogicError(...)

        self._value = self.normalize(new_value, process_none=True)