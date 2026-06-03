def collect_init_parameters(meta: "SimpleObjectMetadata") -> list[inspect.Parameter]:
    """
    Vytvoří seznam parametrů pro __init__ na základě konstant.
    Bere meta.atom_param od každé konstanty v constants_map.
    """
    params = [inspect.Parameter("self", inspect.Parameter.POSITIONAL_OR_KEYWORD)]

    for const_meta in meta.constants_map.values():
        # Využijeme už hotovou signaturu atomu, kterou máme v metadatech konstanty
        params.append(const_meta.atom_param)

    return params