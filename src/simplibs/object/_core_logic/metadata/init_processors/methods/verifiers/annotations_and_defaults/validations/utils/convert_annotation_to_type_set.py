from typing import get_args, Union, get_origin
from types import UnionType


def convert_annotation_to_type_set(
    annotation: type | UnionType
) -> set[type] | set[str]:

    # 1. Pokud hodnota je typ
    if isinstance(annotation, type):
        return {annotation}

    # 2. Pokud hodnota je UnionType
    if isinstance(annotation, UnionType) or get_origin(annotation) is Union:
        return set(get_args(annotation))

    # 3. Fallback pro případné další hodnoty
    return {f"nevalidní typ: repr(annotation)"}
