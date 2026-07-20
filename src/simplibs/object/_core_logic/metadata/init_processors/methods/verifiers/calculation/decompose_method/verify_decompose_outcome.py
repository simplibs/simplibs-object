from typing import Any, TYPE_CHECKING
# Inners
from .validations import (
    raise_decompose_unvalide_outcome_length,
    validate_decompose_unvalide_item_type,
    validate_decompose_unvalide_item_value
)
# Annotations
if TYPE_CHECKING:
    from ........protocols.methods import ClassMethodProtocol
    from ........protocols.classes import SimpleClassLike


def verify_decompose_outcome(
    calculate_default: tuple[Any, ...],
    owner_class: "SimpleClassLike",
    bound_method: "ClassMethodProtocol",
) -> None:
    """Verifies the internal structural alignment of the tuple returned by the '_decompose' hook.

    Validates that the sequence length matches the configured inner metadata definitions,
    and checks each individual item against its expected value type or default state fallback.
    """

    # 1. Extract the inner component definitions from the class metadata layout
    # noinspection PyProtectedMember
    inners = owner_class.meta.inners

    # 2. Verify structural length symmetry (the decomposed payload count must equal the inner count)
    if len(calculate_default) != len(inners):
        raise_decompose_unvalide_outcome_length(calculate_default, inners, bound_method)

    # 3. Iterate through and inspect the type and structural contract of each individual element
    for i, inner in enumerate(inners):
        inner: "SimpleClassLike"  # Type re-assertion for localized static analysis

        # 3.1 Extract the runtime computed value and its corresponding target type specification
        value = calculate_default[i]
        expected_type = inner.meta.value_type

        # 3.2 Evaluate compliance against the expected type or the registered default sentinel state
        if not isinstance(value, expected_type) and value != inner.meta.default:
            validate_decompose_unvalide_item_type(value, expected_type, inner, inners, bound_method)
            validate_decompose_unvalide_item_value(value, inner, inners, bound_method)


_DESIGN_NOTES = """
# verify_decompose_outcome

## Core Architectural Role
The `verify_decompose_outcome` function is a specialized structural sub-orchestrator within the framework's runtime validation layer. When a class handles complex internal compositions, the `_decompose` hook breaks down an active instance state into an ordered tuple of fundamental values. This orchestrator is responsible for ensuring data contract integrity between the output of `_decompose` and the class's compiled metadata declarations (`owner_class.meta.inners`). By checking these boundaries during initialization or evaluation dry-runs, it guarantees that data flows safely without indexing mismatches or type drift.

## Detailed Breakdown of the Structural Verification Process

### Phase 1: Metadata Extraction & Cardinality Alignment
The orchestrator relies on the framework's pre-compiled structural schema to drive its inspection logic:
* **Structural Length Symmetry Check**: Before checking individual values, the function verifies length balance. It compares the size of the calculated sequence (`len(calculate_default)`) against the total number of registered inner components (`len(inners)`).
* **Defensive Boundary Control**: If a developer changes the internal components of a class but forgets to update the sequence in the `_decompose` method, the length test fails immediately. The routine aborts the happy path and routes execution to `raise_decompose_unvalide_outcome_length`. This component builds a clear error layout mapping the mismatched indices to help with debugging.

### Phase 2: Index-Aligned Positional Iteration
If the collection lengths match, the function begins a detailed structural inspection. It uses `enumerate(inners)` to process the metadata components alongside their corresponding positions in the output tuple.
* **Component Context Isolation**: For each step in the loop, the orchestrator pulls out the active runtime value (`calculate_default[i]`) and locates its matching metadata properties, specifically the required data type (`inner.meta.value_type`).

### Phase 3: The Dual-Condition Type & Sentinel Validation Matrix
The core evaluation logic uses a combined validation conditional block:
`if not isinstance(value, expected_type) and value != inner.meta.default:`

This expression accommodates two valid states for every item in a decomposed sequence:
1. **The Primary Type Contract**: The calculated item should match the explicit class definition type (`isinstance(value, expected_type)` evaluates to `True`).
2. **The Sentinel/Default Escape Route**: The item can match the registered fallback default state (`value != inner.meta.default` evaluates to `False`). This allows uninitialized, empty, or reset components to pass inspection safely.

### Phase 4: Micro-Validation Diagnostics & Escalation
When a item fails both valid state criteria, the function passes control to a micro-validation cascade designed to pinpoint the exact syntax error:
* `validate_decompose_unvalide_item_type`: Evaluates and formats the type signature error, showing the invalid class reference alongside the expected type rule.
* `validate_decompose_unvalide_item_value`: Analyzes value discrepancies or bad states within that specific position.

This clear separation ensures that any structural break in a composite object raises an informative, index-mapped error trace instead of causing silent data corruption further down the pipeline.
"""