from typing import Any, TYPE_CHECKING
import pytest
from simplibs.exception.testing import maybe_subtest
# Outers
from ...containers.InnerValue import InnerValue
from ..base.assert_value_change import assert_value_change
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleInstanceLike


# noinspection PyTypeChecker
def assert_reactivity_upward(
    subtests: Any,
    instance: "SimpleInstanceLike",
    *,
    new_value: InnerValue,
    verbose: bool = True,
    verbose_value_change: bool = True,
    intro: str = "",
) -> None:
    """Assert upward reactivity across composite object instances.

    Validates that updating a nested inner component's state (targeted via an ``InnerValue`` payload)
    automatically triggers a recalculation cascade upwards, updating the root composite instance's value.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        instance: Root composite object instance under test.
        new_value: An ``InnerValue`` container referencing the target inner attribute and its new value.
        verbose: Enables isolated pytest subtests reporting for this wrapper.
        verbose_value_change: Enables isolated subtests reporting inside the nested ``assert_value_change``.
        intro: Optional prefix string added to the generated subtest identity name.
    """
    subintro = "test_reactivity_upward::"

    # 1. Capture initial composite root value
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}capture_original_composite",
        verbose=verbose,
    ):
        original_composite_value = instance.value

    # 2. Input parameter MUST be an InnerValue container
    is_inner_value = isinstance(new_value, InnerValue)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_input_type",
        verbose=verbose,
    ):
        if not is_inner_value:
            pytest.fail(
                "Upward reactivity assertion requires an InnerValue container; direct values cannot be used."
            )

    # 2.1 Guard clause: Halt execution if input is not an InnerValue container
    if not is_inner_value:
        return

    # 3. Apply inner value change via shared value change assertion
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}apply_inner_value",
        verbose=verbose,
    ):
        assert_value_change(
            subtests,
            instance,
            value=new_value,
            verbose=verbose_value_change and verbose,
            intro=intro,
        )

    # 4. Composite root value MUST have changed
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}composite_changed",
        verbose=verbose,
    ):
        if instance.value == original_composite_value:
            pytest.fail(
                f"Composite root value on '{instance.meta.class_name}' remained unchanged "
                f"({original_composite_value!r}) after inner component update — upward reactivity is broken."
            )


_DESIGN_NOTES = """
# assert_reactivity_upward (Upward State Cascade Gate)

## Purpose
Verifies bottom-up upward reactivity within composite object hierarchies. It guarantees that when 
a leaf or nested child node's state mutates, the runtime owner notifications (`_recalculate_self`) 
recompute the parent composite state, propagating updated values up to the root instance.

## Execution Pipeline Steps
1. **Initial State Snapshot:** Captures the root instance's current composite value (`instance.value`).
2. **Type & Guard Gate:** Validates that `new_value` is explicitly provided as an `InnerValue` container, 
   halting execution early via a guard clause if a raw non-inner value is passed.
3. **Inner Node Mutation:** Passes the `InnerValue` payload to `assert_value_change`. The base assertion resolves 
   the inner target attribute, pre-validates the candidate inner state, and executes the setter on the child object.
4. **Root State Mutation Assertion:** Asserts that `instance.value != original_composite_value`, confirming that 
   the bottom-up recalculation cascade successfully updated the top-level parent state.

## Pipeline Lifecycle Role
Functions as the upward reactivity validation blade in test runners (e.g., `assert_simple_object`). 
Complements `assert_reactivity_downward` to guarantee full, bidirectional state consistency across the entire 
reactive object graph.
"""