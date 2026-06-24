def make_value_getter_only_on_class(cls: type) -> None:
    """
    Najde na třídě `cls` atribut `value`, pokud je to property se setterem,
    vytvoří novou property jen s getterem a přepíše ji na třídě.
    """
    prop = getattr(cls, "value", None)

    if not isinstance(prop, property):
        return

    if prop.fset is None:
        # Už je getter-only, není co dělat
        return

    new_prop = property(
        fget=prop.fget,
        fset=None,
        fdel=prop.fdel,
        doc=prop.__doc__,
    )
    setattr(cls, "value", new_prop)
