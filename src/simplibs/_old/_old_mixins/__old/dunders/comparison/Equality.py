class EqualityMixin(SimpleMixin):
    """
    Rovnost a hashování pro Simple instance.
    Obojí je založeno na identitě — instance jsou mutovatelné.

    Pokud potřebuješ hodnotovou rovnost s hashováním,
    použij ImmutableEqualityMixin (vyžaduje immutable _type).
    """

    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        # 1) Jiná Simple instance ze stejné definiční třídy → porovnej hodnoty
        if hasattr(other, "meta") and hasattr(other, "value"):
            if self.meta.blueprint_path == other.meta.blueprint_path:
                return self.value == other.value
            return False

        # 2) Surová hodnota → porovnej přímo
        return self.value == other

    def __hash__(self) -> int:
        """
        Hash podle identity — konzistentní s mutovatelností.
        Garantuje stabilitu v dict/set i při změně hodnoty.
        """
        return id(self)