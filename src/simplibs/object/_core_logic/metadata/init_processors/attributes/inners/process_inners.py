from typing import TYPE_CHECKING, Any
from simplibs.sentinels import UNSET
# Inners
from .validations.inners import (
    validate_inners_is_not_empty,
    validate_inners_is_defined,
    validate_inners_is_tuple,
)
from .validations.inner import (
    validate_inner_is_simple_subclass,
    validate_inner_is_not_simple_class,
    validate_inner_is_class,
)
from .validations.name_collisions import (
    validate_collision_within_inners,
    validate_if_collision_with_owner_class,
)
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike


def process_inners(
    node_names_set: set,
    name_snake: str,
    owner_class: "SimpleClassLike",
) -> tuple:
    """
    Validates and processes the list of inner elements (inners) of a composite class.

    Inners determine whether the class behaves as a constant (no inners) or as a
    composition (with inners). This ensures a consistent interface across all classes.

    Args:
        node_names_set (set): Set of names already registered in the parent hierarchy.
        name_snake (str): Snake_case name of the owner class.
        owner_class (SimpleMetadataType): The class being processed.

    Returns:
        tuple: A 5-tuple containing:
            - raw_inners (tuple): Original inner classes
            - new_node_names_set (set): Updated set of all used names
            - inners_params_name (tuple): Names for the _logic method parameters
            - inners_default (dict): {name: default_value} for default computation
            - inners_annotations (dict): {name: type} for type hints
    """

    # 1. Acquire the attribute value
    raw_inners = getattr(owner_class, "_inners", UNSET)

    # 2. Verify whether it is newly defined
    need_validations = "_inners" in owner_class.__dict__ and raw_inners is not UNSET

    # 3. Base validations
    if need_validations:

        # 3.1 Format validation
        if (not raw_inners or
            not isinstance(raw_inners, tuple)):
            validate_inners_is_defined(raw_inners, owner_class)
            validate_inners_is_tuple(raw_inners, owner_class)
            validate_inners_is_not_empty(raw_inners, owner_class)

        # 3.2 Internal import for base classes required within the for-loop
        from ......SimpleConstant import SimpleConstant
        from ......SimpleObject import SimpleObject

    # 4. Prepare data containers
    new_node_names_set = node_names_set.copy()

    # 5. Main iteration through inners
    raw_inners: tuple["SimpleClassLike", ...]
    for inner in raw_inners:
        inner: type["SimpleClassLike"]

        # 5.1 Base validations: type, subclass, and not base class
        if need_validations:
            # noinspection PyUnboundLocalVariable
            if (not isinstance(inner, type) or
                not issubclass(inner, SimpleConstant) or
                inner is SimpleConstant or
                inner is SimpleObject):
                validate_inner_is_class(inner, raw_inners, owner_class)
                validate_inner_is_simple_subclass(inner, owner_class)
                validate_inner_is_not_simple_class(inner, owner_class)

        # 5.2 Check for name collisions with parent and siblings
        node_name_collisions = new_node_names_set & inner.meta.node_names_set
        if node_name_collisions:
            collision_name = next(iter(node_name_collisions))
            validate_if_collision_with_owner_class(collision_name, name_snake, inner, owner_class)
            if need_validations:
                validate_collision_within_inners(collision_name, name_snake, raw_inners, inner, owner_class)

        # 5.3 Register inner's names into the global namespace
        new_node_names_set.update(inner.meta.node_names_set)

    # 6. Return computed values
    return (
        raw_inners,
        new_node_names_set,
    )


_DESIGN_NOTES = """
# process_inners

## Purpose
Validates and processes the list of inner elements (`_inners`) of a composite class.
The inner elements determine whether the target class behaves as a constant leaf node (no inners defined) or as a structural composition (with inners defined). This unified approach ensures a completely consistent public interface and strict arithmetic determinism across all object structures.

## The Crucial Role of Inners
Elements within the `_inners` collection must exclusively be class types that inherit from `SimpleConstant` (which structurally includes `SimpleObject`). This architectural constraint guarantees that every single registered component possesses:
  - A consistent metadata tracking namespace (`__metadata__`)
  - A strictly defined data type boundary annotation (`_type`)
  - A guaranteed baseline fallback default state (`_default`)
  - A fully resolved unique nested identifier index (`node_names_set`)

If the `_inners` attribute is actively defined, the class compilation pipeline automatically classifies the target entity as a `SimpleObject` (a composite structure). In the absolute absence of `_inners`, the class naturally compiles as a terminal `SimpleConstant` (an atomic leaf node).

## Operational Control Flow

### 1. Attribute Extraction and Boundary Validation
The routine initially attempts to fetch the `_inners` attribute directly from the local class `__dict__`. Following this extraction, a comprehensive triple-validation sequence is established:
  - Is the `_inners` token actively defined and present?
  - Is the container formatted explicitly as a standard Python `tuple`?
  - Is the provided tuple sequence populated (not an empty container)?

An empty tuple container represents a structural error because a node declaring an `_inners` namespace must contain actual components; otherwise, the attribute should be omitted entirely so the node can naturally compile as a pure constant leaf.

### 2. Container Preparation
Four distinct internal data containers are initialized to safely aggregate structural component attributes during the iteration phase:
  - `new_node_names_set` (set): The main cumulative identifier namespace accumulator (initialized as a shallow copy of the parent tracking index).
  - `inners_params_name` (list): Stores target parameter names required to dynamically compile the downstream `_logic` execution method signature.
  - `inners_default` (dict): Maps individual components to their fallback states for late-bound composite default computations.
  - `inners_annotations` (dict): Collects type boundary annotations to generate precise runtime type hints for the compilation engine.

### 3. Isolated Base Class Imports
The core base framework classes (`SimpleConstant` and `SimpleObject`) are explicitly imported locally within this block rather than at the root module level. This completely shields the system initialization cycle from circular dependency runtime loops. Furthermore, if high-level container format validations fail, these local imports are completely skipped, avoiding unnecessary CPU overhead during the error pathway execution.

### 4. Component Traversal Iteration
The engine opens a linear sequence traversing each individual inner element, enforcing the following checkpoints:

#### 4.1 Base Structural Type Guards
Evaluates the internal integrity of the reference type across three rigorous boundary layers:
  - `not isinstance(inner, type)` – Rejects active state instances or raw data values; inputs must be abstract class types.
  - `not issubclass(inner, SimpleConstant)` – Enforces framework family lineage alignment.
  - `inner is SimpleConstant` – Blocks utilizing the literal framework root base class directly as a functional data element.
  - `inner is SimpleObject` – Blocks utilizing the literal composite root base class directly as a functional data element.

Rationale: The composition layer demands concrete, user-defined operational domain blueprints, never the raw boilerplate framework roots themselves.

#### 4.2 Precision Lookahead Collision Detection
Computes a direct mathematical intersection between the cumulative active namespace (`new_node_names_set`) and the incoming component's internal index (`inner.meta.node_names_set`). If the intersection yields a conflict, specific diagnostics are routed:
  - The framework first checks if the conflict matches the root parent class identity (`validate_if_collision_with_owner_class`), blocking recursive loop paradoxes.
  - It then traces sibling namespaces down the tree (`validate_collision_within_inners`) to pinpoint the precise overlapping components.

This hierarchical evaluation pattern ensures exceptionally clear, actionable diagnostic exception reporting for the developer.

#### 4.3 Identifier Namespace Registration
Merges the incoming element's `inner.meta.node_names_set` directly into the global `new_node_names_set` accumulator via an in-place `.update()` operation. This guarantees that all nested sub-components are instantly mirrored within the local context, shielding subsequent elements from duplicating names down the line.

#### 4.4 Metadata Component Extraction
Extracts and registers the core semantic definitions from the target inner component:
  - `name_snake` – Resolves the parameter naming token required for the `_logic` signature mapping.
  - `meta.default` – Captures the individual component fallback state (utilized later during compound `process_default` calculations).
  - `meta.value_type` – Extracts type hint targets to accurately map structural validation types inside the dynamic reflection layout.

## Return Value Guarantees
The function finalizes by returning a structured tuple containing two computed states:
  - `raw_inners` – The original immutable tuple of class types (preserved for downstream structural mapping references).
  - `new_node_names_set` – The fully updated, comprehensive tracking index containing all identifier names captured across this entire composition subtree branch.

## Happy Path Optimization Strategy
The architecture is heavily optimized for the "happy path" layout, where class definitions are structurally sound and free of design anomalies:
  - Condition expressions located at primary execution boundaries are highly predictive of successful compilation passes, allowing the internal branch caching mechanisms to execute at maximum performance.
  - If a structural anomaly occurs, the control flow immediately steps out of the fast linear loop and transfers execution entirely to specialized error factories, ensuring zero runtime penalty during standard execution passes.
  - No redundant temporary memory or structural buffers are allocated during successful validation cycles.

## Architectural Architecture Notes
- The parent `node_names_set` index is explicitly isolated via a `.copy()` invocation immediately upon entry, guaranteeing that sibling tree processing never pollutes or alters the original tracking metadata state.
- Postponing the structural imports of `SimpleConstant`/`SimpleObject` directly guarantees they never execute before the core high-level happy path validation checks pass.
- This processor is highly specialized and is invoked exclusively inside the `SimpleObjectMetadata._process_user_interface()` lifecycle block.
- Any single structural or naming violation immediately terminates class compilation by throwing a pinpoint domain exception, preventing the system from ever settling into a degraded or ambiguous state.
"""