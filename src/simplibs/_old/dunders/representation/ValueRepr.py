class ValueReprMixin(SimpleMixin):
    """
    Přepíše __repr__ a __str__ tak, aby objekt vystupoval
    jako surová hodnota kterou obaluje.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{self.meta.class_name}({self.value!r})"

    def __str__(self) -> str:
        return str(self.value)