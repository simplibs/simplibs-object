from typing import TYPE_CHECKING
# Inners
from ._class_name_splitter import _class_name_splitter
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def create_names(
    owner_class: "SimpleClassLike"
) -> tuple[tuple[str, ...], str, str]:
    """
    Processing pipeline for generating deterministic class names.

    This function transforms a class name into various textual representations used
    across the system (from user-facing descriptions to private attributes).
    It delegates class name validation to `_class_name_splitter`.
    """
    class_name = owner_class.__name__

    # 1. Decompose the name into individual words (also performs class name validation)
    # The pipeline begins by breaking the name down into semantic units (a tuple of words).
    name_tuple = _class_name_splitter(class_name)

    # 2. Create a snake_case version for parameters (e.g., in __init__)
    # Standard Python convention for variables and arguments.
    name_snake = "_".join(name_tuple).lower()

    # 3. Create a private version for internal slots and attributes
    # The technical name used to ensure the object's internal integrity.
    name_private = "_" + name_snake

    # 4. Return the tuple containing the generated names
    return (
        name_tuple,
        name_snake,
        name_private
    )


_DESIGN_NOTES = """
# create_names

## Purpose
This function operates as a **processing pipeline** that establishes the identity of a `SimpleObject` across different operational contexts. Its objective is to guarantee absolute determinism — every representation of a name within the system (from a constructor parameter to an exception message token) is directly and predictably derived from the original class name.

## Architectural Concept (Pipeline)
The function is intentionally structured as a linear sequence of transformations:
- **Delegation of Validation**: The pipeline does not evaluate whether the class name is well-formed. It delegates this responsibility entirely to `_class_name_splitter`. If the splitter successfully returns a tuple of words, the pipeline is guaranteed to operate on clean, valid data.
- **Separation of Concerns**: `create_names` focuses exclusively on formatting and assigning semantic meaning to the respective name variants.

## Significance of Generated Names

| Name | Format | Primary Use Case |
|---|---|---|
| `name_tuple` | `tuple[str, ...]` | Tokenized semantic units; raw material for dynamic name transformations. |
| `name_snake` | `snake_case` | Names of parameters in `__init__`, local variables, and JSON keys. |
| `name_private` | `_snake_case` | Identifier for internal `__slots__` and private class attributes. |

## The Power of SimpleObject Determinism
The primary advantage of this pipeline architecture is that the developer never needs to manually declare attribute names or string tags. By forcing strict class name rules at the decomposition boundary, the system automatically guarantees:
1. **Consistency**: An API parameter will always match the internal variable representation in the codebase.
2. **Error Elimination**: Typos caused by manual string copying and rewriting are completely eliminated.
3. **Predictability**: By looking at the class name blueprint, you can instantly determine how its private registry is named and how it behaves interfaces-wise.

## Technical Details
- **Safe Joining**: The pipeline relies on the guarantee that the upstream splitter has already removed all syntactic noise (such as underscores or localized diacritics), ensuring that the `join` operation remains safe, stable, and deterministic.
"""