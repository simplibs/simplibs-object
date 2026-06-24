class ImmutableEqualityMixin(SimpleMixin):
    """
    Hodnotový hash a rovnost — použij pouze spolu s PermissionMixin po zavolání lock().
    Hash je stabilní pouze pokud je instance zamčená.

    Měl by kontrolovat zda je společně s Permixion Mixinem - jinak je to chyba (patří k sobě)
    """

    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        if hasattr(other, "meta") and hasattr(other, "value"):
            if self.meta.blueprint_path == other.meta.blueprint_path:
                return self.value == other.value
            return False
        return self.value == other

    def __hash__(self) -> int:
        if not getattr(self, "_locked", False):
            raise TypeError(
                f"{self.meta.class_name} není zamčený — "
                f"hash podle hodnoty by byl nestabilní. Zavolej nejprve lock()."
            )
        return hash(self.value)