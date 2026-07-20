from typing import Any, TYPE_CHECKING
from types import UnionType
from simplibs.sentinels import UNSET
# Inners
from .decompose_method import verify_decompose_outcome
from .validations import raise_method_raised_exceptions, raise_method_return_unvalide_outcome_type
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike
    from .......protocols.methods import ClassMethodProtocol


def verify_calculation(
    bound_method: "ClassMethodProtocol",
    test_value: Any,
    expected_return_type: type | UnionType,
    owner_class: "SimpleClassLike",
) -> Any:
    """Orchestrates the deterministic test execution of a classmethod hook to verify its operational integrity.

    Executes the targeted method under a controlled boundary, intercepts internal exceptions,
    and validates the types and structure of the computed return values.
    """

    # 1. Define the output tracking variable placeholder
    calculate_result = UNSET

    # 2. Execute the deterministic dry-run validation calculation
    try:
        calculate_result = bound_method(*test_value)
    except Exception as e:
        raise_method_raised_exceptions(e, bound_method)

    # 3. Verify that the calculated result closely conforms to the expected type specification
    if not isinstance(calculate_result, expected_return_type):
        raise_method_return_unvalide_outcome_type(calculate_result, expected_return_type, bound_method)

    # 4. Perform localized inner structural integrity inspection for the '_decompose' hook
    if bound_method.__func__.__name__ == "_decompose":
        calculate_result: tuple[Any, ...]  # Type re-assertion for static analysis tooling
        verify_decompose_outcome(calculate_result, owner_class, bound_method)

    # 5. Return the fully verified computed output value
    return calculate_result


_DESIGN_NOTES = """
# verify_calculation

## Core Architectural Role
The `verify_calculation` orchestrator represents the deterministic runtime validation gateway of the framework's metadata initialization pipeline. While other verifiers (like `verify_params` and `verify_classmethod`) enforce static properties—such as bytecode structure, signature limits, and descriptor wrapping—`verify_calculation` is responsible for operational evaluation. It executes a controlled dry-run test of the user-defined classmethod hook using framework-supplied test tokens (`test_value`). This ensures that the method's internal code logic executes successfully without throwing arbitrary exceptions and that its computed outputs strictly conform to the structural layout required by the core engine.

## Detailed Breakdown of the Calculation Verification Process

### Phase 1: Controlled Dry-Run Invocation & Exception Interception
The function encapsulates the application-level method invocation inside a defensive `try-except` block. 
* **Dynamic Argument Unpacking**: The `test_value` payload is unpacked directly into the target method signature via the standard variable-argument unpacker (`*test_value`). 
* **Exception Isolation Perimeter**: If the user's method throws an unhandled error during execution, the exception is intercepted (`except Exception as e`). Instead of letting the application crash with a generic traceback, the raw exception reference and the target method context are routed directly to `raise_method_raised_exceptions`. This mapping component converts the raw state error into a high-level domain error, preserving diagnostic information.

### Phase 2: Type Assertion Enforcer
Once an execution result is successfully captured, the orchestrator performs a strict type evaluation using a native `isinstance` check against `expected_return_type`. 
* **UnionType Integration**: Because Python allows multi-type definitions through standard type unions (such as `int | str` or `Union[type, type]`), the parameter directly accepts `UnionType` configurations.
* **Type Inversion Defense**: If the calculated data payload deviates from the expected model contract, execution drops out of the happy path into `raise_method_return_unvalide_outcome_type`. This layer handles failure formatting, letting the developer know exactly what invalid type was received versus what the architecture expected.

### Phase 3: Targeted Micro-Orchestration for Specialized Hooks
The framework applies extra structural requirements to specific lifecycle phases. The function inspects the internal string identification tag `bound_method.__func__.__name__` to target these specialized flows:
* **The Decomposition Contract (`_decompose`)**: If the orchestrator detects it is analyzing the `_decompose` method, it knows the framework requires a strict, structured sequence of items corresponding to the class configuration. The result is marked with an inline hint (`tuple[Any, ...]`) for static type checkers and passed to the nested orchestrator `verify_decompose_outcome`. This deeper validation layer unpacks the sequence and verifies that its internal contents align with the sub-components and fields declared within `owner_class`.

### Phase 4: Output Yield
If the calculated value successfully clears both the general type checker and the specialized method inspectors, it is returned as verified output. The framework can now trust this method reference completely, allowing initialization to finish smoothly.
"""