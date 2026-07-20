from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from .._exceptions_helpers import exception_info_for_classmethod
# Inners
from ._clone_classmethod import _clone_classmethod
from .validations import (
    validate_method_is_defined,
    validate_method_is_callable,
    validate_method_is_classmethod
)
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike
    from .......protocols.methods import ClassMethodProtocol


def verify_classmethod(
    method_name: str,
    owner_class: "SimpleClassLike",
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
) -> tuple[bool, classmethod | "ClassMethodProtocol"]:  # tuple[bool(should_validate), return_object]
    """Performs reflection verification and runtime isolation for framework hooks on a target class layout.

    Analyzes inheritance structures, direct class overrides, and ancestor boundaries to determine
    if the target method requires signature verification or structural cloning.
    """

    # 1. Prepare raw layout metadata and runtime attributes
    raw_method = owner_class.__dict__.get(method_name, UNSET)
    bound_method = getattr(owner_class, method_name)

    # 2. Check if the retrieved attribute evaluates as a classmethod descriptor
    if isinstance(bound_method, classmethod):
        bound_method: ClassMethodProtocol  # Type re-assertion for static analyzers

        # 2.1 Process explicitly overriden/newly defined methods in local class body
        if raw_method:
            return True, bound_method

        # 2.2 Process inheritance boundary for '_validate' (inherited validations are never re-verified)
        if method_name == "_validate":
            return False, bound_method

        # 2.3 Check if the current layout is a direct descendant of the base SimpleObject class
        from .......SimpleObject import SimpleObject
        is_direct_descendant = SimpleObject in owner_class.__bases__

        # 2.4 Process inheritance evaluation for '_logic' and '_decompose' on deep subclasses
        if not is_direct_descendant:
            need_validations = bool(owner_class.__dict__.keys() & {"_inners", "_type", "_logic"})
            output_bound_method = _clone_classmethod(bound_method) if need_validations else bound_method
            return need_validations, output_bound_method

        # 2.5 Process base-level resolution for optional '_decompose' hook (if undefined, '_logic' falls through to exceptions)
        if method_name == "_decompose":
            return False, UNSET

    # 3. Compile full descriptive payload mapping for exception execution pipelines
    base_info_for_exception = exception_info_for_classmethod(
        bound_method=bound_method,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count
    )

    # 4. Trigger localized micro-validations to diagnose structural and descriptor issues
    validate_method_is_defined(method_name, owner_class, base_info_for_exception)
    validate_method_is_callable(raw_method, base_info_for_exception)
    validate_method_is_classmethod(raw_method, base_info_for_exception)
    return False, UNSET  # Unreachable structural fallback line


_DESIGN_NOTES = """
# verify_classmethod

## Core Architectural Role
The `verify_classmethod` function acts as the critical reflection gatekeeper for classmethod lifecycle parsing within the framework. When a class definition inherits from `SimpleObject`, the system must intercept its core structural hook methods (`_validate`, `_logic`, `_decompose`). This orchestrator safely inspects Python's runtime namespaces, untangles complex class inheritance chains, prevents framework memory pollution via explicit object cloning, and routes any malformed structures directly to localized validation pipelines.

## Detailed Breakdown of the Verification & Routing Process

### Phase 1: Dual-Layer Namespace Extraction
The orchestrator avoids using naive attribute access alone. Instead, it captures two completely different dimensions of the same object simultaneously:
1. `owner_class.__dict__.get(method_name)`: Inspects only the *immediate, local* class namespace dictionary. If the target attribute is missing here, it evaluates to `UNSET` (or `None`), proving that the method is inherited from a parent class without local modification.
2. `getattr(owner_class, method_name)`: Resolves through the entire Method Resolution Order (MRO) to find the actual runtime object ready for invocation.

### Phase 2: Descriptor Check & The Happy/Inherited Path Matrix
If the resolved `bound_method` is successfully identified as an instance of `classmethod`, the code enters a high-speed routing matrix based on structural state rules:

* **Direct Local Override (Section 2.1)**: If `raw_method` exists locally in the class `__dict__`, it means the developer has actively rewritten this hook method on this specific class. It immediately flags `need_validations = True` and returns the bound reference for bytecode inspection.
* **The `_validate` Inheritance Border (Section 2.2)**: The core validation hook `_validate` is inherently stateless and reusable across child classes. If it is inherited (not local), it has already passed strict inspection during the parent class's compilation phase. Re-verifying it would cause redundant processor cycles, so the orchestrator returns `False` to bypass signature checks.
* **Deep Subclassing & Component Extraction (Sections 2.3 & 2.4)**: When analyzing methods on classes that are nested deep within an inheritance hierarchy (not direct descendants of `SimpleObject`), the orchestrator performs a fast bitwise intersection check (`&`). It scans the local class namespace keys for active structural configurations (`_inners`, `_type`, or `_logic`).
  * If these definitions are present, it signifies that the subclass represents a new architectural layout. To protect the ancestor class's descriptor from frame pollution or downstream argument injections, the method is decoupled using `_clone_classmethod`.
* **Optional Fallbacks (Section 2.3 & 2.5)**: The `_decompose` method is an optional architectural framework hook. If the class is a direct descendant of `SimpleObject` and the descriptor check falls through to this point, it means `_decompose` was never declared. The system gracefully returns `False` and an `UNSET` payload, allowing execution to skip decomposition without crashing.

### Phase 3: The Cold Error-Reporting Perimeter
If the resolved method completely fails the `isinstance(bound_method, classmethod)` conditional, it means the class structure is severely corrupted or violates framework syntax rules (e.g., the developer omitted the `@classmethod` decorator, wrote a raw variable, or completely forgot to declare a mandatory hook like `_logic`).
1. **Lazy Diagnostic Construction**: The function invokes `exception_info_for_classmethod` to compile all required file locations, class properties, and target layout mockups into the `base_info_for_exception` dictionary.
2. **Cascaded Isolation**: The data is fed sequentially into the micro-validation stack:
   * `validate_method_is_defined`: Verifies if the token name exists anywhere in the class tree.
   * `validate_method_is_callable`: Verifies that the internal attribute can be executed as a functional block.
   * `validate_method_is_classmethod`: Diagnoses the exact missing decorator boundary error and triggers a domain-specific `SimpleMetadataError`.
"""