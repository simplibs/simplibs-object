# Outers
from ......_types import SimpleMetaType
# Inners
from .template_builders.build_init_signature_string import build_init_signature_string
from .template_builders.build_constants_init_lines import build_constants_init_lines
from .template_builders.build_composites_init_lines import build_composites_init_lines
from .template_builders.build_final_calculation_lines import build_final_calculation_lines


def create_composite_init_template(
    meta: SimpleMetaType
) -> str:
    """
    Vygeneruje a zkompiluje nativní metodu __init__ pro kompozici.
    Využívá pomocné generátory pro sestavení těla a signatury.
    """

    # 1. Vytvoření řetězce pro parametry
    sig_str = build_init_signature_string(meta)

    # 2. Vytvoření řetězce pro logiku
    init_lines = [
        f"def __init__({sig_str}):",
        *build_constants_init_lines(meta),
        *build_composites_init_lines(meta),
        *build_final_calculation_lines(meta)
    ]

    # 3. Navrácení spojeného textu
    return "\n    ".join(init_lines)



