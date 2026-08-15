from typing import Any, TYPE_CHECKING
# Inners
from ._validations import (
    raise_inners_is_not_tuple,
    raise_inner_is_not_simple_constant_subclass,
)
# Outers
from ....SimpleConstant import SimpleConstant
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassType


def load_parameters_from_inners(
    class_name: str,
    inners: tuple["SimpleClassType", ...]
) -> dict[str, Any]:
    """Extracts logic parameter defaults from a tuple of inner component blueprint classes.

    Iterates through child ``inners`` classes, validating their type hierarchy, and collects a mapping
    of parameter snake_case names to their declared default values.

    Args:
        class_name: Target composite class name used for diagnostic error context.
        inners: Tuple of inner child component blueprint classes.

    Returns:
        A dictionary mapping snake_case child attribute names to their default values.

    Raises:
        SimpleLogicError: If inners is not a tuple or contains invalid class types.
    """

    # 1. Container Type Boundary Validation
    if not isinstance(inners, tuple):
        raise_inners_is_not_tuple(class_name, inners)

    # 2. Extract Attribute Names & Defaults from Inners
    params: dict[str, Any] = {}

    for inner in inners:

        # 2.1 Validation of descendant ancestors
        # noinspection PyTypeChecker
        if not issubclass(inner, SimpleConstant):
            raise_inner_is_not_simple_constant_subclass(class_name, inner)

        # 2.2 Adding a default value
        # noinspection PyUnresolvedReferences
        params[inner_class.meta.name_snake] = inner_class.meta.default

    # 3. Return Mapped Parameters Dictionary
    return params


_DESIGN_NOTES = """
# load_parameters_from_inners (Helper Engine)

## Purpose
Parses the `inners` tuple of a composite object blueprint to construct a mapping 
of parameter names (`name_snake`) and default values (`default`). This dictionary feeds 
logic signature verification and default value calculation.

## Execution Workflow
1. Validates that `inners` is a tuple via `validate_inners_is_tuple`.
2. Iterates over child entries, verifying that each item is a `SimpleConstant` subclass via `validate_inner_is_simple_constant_subclass`.
3. Extracts `inner.meta.name_snake` as dictionary key and `inner.meta.default` as value.
4. Returns the mapped parameters.

## Framework Usage
- Invoked inside `create_object_class` during dynamic composite blueprint generation.
"""