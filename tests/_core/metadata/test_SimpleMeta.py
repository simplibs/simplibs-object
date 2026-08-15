from typing import Any, Dict, Tuple, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .SimpleConstantMetadata import SimpleConstantMetadata
from .SimpleObjectMetadata import SimpleObjectMetadata
from .constants import BASE_CLASS_NAMES
from .validations import raise_attribut_allready_set
from .instance_builders.instance import create_instance
# Annotations
if TYPE_CHECKING:
    from ..protocols.classes import SimpleClassLike
    from ..protocols.instance import SimpleInstanceLike
    from ..protocols.metadata import SimpleMetadataLike, SimpleMetaProtocol


class SimpleMeta(type):
    """Metaclass orchestrating metadata creation, write-once protection, and instance construction."""

    # ----------------------------------------------------------------------
    # 1) Class creation (__new__)
    # ----------------------------------------------------------------------
    def __new__(
        mcls,
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any],
    ) -> "SimpleClassLike":
        """Creates the class and attaches metadata for declarative Simple classes."""

        cls = super().__new__(mcls, name, bases, namespace)
        cls: "SimpleClassLike"

        # Skip metadata creation for system base classes and instance classes
        if hasattr(cls, "_is_instance_class") or name in BASE_CLASS_NAMES:
            return cls

        # Compute metadata (constant vs object)
        calculated_metadata = (
            SimpleObjectMetadata(owner_class=cls)
            if hasattr(cls, "_inners")
            else SimpleConstantMetadata(owner_class=cls)
        )
        calculated_metadata: SimpleMetadataLike
        cls.__metadata__ = calculated_metadata

        return cls

    # ----------------------------------------------------------------------
    # 2) Write-once attribute protection (__setattr__)
    # ----------------------------------------------------------------------
    def __setattr__(
        cls: "SimpleMetaProtocol",
        attr_name: str,
        new_value: Any,
    ) -> None:
        """Prevents overwriting already-initialized class-level attributes."""

        if getattr(cls, attr_name, UNSET) is not UNSET:
            raise_attribut_allready_set(cls, attr_name, new_value)

        super().__setattr__(attr_name, new_value)

    # ----------------------------------------------------------------------
    # 3) Instance creation (__call__)
    # ----------------------------------------------------------------------
    def __call__(
        cls: "SimpleMetaProtocol",
        *,
        mixins: tuple = (),
        as_atom: bool = False,
        mutable: bool = True,
    ) -> "SimpleInstanceLike":
        """Creates a new instance using the full instance-builder pipeline."""
        # noinspection PyTypeChecker
        return create_instance(
            cls,
            mixins,
            as_atom=as_atom,
            mutable=mutable,
        )

    # ----------------------------------------------------------------------
    # 4) Technical representation (__repr__)
    # ----------------------------------------------------------------------
    def __repr__(cls: "SimpleMetaProtocol") -> str:
        """Technical representation of the blueprint class."""
        return (
            f"<class {cls.__name__} (System Base)>"
            if cls.meta is UNSET else
            f"<{cls.meta.class_name}Blueprint blueprint='{cls.meta.blueprint_path}' "
            f"type={'Constant' if cls.meta.is_constant else 'Object'}>"
        )

    # ----------------------------------------------------------------------
    # 5) User-facing representation (__str__)
    # ----------------------------------------------------------------------
    def __str__(cls: "SimpleMetaProtocol") -> str:
        """User-facing name of the blueprint class."""
        return cls.__name__

    # ----------------------------------------------------------------------
    # 6) Metadata accessor
    # ----------------------------------------------------------------------
    @property
    def meta(cls: "SimpleMetaProtocol") -> "SimpleMetadataLike":
        """Public accessor for class metadata."""
        return cls.__metadata__


_DESIGN_NOTES = """
# SimpleMeta — Full Lifecycle Overview

## Purpose
`SimpleMeta` is the central metaclass of the Simple system. It governs the entire
lifecycle of declarative blueprint classes:

1. Class creation and metadata attachment
2. Write-once protection of structural attributes
3. Instance construction via the instance-builder pipeline
4. Technical and user-facing class representation
5. Metadata access

This metaclass ensures that Simple classes behave like stable, immutable
blueprints while still supporting dynamic, high-performance instance creation.

---

## 1. Class Creation (`__new__`)
Executed when a new class is defined.

Responsibilities:
- Create the class object.
- Detect whether the class is:
  - a system base class,
  - an instance class,
  - or a declarative user blueprint.
- Attach the correct metadata:
  - `SimpleConstantMetadata` for constant nodes
  - `SimpleObjectMetadata` for composite nodes

Metadata is computed once and cached on the class as `__metadata__`.

---

## 2. Write-Once Protection (`__setattr__`)
Executed whenever a class-level attribute is assigned.

Responsibilities:
- Prevent overwriting already-initialized attributes.
- Enforce blueprint immutability.
- Route violations through `raise_attribut_allready_set`.

This guarantees that declarative classes remain stable and cannot be mutated
after definition.

---

## 3. Instance Construction (`__call__`)
Executed when the class is *called* like a function.

Responsibilities:
- Delegate to `create_instance`, which performs:
  - validation,
  - structural resolution,
  - base-class selection,
  - mixin compatibility checks,
  - dynamic class compilation,
  - mixin extension hooks,
  - memory allocation,
  - initialization.

This method transforms blueprint classes into fully operational runtime instances.

---

## 4. Technical Representation (`__repr__`)
Provides a structured, machine-oriented representation of the blueprint class.

Used for debugging, logging, and developer tooling.

---

## 5. User-Facing Representation (`__str__`)
Returns the clean business name of the class.

Used in UI, logs, and user-facing messages.

---

## 6. Metadata Accessor (`meta`)
Provides a stable, public interface for retrieving metadata.

Metadata is always stored on the class as `__metadata__`.

---

# Recommended Ordering of Metaclass Dunder Methods

The ordering used in `SimpleMeta` is the recommended and conventional structure:

1. `__new__` — class creation
2. `__setattr__` — class-level attribute control
3. `__call__` — instance creation
4. `__repr__` — technical representation
5. `__str__` — user-facing representation
6. `@property meta` — metadata accessor

This ordering reflects the natural lifecycle of a class:
creation → protection → instantiation → representation → metadata access.

It is also the order used in CPython’s own metaclasses and most frameworks.

"""