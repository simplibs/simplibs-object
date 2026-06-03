def validate_mixins(mixins):
    # 2. Striktní validace argumentu 'mixins'
    # Pokud uživatel zapomněl na tuple a poslal rovnou jednu třídu, nebo poslal ne-tuple:
    if not isinstance(mixins, tuple):
        raise TypeError(
            f"Argument 'mixins' při volání {cls.__name__}() musí být striktně typu 'tuple'. "
            f"Obdržen typ: '{type(mixins).__name__}'."
        )

    # 3. Kontrola, zda jsou v tuple opravdu jen validní třídy (mixiny)
    for mixin in mixins:
        if not isinstance(mixin, type):
            raise TypeError(
                f"Všechny prvky v předaném 'mixins' musí být třídy (type). "
                f"Obdržen prvek: {mixin!r} (typ: '{type(mixin).__name__}')."
            )

    # Možná ještě i validaovat dne nějakého příznaku či atributu v mixinu
    # A možná i validovat metodu init_mixins() zda obsahuje super() a propaguje se dále.