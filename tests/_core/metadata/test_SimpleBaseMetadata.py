from typing import Set, Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .init_processors.names import create_names
from .init_processors.blueprint_path import calculate_blueprint_path
from .validations import raise_metadata_is_immutable
# Annotations
if TYPE_CHECKING:
    from ..protocols.metadata import SimpleBaseMetadataProtocol
    from ..protocols.classes import SimpleClassLike


class SimpleBaseMetadata:
    """Base metadata orchestrator for Simple classes."""

    __slots__ = (
        # 1. Owner class
        "owner_class",

        # 2. Name identity
        "class_name",       # "MyData"
        "name_tuple",       # ("My", "Data")
        "name_snake",       # "my_data"
        "name_private",     # "_my_data"

        # 3. Namespace registry
        "node_names_set",

        # 4. Blueprint path
        "blueprint_path",
    )

    def __init__(
        self: "SimpleBaseMetadataProtocol",
        owner_class: "SimpleClassLike"
    ) -> None:
        """Initializes core metadata fields."""

        # 1. Owner reference
        self.owner_class = owner_class

        # 2. Name identity
        self.class_name = owner_class.__name__
        (
            self.name_tuple,
            self.name_snake,
            self.name_private,
        ) = create_names(owner_class)

        # 3. Namespace registry
        self.node_names_set: Set[str] = {self.name_snake}

        # 4. Blueprint path
        self.blueprint_path = calculate_blueprint_path(owner_class)

        # 5. Subclass hook
        self._process_user_data()

    def _process_user_data(
        self: "SimpleBaseMetadataProtocol"
    ) -> None:
        """Subclass-specific initialization hook."""
        pass

    def __setattr__(
        self: "SimpleBaseMetadataProtocol",
        attr_name: str,
        new_value: Any
    ) -> None:
        """Allows assignment only if the field is UNSET."""

        current_value = getattr(self, attr_name, UNSET)

        if current_value is not UNSET:
            raise_metadata_is_immutable(
                attr_name,
                current_value,
                new_value,
                self.owner_class,
            )

        super().__setattr__(attr_name, new_value)



_DESIGN_NOTES = """
# SimpleBaseMetadata

## Purpose
Provides the foundational metadata structure for all Simple classes.  
It extracts naming identity, initializes namespace tracking, and enforces
immutability of metadata fields.

## Initialization pipeline
The constructor performs five deterministic steps:

1. **Owner reference**  
   Stores the class for which metadata is being generated.

2. **Name identity**  
   Uses `create_names` to derive:
   - `name_tuple`
   - `name_snake`
   - `name_private`

3. **Namespace registry**  
   Initializes `node_names_set` with the class’s own snake name.  
   Subclasses extend this set when processing inner fields.

4. **Blueprint path**  
   Uses `calculate_blueprint_path` to generate a readable inheritance path.

5. **Subclass hook**  
   Calls `_process_user_data()` for specialized metadata types.

## Write-once rule
Metadata fields are immutable after initialization.

- Fields start with `UNSET`.
- `__setattr__` allows assignment only when the current value is `UNSET`.
- Any overwrite attempt triggers `raise_metadata_is_immutable`.

This guarantees stable, deterministic metadata for the lifetime of the class.

## Subclass architecture
Subclasses **must not** override `__init__`.  
All custom initialization belongs inside `_process_user_data()`.

This ensures:
- consistent naming identity,
- consistent namespace initialization,
- consistent blueprint path generation,
- predictable metadata structure.

## Notes
- The class is lightweight and performs only structural tasks.
- All heavy logic is delegated to specialized processors.
- Metadata objects are created once per class and never mutated.
"""