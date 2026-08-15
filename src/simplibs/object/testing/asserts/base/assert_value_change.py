from typing import Any
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.testing import maybe_subtest
# Outers
from ...containers.InnerValue import InnerValue


# noinspection PyTypeChecker
def assert_value_change(
    subtests: Any,
    instance: Any,
    *,
    value: Any | InnerValue,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """Assert that a value on a target instance (or its nested inner) changes correctly.

    Resolves the target instance (either the root instance or a nested inner node via
    ``InnerValue``), validates the candidate value against the node's schema, ensures it differs
    from the current state, applies the new value via the property setter, and verifies that
    the updated state matches expectations.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        instance: Root object instance under test.
        value: Explicit raw new value or an ``InnerValue`` container pointing to a nested node.
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.

    Returns:
        The validated, newly applied raw value.
    """
    subintro = "assert_value_change::"

    # 1. Resolve target instance and extract raw candidate value
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}resolve_target",
        verbose=verbose,
    ):
        if isinstance(value, InnerValue):
            target, candidate_value = value.as_instance_tuple(instance)
            if target is UNSET:
                pytest.fail("InnerValue path could not be resolved on target instance.")
        else:
            target = instance
            candidate_value = value

    # Store current value state for change assertions
    old_value = target.value

    # 2. Validate new value against target schema
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_new_value",
        verbose=verbose,
    ):
        if not target.validate(candidate_value, return_bool=True):
            pytest.fail(
                f"Value '{candidate_value}' is invalid for target '{target.meta.name_snake}'."
            )

    # 3. Ensure candidate value differs from the current state
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}not_original",
        verbose=verbose,
    ):
        if candidate_value == old_value:
            pytest.fail(
                f"New value must differ from current state value ({old_value!r})."
            )

    # 4. Apply new value via setter
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}apply_value",
        verbose=verbose,
    ):
        try:
            target.value = candidate_value
        except Exception as exc:
            pytest.fail(f"Failed to apply new value to target '{target.meta.name_snake}': {exc}")

    # 5. Ensure value actually changed and matches expected state
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}value_changed",
        verbose=verbose,
    ):
        if target.value != candidate_value:
            pytest.fail(
                f"Value did not change on '{target.meta.name_snake}': "
                f"expected {candidate_value!r}, got {target.value!r}."
            )

    return candidate_value


_DESIGN_NOTES = """
# assert_value_change (Universal Value Mutation Assertion)

## Purpose
Provides a robust, unified assertion blade for validating value changes on both root instances 
and deeply nested composite inner objects (`InnerValue`). It encapsulates validation pre-checks, 
state-diff sanity assertions, property setter execution, and post-mutation verification.

## Execution Matrix & Pipeline Steps
1. **Target Resolution (`InnerValue` Adapter):** Dynamically resolves whether mutation targets 
   the root instance or a nested inner attribute via `value.as_instance_tuple(instance)`.
2. **Schema Pre-Validation Gate:** Executes `target.validate(candidate_value, return_bool=True)` 
   to guarantee the candidate value is structurally and semantically valid before mutating state.
3. **Difference Assertion:** Confirms `candidate_value != target.value` upfront to prevent false-positive 
   no-op assignment passes.
4. **Setter Invocation:** Applies `target.value = candidate_value` inside a protected interception block.
5. **State Verification:** Asserts that `target.value == candidate_value` to guarantee state persistence.

## Downstream Role
Returns the validated `candidate_value`. This enables composite reactivity orchestrators (such as 
`assert_reactivity_upward` and `assert_reactivity_downward`) to chain value changes and verify 
cascade propagation seamlessly.
"""