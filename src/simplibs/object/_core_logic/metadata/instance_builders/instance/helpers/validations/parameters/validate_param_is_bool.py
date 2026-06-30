from ......exceptions import SimpleObjectInstanceError


def validate_param_is_bool(
    as_atom: bool
) -> None:
    """
    Validuje, že parametr as_atom je typu bool.
    """

    # Podmínka, která vede k vyvolání výjimky:
    # if not isinstance(as_atom, bool):

    if not isinstance(as_atom, bool):

        raise SimpleObjectInstanceError(
            error_name="INVALID PARAMETER",
            value_label="Parameter 'as_atom' must be bool",
            expected="Hodnota typu bool (True nebo False).",
            value=as_atom,
            problem=(
                f"Hodnota parametru 'as_atom' není typu bool. "
                f"Obdrženo: {as_atom!r} ({type(as_atom).__name__})."
            ),
            context="create_instance(..., as_atom=...)",
            how_to_fix=(
                "Upravte hodnotu parametru 'as_atom' na True nebo False.",
                "Příklad:",
                "    create_instance(MyClass, mixins=(), as_atom=True)"
            ),
            exception=TypeError
        )
