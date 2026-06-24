# Outers
from ......protocols import SimpleMetadataType
# Inners
from ....._core_logic.base_utils.properties import create_properties_for_inner


def _collect_nested_inner_properties(
    meta: SimpleMetadataType,
    path: tuple[str, ...],
    result: dict
) -> None:
    """
    Rekurzivně projde všechny vnitřní (nested) inners
    a přidá jejich property do slovníku `result`.
    """

    # 1. Průchod skrze inners
    for inner in meta.inners:

        # 1.1 Definice proměných
        inner_meta = inner.meta
        new_path = path + (inner_meta.name_private,)

        # 1.2 Vytvoření porperty (pro konstantu i kompozici)
        props = create_properties_for_inner(inner_meta, new_path)
        result.update(props)

        # 1.3 Rekurzivní zpracování pro kompozice
        if not inner_meta.is_constant:
            _collect_nested_inner_properties(inner_meta, new_path, result)

