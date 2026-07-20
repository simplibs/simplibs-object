from typing import Set, Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .init_processors.names import create_names
from .init_processors.path import calculate_blueprint_path
from .validations import raise_metadata_is_immutable
# Annotations
if TYPE_CHECKING:
    from ...protocols.metadata import SimpleBaseMetadataProtocol
    from ...protocols.classes import SimpleClassLike


class SimpleBaseMetadata:
    """
    Core metadata orchestrator for the Simple system.
    Handles class name token extraction and object namespace management.
    """

    #--- __slots__ definition for optimized runtime performance ---#
    # (Every subclass must define slots explicitly to maintain this optimization)
    __slots__ = (
        # 1. Reference to the owner class blueprint
        "owner_class",

        # 2. String identity markers (derived from the class name)
        "class_name",       # e.g., "MyData"
        "name_tuple",       # e.g., ("My", "Data")
        "name_snake",       # e.g., "my_data"
        "name_private",     # e.g., "_my_data"

        # 3. Namespace lifecycle management
        "node_names_set",       # Set of occupied names to detect naming collisions

        # 4. Precalculated path helper utilized by __repr__
        "blueprint_path"
    )

    #--- __init__ definition for initializing slot properties ---#
    # (Subclasses do not define their own __init__; they inherit this orchestrator flow)
    def __init__(
        self: "SimpleBaseMetadataProtocol",
        owner_class: "SimpleClassLike"
    ) -> None:
        """
        Initializes core blueprint metadata attributes.
        """
        # 1. Assign owner class reference
        self.owner_class = owner_class

        # 2. Derive string identity tokens
        self.class_name = owner_class.__name__
        (self.name_tuple,
         self.name_snake,
         self.name_private) = create_names(owner_class)

        # 3. Register the snake_case name to initialize the collision detection set
        self.node_names_set: Set[str] = {self.name_snake}

        # 4. Precalculate the blueprint path representation
        self.blueprint_path = calculate_blueprint_path(owner_class)

        # 5. Execute downstream hooks for subclass-specific metadata processing
        self._process_user_data()

    #--- Subclass initialization hook ---#
    # (Invoked at the end of base initialization to be overridden by subclasses)
    def _process_user_data(
        self: "SimpleBaseMetadataProtocol"
    ) -> None:
        """
        Hook method for type-specific metadata processing execution.

        Default implementation: No operation.
        Designed to be overridden by specialized metadata subclasses.
        """
        pass

    #--- Custom attribute assignment interceptor ---#
    # (Enforces the immutability of initialized metadata attributes)
    def __setattr__(
        self: "SimpleBaseMetadataProtocol",
        attr_name: str,
        new_value: Any
    ) -> None:
        """Permits assignment only if the target slot holds UNSET."""

        # 1. Fetch the current state of the attribute
        current_value = getattr(self, attr_name, UNSET)

        # 2. Raise an error if attempting to overwrite an already assigned slot
        if current_value is not UNSET:
            raise_metadata_is_immutable(attr_name, current_value, new_value, self.owner_class)

        # 3. Commit the write operations if valid
        super().__setattr__(attr_name, new_value)


_DESIGN_NOTES = """
# SimpleBaseMetadata

## Purpose
Acts as the abstract structural foundation and orchestrator for all metadata processing pipelines within the Simple ecosystem. It intercepts class creation, extracts naming identity tokens, initializes namespace registries, and guarantees absolute immutability of structural metadata once compiled.

## The Write-Once Paradigm (`__setattr__`)
To secure system stability, metadata attributes strictly follow a **Write-Once** lifecycle pattern:
- Slots are initialized either dynamically or set to `UNSET` by default.
- `__setattr__` intercepts every assignment request. If an attribute contains a value other than `UNSET`, it is considered locked.
- Any subsequent attempt to re-assign or mutate that attribute triggers `raise_metadata_is_immutable`.
- This ensures that once a class blueprint structural layout is determined at boot time, it cannot be corrupted at runtime.

## Namespace Management & Collision Shielding
The `node_names_set` property serves as the foundational tracking registry for all identifiers associated with a class entity.
- During this base initialization step, the class's own `name_snake` token is registered.
- In downstream subclasses (e.g., composite objects), this set expands as inner attributes are processed.
- This structural layout allows the framework to execute ultra-fast lookup checks to detect and prevent naming collisions between structural properties, methods, and system-generated tokens.

## Inherited Initialization Architecture
Subclasses of `SimpleBaseMetadata` **must not** implement their own `__init__` methods. 
- The entire structural pipeline is centrally controlled by `SimpleBaseMetadata.__init__`.
- Custom initialization logic for specialized metadata flavors (Constants vs. Composite Objects) must be isolated inside the `_process_user_data()` hook.
- This guarantees that core identity fields (`name_snake`, `blueprint_path`, etc.) are always consistently populated before any subclass-specific evaluations take place.
"""