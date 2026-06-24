def raise_unvalide_snopshot_timestamp():
    raise KeyError(f"No snapshot found for timestamp {timestamp!r}")
