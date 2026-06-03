from inspect import Signature, Parameter
# Outers
from ...._types import SimpleMetaType, SimpleClassProtocol



def make_composite_class(
    owner_class: SimpleClassProtocol
) -> type:
    """
    Externí továrna na COMPOSITION_INSTANCE třídy.
    Vytváří třídu, která rekurzivně dědí ze všech instancí vnořených prvků (inners).
    """
    meta: SimpleMetaType = owner_class.meta

    # 1. Příprava dat
    inners: tuple[SimpleClassProtocol, ...] = meta.inners
    inner_classes: tuple[type, ...] = tuple(inner.meta.composite_class for inner in inners)
    inner_names: list[str] = [inner.__name__ for inner in inners]
    atom_instance_class: type = meta.atom_class
    init_signature: Signature = Signature(meta.composite_params)

    # 2. Pokud nemá inners, chová se jako ATOM (vrací základní instanci)
    if not inners:
        return atom_instance_class

    # 3. Definice inicializačního procesu
    # noinspection PyArgumentList
    def __init__(self, **kwargs):
        # 3.1 Předání kwargs dále dle MRO
        # super() zde projde celý řetězec dědičnosti (owner_class.ATOM_INSTANCE + all inner_classes)
        # Každý článek řetězce si z kwargs vytáhne to své a zbytek pošle dál.
        super(type(self), self).__init__(**kwargs)

    # 3.2 Podpis pro IDE a našeptávače
    __init__.__signature__ = init_signature

    # 4. Definice jména třídy (obsahuje jména inners pro lepší debug)
    class_name = f"{owner_class.__name__}Composition({ '_'.join(inner_names) })"

    # 5. Definice předků
    # První je vždy vlastní ATOM_INSTANCE dané třídy, pak následují třídy inners
    class_parents = (atom_instance_class,) + inner_classes

    # 6. Vytvoření slovníku třídy
    class_dict = {
        '__doc__': f"Kompozitní instance {owner_class.__name__} složená z: {', '.join(inner_names)}",
        '__slots__': (),  # Kompozice sama o sobě nepřidává data, jen sdružuje předky
        '__init__': __init__,
    }

    # 7. Vytvoření objektu třídy
    composition_class = type(class_name, class_parents, class_dict)

    # 7.1 Přiřazení signatury samotné třídě (pro maximální kompatibilitu s IDE)
    composition_class.__signature__ = init_signature

    # 8. Navrácení vytvořené třídy
    return composition_class