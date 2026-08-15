from typing import TYPE_CHECKING
# Inners
from ._class_name_splitter import _class_name_splitter
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleClassLike


def create_names(
    owner_class: "SimpleClassLike"
) -> tuple[tuple[str, ...], str, str]:
    """Generates deterministic name variants derived from the class name."""

    # 1. Extract raw class name
    class_name = owner_class.__name__

    # 2. Split into semantic words (includes validation)
    name_tuple = _class_name_splitter(class_name)

    # 3. Create snake_case variant
    name_snake = "_".join(name_tuple).lower()

    # 4. Create private variant
    name_private = "_" + name_snake

    # 5. Return all name forms
    return (
        name_tuple,
        name_snake,
        name_private,
    )



_DESIGN_NOTES = """
# create_names

## Purpose
Generates all name variants used throughout the metadata system.  
Every variant is derived deterministically from the class name, ensuring
predictable and consistent naming across the entire SimpleObject ecosystem.

## Pipeline
The function performs three simple steps:

1. **Split the class name**  
   Delegates to `_class_name_splitter`, which validates the name and returns
   a tuple of semantic words.

2. **Create snake_case**  
   Joins the words using underscores and converts them to lowercase.

3. **Create private name**  
   Prefixes the snake_case name with `_` for internal metadata and slot usage.

## Output
| Name          | Format        | Purpose                                      |
|---------------|---------------|----------------------------------------------|
| `name_tuple`  | `("my", "class")` | Raw semantic units for further processing |
| `name_snake`  | `"my_class"`  | Parameter names, JSON keys, internal fields |
| `name_private`| `"_my_class"` | Private slots and internal attributes        |

## Determinism
All name variants are derived from a single source: the class name.  
This guarantees:

- **Consistency** — internal and external names always match  
- **Safety** — no manual string manipulation  
- **Predictability** — developers can infer all generated names from the class name alone

## Notes
- `_class_name_splitter` ensures the name is valid, ASCII-only, and PascalCase.
- Because validation happens upstream, joining and formatting are always safe.
"""