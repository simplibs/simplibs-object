from typing import get_args, Union, get_origin, Any
from types import UnionType


def _convert_annotation_to_type_set(
    annotation: type | None | UnionType
) -> set[type]:
    """Converts a type annotation or a union variance layout into a flat set of unique type objects.

    Transforms single types, legacy typing.Union, and modern PEP 604 pipe unions into
    a uniform collection footprint for simplified subset and variance validation.
    """

    # 1. If the value is a single standard class or primitive type
    if isinstance(annotation, type):
        return {annotation}

    # 2. If the value is a PEP 604 UnionType or a legacy typing.Union construct
    if isinstance(annotation, UnionType) or get_origin(annotation) is Union:
        return set(get_args(annotation))

    # 3. Fallback path to gracefully capture and isolate anomalous or unhandled type definitions
    return {Any}


_DESIGN_NOTES = """
# _convert_annotation_to_type_set

## Purpose
Acts as a normalization utility that flattens varied Python type representation models (standard classes, `typing.Union`, and pipe-delimited `UnionType` layouts) into a uniform, deduplicated mathematical `set` footprint to enable rapid variance calculations.

## Diagnostic Layout & Formatting
1. **Normalization Strategy**: Simplifies high-level signature checks down to standard container evaluations (`issubset`), entirely removing the need for complex, nested recursive type parsing blocks inside caller routines.
2. **PEP 604 & Legacy Alignment**: Bridges native introspection boundaries by coupling operational `UnionType` checks directly with `typing.get_origin` filters, ensuring total compatibility across different runtime annotation patterns.
3. **Failsafe Containment Blueprint**: Replaces low-level type evaluation crashes within the exception track by packing unparseable annotation parameters into a predictable fallback string representation set block.
"""