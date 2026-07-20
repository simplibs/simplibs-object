from typing import Any, TYPE_CHECKING
# Outers
from .._exceptions_helpers import exception_info_for_classmethod
# Inners
from .validations import validate_args_defaults, validate_kwargs_defaults, validate_annotations
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol


def verify_annotations_and_defaults(
    bound_method: "ClassMethodProtocol",
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    bound_method_annotations: dict[str, Any],
    expected_args_defaults: tuple | None,
    expected_kwargs_defaults: dict[str, Any],
):
    """Orchestrates the verification of method signatures, parameter type hints, and initialization defaults.

    Evaluates the method descriptor's internal byte structures to confirm that the contract
    defined by user hooks aligns perfectly with the framework's semantic specifications.
    """

    # 1. Compile full descriptive payload mapping for exception execution pipelines
    base_info_for_exception = exception_info_for_classmethod(
        bound_method=bound_method,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count
    )

    # 2. Validate type hints and parameter annotations if explicitly declared
    if bound_method.__func__.__annotations__:
        validate_annotations(bound_method_annotations, bound_method, base_info_for_exception)

    # 3. Validate positional-argument defaults against structural boundary rules
    if bound_method.__func__.__defaults__:
        validate_args_defaults(expected_args_defaults, expected_params, bound_method, base_info_for_exception)

    # 4. Validate keyword-only argument defaults against framework mapping keys
    if bound_method.__func__.__kwdefaults__:
        validate_kwargs_defaults(expected_kwargs_defaults, bound_method, base_info_for_exception)


_DESIGN_NOTES = """
# verify_annotations_and_defaults

## Core Architectural Role
The `verify_annotations_and_defaults` function is a crucial configuration orchestrator operating during the bootstrap phase of the framework's runtime model compilation. When a classmethod hook clears low-level descriptor routing (in `verify_classmethod`), it must pass through this block to ensure its internal signature contract is valid. The routine reads the bytecode metadata of the function to verify that the type hints, positional default sequences, and keyword-only configurations provided by the developer match the exact semantic contracts expected by the framework.

## Detailed Breakdown of the Verification & Gating Process

### Phase 1: Proactive Diagnostic Assembly
Instead of compiling context details within individual exception sub-systems, the orchestrator begins by building a shared diagnostic state using `exception_info_for_classmethod`. 
* This operation extracts metadata from `bound_method` and maps it alongside `expected_params` and `expected_args_params_count` into the `base_info_for_exception` payload.
* By passing this pre-built diagnostic map directly into each downstream validation micro-component, the system minimizes overhead during the happy path while ensuring rich error formatting if a verification fails.

### Phase 2: Lazy Annotation Evaluation
The framework does not enforce rigid typing requirements if type hints are omitted completely. However, if the developer chooses to add signatures, they must be accurate:
* **The `__annotations__` Gate**: The system checks `bound_method.__func__.__annotations__`. If this mapping contains entries, it triggers `validate_annotations`.
* **Constraint Enforcement**: This component cross-references the runtime types passed in `bound_method_annotations` against the developer's declarations. If there is a mismatch (e.g., an incorrect return type or a misaligned argument parameter hint), it raises an informative domain error.

### Phase 3: Positional Default Sequence Analysis
Python captures standard positional default values sequentially inside an ordered tuple under the `__defaults__` property:
* **The `__defaults__` Gate**: If `bound_method.__func__.__defaults__` evaluates to a non-empty tuple, it means positional fallback parameters are actively being used.
* **Symmetry Check**: Control is routed to `validate_args_defaults`, which processes the default values alongside `expected_args_defaults` and `expected_params`. It ensures that default arguments are assigned only to valid positions and that the types of these fallbacks align with framework specs.

### Phase 4: Keyword-Only Map Verification
Keyword-only arguments (declared after a bare `*` or a `*args` sequence) are managed separately by the Python runtime inside a dedicated mapping dictionary:
* **The `__kwdefaults__` Gate**: The function checks `bound_method.__func__.__kwdefaults__`.
* **Key Alignment Enforcer**: If present, it triggers `validate_kwargs_defaults` to verify that all provided keyword-only keys and values match the configured keys in `expected_kwargs_defaults`. This protects downstream execution from unexpected keyword arguments that could bypass standard initialization layers.
"""