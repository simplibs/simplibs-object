from typing import Any
import pytest
from simplibs.exception.testing import maybe_subtest
# Outers
from ..base.assert_value_change import assert_value_change


# noinspection PyTypeChecker
def assert_reactivity_downward(
    subtests: Any,
    instance: Any,
    *,
    new_value: Any,
    verbose: bool = True,
    verbose_value_change: bool = True,
    intro: str = "",
) -> None:
    """Assert downward reactivity across composite object instances.

    Validates that updating the root value of a composite instance automatically decomposes and
    propagates updated states down to all nested inner components according to the defined
    decomposition contract.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        instance: Root composite object instance under test.
        new_value: Candidate raw composite value to apply to the root instance.
        verbose: Enables isolated pytest subtests reporting for this wrapper.
        verbose_value_change: Enables isolated subtests reporting inside the nested ``assert_value_change``.
        intro: Optional prefix string added to the generated subtest identity name.
    """
    subintro = "test_reactivity_downward::"

    # 1. Target instance must be a composite (non-constant) object
    meta = instance.meta
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}is_composite",
        verbose=verbose,
    ):
        if getattr(meta, "is_constant", False):
            pytest.fail(
                f"Cannot test downward reactivity on atomic constant '{meta.class_name}', "
                f"because constants do not contain inner components."
            )

    # 1.1 Guard clause: Halt execution if instance is an atomic constant
    if getattr(meta, "is_constant", False):
        return

    # 2. Target composite must explicitly support decomposition
    is_decomposeable = getattr(meta, "is_decomposeable", False)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}supports_decompose",
        verbose=verbose,
    ):
        if not is_decomposeable:
            pytest.fail(
                f"Composite '{meta.class_name}' does not define a decomposition method; "
                f"downward reactivity cannot be verified."
            )

    # 2.1 Guard clause: Halt execution if composite does not support decomposition
    if not is_decomposeable:
        return

    # 3. Apply composite value change to root via shared assertion
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}apply_composite_value",
        verbose=verbose,
    ):
        assert_value_change(
            subtests,
            instance,
            value=new_value,
            verbose=verbose_value_change and verbose,
            intro=intro,
        )

    # 4. Compute expected decomposed inner values
    expected_values = None
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}compute_expected",
        verbose=verbose,
    ):
        try:
            expected_values = instance.decompose_value(new_value)
        except Exception as exc:
            pytest.fail(
                f"decompose_value raised an unexpected exception on '{meta.class_name}': {exc}"
            )

    # 4.1 Guard clause: Halt execution if decomposition calculation failed
    if expected_values is None:
        return

    # 5. Compare inner property attributes against expected decomposed values
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}compare_inners",
        verbose=verbose,
    ):
        inners = tuple(getattr(meta, "inners", ()))
        if len(expected_values) != len(inners):
            pytest.fail(
                f"decompose_value returned {len(expected_values)} values for '{meta.class_name}', "
                f"but the class has {len(inners)} inner components."
            )
        for inner, expected_value in zip(inners, expected_values):
            name_snake = inner.meta.name_snake
            actual_value = getattr(instance, name_snake)

            if actual_value != expected_value:
                pytest.fail(
                    f"Downward reactivity state mismatch for inner property '{name_snake}': "
                    f"expected {expected_value!r}, got {actual_value!r}."
                )


_DESIGN_NOTES = """
# assert_reactivity_downward (Downward State Cascade Gate)

## Purpose
Verifies downward reactivity within composite object hierarchies. It ensures that when a new root
composite value is assigned, the underlying framework decomposes the root payload into individual
component state values and propagates them down to each nested inner object.

## Execution Pipeline Steps
1. **Composite Type & Guard Gate:** Verifies that the target instance is a composite node (`not meta.is_constant`).
   Aborts early via a guard clause if the target is an atomic constant.
2. **Decomposition Contract & Guard Gate:** Confirms the composite class defines decomposition capabilities
   (`meta.is_decomposeable`). Halts execution if decomposition is unsupported.
3. **Root Mutation Intercept:** Mutates the root composite value using `assert_value_change`, which handles pre-validation
   and in-place assignment.
4. **Decomposition Calculation & Guard Gate:** Calls `instance.decompose_value(new_value)` to derive the expected
   sequence of child values, guarded by a fail-fast exit if calculation raises an exception.
5. **Inner State Reconciliation:** Iterates over `meta.inners`, fetching the runtime inner attribute via
   `getattr(instance, name_snake)`, and asserts that every child state strictly reflects the decomposed expected value.

## Pipeline Lifecycle Role
Serves as one of the twin reactivity validation blades in the framework. While `assert_reactivity_upward`
verifies state aggregation from leaf to root, `assert_reactivity_downward` ensures top-down state distribution
and decomposition remain fully synchronized across the entire object tree.
## Length Check
`zip` stops at the shorter side, so a `decompose_value` that returns too few (or too many) values would
leave the remaining inner components unchecked and the test green. The two lengths are compared first.
"""
