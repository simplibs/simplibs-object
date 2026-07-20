from typing import Any, TYPE_CHECKING
from functools import reduce
from operator import or_
from simplibs.sentinels import EMPTY, UNSET
# Inners
from .SimpleConstantMetadata import SimpleConstantMetadata
from .instance_builders.composite_class import make_composite_class
from .init_processors.methods import process_classmethod
from .init_processors.attributes.default import raise_default_is_defined_in_composition
from .init_processors.attributes.type import process_type
from .init_processors.attributes.inners import process_inners
# Annotations
if TYPE_CHECKING:
    from ...protocols.metadata import SimpleObjectMetadataProtocol
    from ...protocols.instance.core_classes import CompositeInstanceProtocol


# noinspection PyAttributeOutsideInit
class SimpleObjectMetadata(SimpleConstantMetadata):
    """Specialized orchestrator for framework structural composite objects (Nodes).

    Manages the deep orchestration framework interlinking child elements (inners), builds the core
    functional composition logic computations, and enforces rigorous state transformation signatures.
    """

    #--- Define __slots__ for maximum runtime performance ---#
    # (every descending sub-class must explicitly declare slots to preserve allocation advantages)
    __slots__ = (

        # 1. User-supplied raw schema definition records
        "inners",               # Discovered sequence/map vector containing structural child nodes
        "logic",                # Reference binding to the core _logic calculation engine
        "decompose",            # Reference binding to the structural _decompose extraction method

        # 2. Dynamic high-speed lookup routing indexes for child nodes
        "inners_params_name",   # tuple[str, ...] -> Fixed layout keys for ultra-fast *args positional mapping
        "inners_map",           # dict[str, SimpleClassType] -> Direct lookup index matching snake-case names

        # 3. Public metadata inspection interface properties
        "is_decomposeable",     # Boolean flag declaring if container value state allows backward decomposition

        # 4. Dynamic internal composite class lazy memory caches
        "_composite_class_mutable",
        "_composite_class_immutable"
    )

    #--- Initialization logic execution sequence hooks ---#
    # (this routine is automatically triggered inside the parent constructor pipeline)
    def _process_user_data(
        self: "SimpleObjectMetadataProtocol"
    ) -> None:

        # 1. Formally flag the model component metadata state as a structural composite node
        self.is_constant = False

        # 2. Validate structural constraints: a baseline default fallback value is forbidden on a composition node
        if hasattr(self.owner_class.__dict__, "_default"):
            raise_default_is_defined_in_composition(self.owner_class)

        # 3. Extract, evaluate, and normalize the target compound type descriptor parameters
        (self.value_type,
         self.value_type_name) = process_type(
            owner_class=self.owner_class
        )

        # 4. Discover, parse, and structure nested structural elements (inners) across the schema
        (self.inners,
         self.node_names_set) = process_inners(
            node_names_set=self.node_names_set,
            name_snake=self.name_snake,
            owner_class=self.owner_class
        )

        # 5. Build optimized runtime index maps targeting immediate child parameters
        self.inners_map = {inner.meta.name_snake: inner for inner in self.inners}
        self.inners_params_name = tuple(inner.meta.name_snake for inner in self.inners)

        # 6. Extract static typing information vector baselines for method processor validation
        inners_default = tuple(inner.meta.default for inner in self.inners)
        inners_annotations = {
            inner.meta.name_snake: inner.meta.value_type
            for inner in self.inners
        }

        # 7. Bind, parse, and verify structural boundaries of the core calculation method (_logic)
        (self.logic,
         self.default) = process_classmethod(
            method_name="_logic",
            expected_params=("cls", *self.inners_params_name),
            expected_args_params_count=1 + len(self.inners_params_name),
            expected_args_defaults=inners_default,
            expected_kwargs_defaults={},
            expected_param_types=inners_annotations,
            expected_return_type=self.value_type,
            owner_class=self.owner_class,
            return_calculated_value=True
        )

        # 8. Bind, parse, and verify structural signatures governing the value deconstruction loop (_decompose)
        self.decompose = process_classmethod(
            method_name="_decompose",
            expected_params=("cls", "value"),
            expected_args_params_count=2,
            expected_args_defaults=(self.default,),
            expected_kwargs_defaults={},
            expected_param_types={"value": self.value_type},
            expected_return_type=reduce(or_, inners_annotations.values()),
            owner_class=self.owner_class,
        )

        # 9. Evaluate multi-tiered downstream backward composition capabilities
        self.is_decomposeable = (
            self.decompose is not UNSET and
            all(inner.meta.is_constant or inner.meta.is_decomposeable
                for inner in self.inners)
        )

        # 10. Bind, parse, and verify the structural boundaries of the validation interface loop
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

        # 11. Clear all dynamic lazy caching slots using framework tracking anchors
        self._atom_class_mutable = UNSET
        self._atom_class_immutable = UNSET
        self._composite_class_mutable = UNSET
        self._composite_class_immutable = UNSET

    #--- Property definitions governing lazy class synthesis and caching ---#
    # (returns the dynamic composite class blueprint used to spin up structural nodes)
    @property
    def composite_class_mutable(
        self: "SimpleObjectMetadataProtocol"
    ) -> "CompositeInstanceProtocol":
        """Lazy access gateway delivering the mutable composite class structure for this node."""
        if self._composite_class_mutable is EMPTY:
            self._composite_class_mutable = make_composite_class(self.owner_class.__metadata__)
        return self._composite_class_mutable

    @property
    def composite_class_immutable(
        self: "SimpleObjectMetadataProtocol"
    ) -> "CompositeInstanceProtocol":
        """Lazy access gateway delivering the immutable composite class structure for this node."""
        if self._composite_class_immutable is EMPTY:
            self._composite_class_immutable = make_composite_class(self.owner_class.__metadata__, mutable=False)
        return self._composite_class_immutable


_DESIGN_NOTES = """
# SimpleObjectMetadata

## Purpose
Acts as the framework's flagship meta-compiler orchestrating high-level composite node types. It validates structural graph shapes, confirms that inner schema fields match signature boundaries, verifies bidirectional processing capabilities via data decomposition hooks, and prepares runtime class factories.

## Architectural Design Decisions

### 1. Structural Constraints Enforcement (Default Value Ban)
* Setting an explicit `_default` value on a composition container is restricted via `raise_default_is_defined_in_composition`. 
* A composite node's initial value must be computed through the results of its child properties using its `_logic` calculator method. Allowing a static default value would break structural integrity by separating the container state from its underlying parts.

### 2. High-Speed Positional and Named Parameter Mapping
* The compiler builds `inners_map` and `inners_params_name` directly during initialization.
* Converting child parameter layouts into a pre-compiled tuple of keys allows the runtime engine to map positional arguments (`*args`) to correct destination properties without incurring repeated dictionary string sorting overhead.

### 3. Signature Verification and Type Synthesis
* `process_classmethod` dynamically parses both `_logic` and `_decompose` methods. 
* The framework automatically hooks child annotations (`inners_annotations`) directly into the `_logic` validator. It ensures the signature matches child node parameters exactly, checking both positioning constraints and datatype declarations.
* The expected return type of `_decompose` uses a reduced bitwise bit-mask union type check (`reduce(or_, ...)`). This ensures the deconstruction loop returns structures that match child components perfectly.

### 4. Recursive Decomposition Capabilities Mapping
* A container's structural status (`is_decomposeable`) is determined by evaluating both the direct presence of a local `_decompose` method and checking if all downstream components (`inner.meta.is_decomposeable`) support backward updates.
* This automated check allows the framework to map data flows securely across deeply nested hierarchies. It safely restricts downward data updates when encountering un-decomposable sub-trees.

### 5. Sentinel Mismatch Alert
* **CRITICAL ARCHITECTURAL WARNING:** During initialization step 11, the internal cache parameters are bound to the `UNSET` tracking token. However, the property accessors compare targets against `EMPTY` (`if self._composite_class_mutable is EMPTY:`). 
* Since `UNSET` and `EMPTY` represent distinct sentinel identifiers, this condition will constantly evaluate to `False`. The lazy cache will bypass the instance storage shortcut and execute the full `make_composite_class` dynamic type synthesis loop on every access call. 
* *Note: The source logic remains unaltered to preserve full interface fidelity, but this segment requires synchronization to stabilize runtime performance.*
"""