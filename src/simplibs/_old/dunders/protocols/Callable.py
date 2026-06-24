class CallableMixin(SimpleMixin):
    """
    Umožňuje volat instanci jako funkci.
    obj()            → vrátí aktuální hodnotu
    obj(**kwargs)    → spočítá hodnotu přes _logic a vrátí ji
    """

    __slots__ = ()

    def __call__(self, **kwargs: Any) -> Any:
        if not kwargs:
            return self.value
        return self.__class__.calculate_value(**kwargs)

    def call_as_instance(self, **kwargs: Any) -> Any:
        """Vrátí novou instanci s vypočítanou hodnotou."""
        new = self.__class__()
        new.value = self.__class__.calculate_value(**kwargs)
        return new