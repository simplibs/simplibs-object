from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance.core_classes import InstanceBaseProtocol


class InstanceBase:
    """The common denominator and identity guarantor for all instantiated framework components.

    Serves as the foundational substrate for memory management via explicit slots,
    handles dynamic mixin hook lifecycles, and provides unified introspection overrides.
    """

    # 1. Configure slots and include weakref support to allow instance caching and tracking
    __slots__ = ("__weakref__",)

    # 2. Define a low-level mixin anchor allowing external extensions to plug into the initialization pipeline
    def init_mixins(
        self: "InstanceBaseProtocol"
    ) -> None:
        """Default empty anchor for reactive instantiation and execution of custom class mixins."""
        pass

    # 3. Define the core metadata access property bypassing traditional MRO traversal traps
    @property
    def meta(
        self: "InstanceBaseProtocol"
    ) -> "SimpleMetadataLike":
        """Public access interface exposing class metadata descriptor payloads.

        Metadata maps are attached efficiently directly at class scope levels to ensure
        maximum resolution speed and read-only protection boundaries.
        """
        return self.__class__.__metadata__

    # 4. Define standard __repr__ output delivering a detailed technical diagnostic snapshot
    def __repr__(
        self: "InstanceBaseProtocol"
    ) -> str:
        """Unified structural string representation blueprint for all custom object instances.

        Intentionally avoids mocking standard variable parameter instantiation syntaxes;
        instead, it provides transparent diagnostics revealing types, sources, states, and memory targets.
        """
        class_name  = self.meta.class_name
        blueprint   = f"blueprint='{self.meta.blueprint_path}'"
        state       = f"value={self._value!r}" if hasattr(self, "_value") else "value=EMPTY"
        hex_id      = f"id={hex(id(self))}"

        return f"<{class_name} {blueprint} {state} {hex_id}>"

    # 5. Define standard __str__ output providing clean, user-facing nomenclature
    def __str__(
        self: "InstanceBaseProtocol"
    ) -> str:
        """Clean human-readable layout representation.

        Example:
            Car
        """
        return self.meta.class_name


_DESIGN_NOTES = """
# InstanceBase

## Purpose
Acts as the global structural anchor and identity runtime root for all generated objects (such as Atomic Constants and Composition blocks) inside the metadata architecture. It guarantees optimal object footprints and layout homogeneity across dynamically generated sub-classes.

## Architectural Design Decisions

### 1. Memory Optimization & Weakref Constraints (`__slots__`)
* By declaring a single element tuple `__slots__ = ("__weakref__",)`, `InstanceBase` explicitly blocks the creation of an underlying mutable internal dynamic dictionary (`__dict__`) for its descendants unless downstream classes choose to break this layout.
* Adding `__weakref__` explicitly allows objects built over this architecture to safely register with low-cost cache listeners, external identity registries, and automated garbage collection tracking systems without sacrificing high-performance raw slot read-write times.

### 2. Micro-Optimization of Metadata Resolution
* The `meta` property bypasses standard complex Method Resolution Order (`MRO`) lookups by directly addressing the static target binding at class scope via `self.__class__.__metadata__`.
* This configuration bounds metadata extraction costs to a constant $O(1)$ lookup time, ensuring that intense runtime validations or validation tracking steps don't incur lookup penalties down deep inheritance paths.

### 3. Dynamic Mixing Lifecycles (`init_mixins`)
* The presence of `init_mixins` sets up a stable, non-breaking structural registration point for extension behaviors. Because dynamically assembled classes (`type(...)`) combine multiple inherited structures, this anchor allows secondary behaviors to execute setup configurations without stepping on the primary `__init__` sequence.

### 4. Deterministic Uniform Introspection (`__repr__` and `__str__`)
* `__repr__` isolates structural state checks (`hasattr(self, "_value")`) ensuring the framework can safely print diagnostic dumps even when checking partially constructed or corrupted memory structures.
* The output layout is strictly formatted to match typical engine diagnostics, making log checking, tracking, and debugging highly legible throughout execution loops.
"""