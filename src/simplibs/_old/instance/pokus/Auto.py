class Auto(SimpleConstant):
    _type = str
    _default = "Škoda"
    _mutable = True  # Příznak, který ovlivňuje Core

    # Metadata vygenerují:
    # name_snake = "auto"
    # name_private = "_auto_core"