from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .SimpleBaseMetadata import SimpleBaseMetadata
from .instance_builders.atom_class import make_atom_class
from .init_processors.methods import process_classmethod
from .init_processors.attributes import (
    process_type, process_default_for_constant
)
# Annotations
if TYPE_CHECKING:
    from ...protocols.metadata import SimpleConstantMetadataProtocol
    from ...protocols.instance.core_classes import AtomInstanceProtocol


# noinspection PyAttributeOutsideInit
class SimpleConstantMetadata(SimpleBaseMetadata):
    """Specialized orchestrator for framework Constant definitions (Atoms).

    Guarantees that every leaf node within the system graph possesses a strictly resolved type,
    a validated default fallback value, and a fully functional validation signature interface.
    """

    #--- Define __slots__ for maximum runtime performance ---#
    # (every descending sub-class must explicitly declare slots to preserve allocation advantages)
    __slots__ = (

        # 1. User-supplied raw schema definition records
        "value_type",       # Normalized data type object (_type)
        "default",          # Materialized baseline value (_default)
        "validate",         # Reference binding to the extracted _validate classmethod

        # 2. Public metadata inspection interface properties
        "value_type_name",  # Plain-text string nomenclature of the type (str)
        "is_constant",      # Boolean flag declaring whether this node behaves as a constant

        # 3. Dynamic internal instance class lazy memory caches
        "_atom_class_mutable",
        "_atom_class_immutable"
    )

    #--- Initialization logic execution sequence hooks ---#
    # (this routine is automatically triggered inside the parent constructor pipeline)
    def _process_user_data(
        self: "SimpleConstantMetadataProtocol"
    ) -> None:

        # 1. Formally flag the model component metadata state as a constant leaf
        self.is_constant = True

        # 2. Extract, evaluate, and normalize the raw type descriptor parameters
        (self.value_type,
         self.value_type_name) = process_type(
            owner_class=self.owner_class
        )

        # 3. Materialize and process the default structural fallback target values
        self.default = process_default_for_constant(
            default_type=self.value_type,
            owner_class=self.owner_class
        )

        # 4. Bind, parse, and verify the structural boundaries of the _validate interface
        self.validate = process_classmethod(
            method_name="_validate",
            expected_params=("cls", "value", "return_bool"),
            expected_args_params_count=2,
            expected_args_defaults=(),
            expected_kwargs_defaults={"return_bool": False},
            expected_param_types={"value": Any, "return_bool": bool},
            expected_return_type=bool | None,
            test_value=(self.default,),
            owner_class=self.owner_class,
        )

        # 5. Initialize internal lazy caching anchors to the architectural UNSET sentinel
        self._atom_class_mutable = UNSET
        self._atom_class_immutable = UNSET

    #--- Property definitions governing lazy class synthesis and caching ---#
    # (returns the dynamic atomic class blueprint used to spin up instances)
    @property
    def atom_class_mutable(
        self: "SimpleConstantMetadataProtocol"
    ) -> "AtomInstanceProtocol":
        """Lazy access gateway delivering the mutable core class structure for this parameter."""
        if self._atom_class_mutable is UNSET:
            self._atom_class_mutable = make_atom_class(self.owner_class.__metadata__)
        return self._atom_class_mutable

    @property
    def atom_class_immutable(
        self: "SimpleConstantMetadataProtocol"
    ) -> "AtomInstanceProtocol":
        """Lazy access gateway delivering the immutable core class structure for this parameter."""
        if self._atom_class_immutable is UNSET:
            self._atom_class_immutable = make_atom_class(self.owner_class.__metadata__, mutable=False)
        return self._atom_class_immutable


_DESIGN_NOTES = """
# SimpleConstantMetadata

## Purpose
Acts as the central configuration compiler and execution orchestrator for constant leaf nodes inside the object model metadata architecture. It transforms loose declarative class attributes (`_type`, `_default`, `_validate`) into strict, high-performance runtime metadata specifications.

## Architectural Design Decisions

### 1. Unified Substrate Slots Footprint (`__slots__`)
* The explicit declaration of `__slots__` blocks the allocation of local instance dictionaries (`__dict__`). This choice minimizes the system footprint during massive bulk meta-graph initialization sweeps.
* It enforces strict structural shape boundaries; down-tree metadata definitions cannot arbitrarily write un-tracked operational states directly into the data controller.

### 2. Isolation of Ingestion Pipeline Phases (`_process_user_data`)
* The processing of user definitions flows through a highly deterministic order:
  1. **Type Normalization**: Establish explicit type contracts first.
  2. **Default Value Resolution**: Ensure the fallback value matches the determined type constraint.
  3. **Signature Verification**: Validate the `_validate` routine signature and test it immediately against the resolved default value.
* If a default value violates the type definition, or if a `_validate` method contains signature mismatches, the pipeline halts immediately at initialization time, preventing corrupt configurations from bleeding into runtime instance loops.

### 3. Asymmetric Lazy Class Caching Strategy
* The properties `atom_class_mutable` and `atom_class_immutable` are entirely decoupled and lazily constructed on demand using the `UNSET` sentinel pattern.
* Metaprogramming class compilation (`make_atom_class`) is deferred until the exact moment an instance allocation is requested. This dramatically reduces early class loading strain for vast domain graphs containing hundreds of defined models that may never actually be instantiated during a light execution thread lifecycle.
"""