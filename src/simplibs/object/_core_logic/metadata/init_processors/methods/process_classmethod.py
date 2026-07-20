from typing import Any, TYPE_CHECKING
from types import UnionType
# Inners
from .verifiers import (
    verify_classmethod,
    verify_params,
    verify_calculation,
    verify_annotations_and_defaults
)
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike
    from .....protocols.methods import ClassMethodProtocol


def process_classmethod(
    method_name: str,
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    expected_args_defaults: tuple | None,
    expected_kwargs_defaults: dict[str, Any],
    expected_param_types: dict[str, type | UnionType],
    expected_return_type: type | UnionType,
    owner_class: "SimpleClassLike",
    test_value: tuple = (),
    return_calculated_value: bool = False,
) -> Any:
    """Orchestrates the entire reflection, verification, injection, and compilation pipeline for standard class methods.

    Reflects the targeted descriptor from the class layout, executes standard signature verification rules,
    injects framework specification metadata, and runs a deterministic dry-run verification calculation.
    """

    # 1. Perform structural baseline evaluation of user-defined method layout
    need_validations, bound_method = verify_classmethod(
        method_name=method_name,
        owner_class=owner_class,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count,
    )
    # Type casting
    bound_method: "ClassMethodProtocol"

    # 2. Execute signature enforcement and default parameter injection if processing a new definition level
    if need_validations:

        # 2.1 Enforce operational parameters bounds
        verify_params(
            expected_params=expected_params,
            expected_args_params_count=expected_args_params_count,
            bound_method=bound_method,
        )

        # 2.2 Construct full expected runtime signature specification
        bound_method_annotations = {
            **expected_param_types,
            "return": expected_return_type
        }

        # 2.3 Verify explicit developer annotations and defaults if overrides exist
        if (bound_method.__func__.__annotations__ or
            bound_method.__func__.__defaults__ or
            bound_method.__func__.__kwdefaults__):
            verify_annotations_and_defaults(
                bound_method=bound_method,
                expected_params=expected_params,
                expected_args_params_count=expected_args_params_count,
                bound_method_annotations=bound_method_annotations,
                expected_args_defaults=expected_args_defaults,
                expected_kwargs_defaults=expected_kwargs_defaults
            )

        # 2.4 Inject fallback defaults and standardized signatures directly into the function frame
        bound_method.__func__.__defaults__ = expected_args_defaults
        bound_method.__func__.__kwdefaults__ = expected_kwargs_defaults
        bound_method.__func__.__annotations__ = bound_method_annotations

    # 3. Perform a deterministic validation execution test run to verify structural processing logic
    calculated_value = verify_calculation(
        bound_method=bound_method,
        test_value=test_value,
        expected_return_type=expected_return_type,
        owner_class=owner_class
    )

    # 4. Return processed runtime methods and verified internal calculation state
    if return_calculated_value:
        return bound_method, calculated_value
    return bound_method


_DESIGN_NOTES = """
# process_classmethod

## Core Architectural Role
The `process_classmethod` function acts as the root orchestrator for the framework's method-reflection and metadata-injection assembly line. It serves as the single point of coordination connecting low-level descriptor inspection, signature normalization, and deterministic execution checking. During class compilation, the framework routes discovered user hooks (such as lifecycle rules or mutation definitions) through this routine. It dynamically audits the developer's definitions, normalizes default configurations, injects unified framework type maps, and tests execution sanity before locking down the compiled class model state.

## Detailed Breakdown of the Compilation and Injection Pipeline

### Phase 1: Structural Reflection and State Gating
The assembly pipeline begins by resolving the targeted classmethod from the raw class definition layout:
* **Descriptor Inspection**: It calls `verify_classmethod` to reflect the method by string identifier (`method_name`) from the `owner_class` namespace. This sub-system evaluates descriptor boundaries and returns an evaluation tuple containing a boolean gating flag (`need_validations`) and the verified `bound_method` descriptor object.
* **Inheritance Protection Gate**: The `need_validations` boolean acts as an optimization gate. If the method reference is inherited unmodified from a parent class that has already been compiled, the orchestration pipeline skips initialization sub-steps to prevent unnecessary modifications to shared parent references.

### Phase 2: Structural Verification and Validation
If the gate determines that a new validation phase is required (`need_validations` evaluates to `True`), the orchestrator applies strict structural checks:
* **Signature Alignment**: The routine triggers `verify_params` to confirm that the number and naming conventions of the parameters defined by the user match the strict baseline expected by the framework.
* **User Override Verification**: The orchestrator builds a unified reference signature dictionary (`bound_method_annotations`) combining param types and the mandatory `"return"` key. It then evaluates if the developer has declared custom annotations or defaults. If any exist, it routes execution to `verify_annotations_and_defaults` to catch configuration mismatches before they enter the runtime environment.

### Phase 3: Framework Injection and Signature Normalization
Once all validation checks pass, the orchestrator updates the function frame directly:
* **State Standardization**: It applies the configuration specs directly onto the underlying function fields:
  * `bound_method.__func__.__defaults__`: Injects the structural positional defaults.
  * `bound_method.__func__.__kwdefaults__`: Injects the keyword-only fallback map.
  * `bound_method.__func__.__annotations__`: Overwrites the function's type system annotations with the framework's normalized type specification map.
* **System Predictability**: This step standardizes method behavior, ensuring that downstream components can interact with user hooks using a predictable, unified signature interface.

### Phase 4: Deterministic Invocation Auditing and Output Resolution
The final phase validates the operational stability of the newly configured hook:
* **Dry-Run Auditing**: The orchestrator calls `verify_calculation`, passing the target method, test inputs (`test_value`), expected output types, and the owner class reference. This triggers a controlled execution run to confirm that the method runs successfully and that its returned payload matches the structural rules of the application framework.
* **Flexible Dispatch Routing**: Depending on the configuration state requested by the caller via `return_calculated_value`, the orchestrator returns either the fully prepared classmethod descriptor alone, or pairs it with the validated dry-run result tuple. This provides flexibility for components that require immediate access to computed initialization data.
"""