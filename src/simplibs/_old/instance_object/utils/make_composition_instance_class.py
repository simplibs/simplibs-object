from inspect import Signature
from typing import Any

def make_composition_instance_class(base_class: type) -> type:
    """
    Externí továrna na COMPOSITION_INSTANCE třídy.
    Vytváří třídu, která rekurzivně dědí ze všech instancí vnořených prvků (inners).
    """

    # 1. Pokud nemá inners, chová se jako ATOM (vrací základní instanci)
    if not base_class.meta.inners:
        return base_class.ATOM_INSTANCE()

    # 2. Rekurzivní sběr kompozitních tříd všech vnořených prvků
    # Každý inner prvek vrátí buď svou ATOM_INSTANCE nebo svou COMPOSICE_INSTANCE
    inner_classes = tuple(
        inner.COMPOSICE_INSTANCE() for inner in base_class.meta.inners
    )

    # 3. Definice inicializačního procesu
    def __init__(self, **kwargs):
        # super() zde projde celý řetězec dědičnosti (base_class.ATOM_INSTANCE + all inner_classes)
        # Každý článek řetězce si z kwargs vytáhne to své a zbytek pošle dál.
        super(type(self), self).__init__(**kwargs)

    # 4. Sběr všech parametrů pro signaturu (pro IDE)
    # base_class.MIXIN_PARAMS() rekurzivně sesbírá parametry z celého stromu
    init_signature = Signature(base_class.MIXIN_PARAMS())
    __init__.__signature__ = init_signature

    # 5. Definice předků
    # První je vždy vlastní ATOM_INSTANCE dané třídy, pak následují třídy inners
    class_parents = (base_class.ATOM_INSTANCE(),) + inner_classes

    # 6. Název třídy pro introspekci (obsahuje jména inners pro lepší debug)
    inner_names = [inner.__name__ for inner in base_class.meta.inners]
    class_name = f"{base_class.__name__}Composition({ '_'.join(inner_names) })"

    # 7. Vytvoření slovníku třídy
    class_dict = {
        '__doc__': f"Kompozitní instance {base_class.__name__} složená z: {', '.join(inner_names)}",
        '__slots__': (),  # Kompozice sama o sobě nepřidává data, jen sdružuje předky
        '__init__': __init__,
    }

    # 8. Vytvoření třídy a přiřazení signatury
    composition_class = type(class_name, class_parents, class_dict)
    composition_class.__signature__ = init_signature

    return composition_class