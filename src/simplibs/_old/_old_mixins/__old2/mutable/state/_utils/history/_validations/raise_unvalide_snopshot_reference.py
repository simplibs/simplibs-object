def raise_unvalide_snopshot_reference():
    raise TypeError(f"Expected int or datetime, got {type(ref)!r}")

