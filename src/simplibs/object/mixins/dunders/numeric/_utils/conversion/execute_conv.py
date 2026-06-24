def execute_conv(self, func, *args):
    """
    Rychlý modulární exekutor pro nativní konverze hodnoty.
    Provádí transformaci a formátuje unifikovanou chybovou hlášku při selhání.
    """

    # 1. Pokus o výpočet
    try:
        return func(self.value, *args)

    # 2. Vyvolání výjimky při neúspěchu
    except (TypeError, ValueError) as e:
        raise TypeError(
            f"Nelze provést {func.__name__}() na {self.meta.class_name} "
            f"(value={self.value!r}): {e}"
        ) from e
