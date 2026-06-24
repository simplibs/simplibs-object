class CompositeCollectionMixin(SimpleMixin):
    """
    Kolekční chování pro kompozitní SimpleObject instance.
    Umožňuje přístup jako k dictu, iteraci, len(), reversed(), atd.
    """

    __slots__ = ()
    _composite_only = True

    # -------------------------
    # len(obj)
    # -------------------------
    def __len__(self) -> int:
        return len(self.meta.inners)

    # -------------------------
    # key in obj
    # -------------------------
    def __contains__(self, key: Any) -> bool:
        """Vrací True pokud key odpovídá jménu některého vnitřního prvku."""
        return any(inner.meta.name_snake == key for inner in self.meta.inners)

    # -------------------------
    # iter(obj)
    # -------------------------
    def __iter__(self):
        return iter(inner.meta.name_snake for inner in self.meta.inners)

    # -------------------------
    # reversed(obj)
    # -------------------------
    def __reversed__(self):
        return reversed([inner.meta.name_snake for inner in self.meta.inners])

    # -------------------------
    # obj[key]
    # -------------------------
    def __getitem__(self, key: str) -> Any:
        for inner in self.meta.inners:
            if inner.meta.name_snake == key:
                return getattr(self, key)
        return self.__missing__(key)  # místo přímého raise KeyError

    def __missing__(self, key: str) -> Any:
        raise KeyError(
            f"Prvek '{key}' není definován v {self.meta.class_name}. "
            f"Dostupné prvky: {self.keys()}"
        )

    # -------------------------
    # obj[key] = value
    # -------------------------
    def __setitem__(self, key: str, value: Any) -> None:
        for inner in self.meta.inners:
            if inner.meta.name_snake == key:
                setattr(self, key, value)
                return
        raise KeyError(
            f"Prvek '{key}' není definován v {self.meta.class_name}."
        )

    # -------------------------
    # obj.keys()
    # -------------------------
    def keys(self) -> list[str]:
        return [inner.meta.name_snake for inner in self.meta.inners]


    # -------------------------
    # obj.values()
    # -------------------------
    def values(self) -> list[Any]:
        return [getattr(self, key) for key in self.keys()]

    # -------------------------
    # obj.items()
    # -------------------------
    def items(self) -> list[tuple[str, Any]]:
        return [(key, getattr(self, key)) for key in self.keys()]

    # -------------------------
    # dir(obj)
    # -------------------------
    def __dir__(self) -> list[str]:
        base = list(object.__dir__(self))
        base += [inner.meta.name_snake for inner in self.meta.inners]
        return sorted(set(base))
