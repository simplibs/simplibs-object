from typing import Any
import pytest
from simplibs.exception.testing import maybe_subtest
# Outers
from ..base.assert_value_change import assert_value_change


# noinspection PyTypeChecker
def assert_mutable_behavior(
    subtests: Any,
    test_class: Any,
    *,
    new_value: Any,
    verbose: bool = True,
    verbose_value_change: bool = True,
    intro: str = "",
) -> None:
    """Assert that the target class correctly enforces mutable state semantics.

    Validates that an instance instantiated with ``mutable=True`` permits in-place state updates via
    ``assert_value_change`` while strictly maintaining its Python object identity (memory address).

    Args:
        subtests: The native pytest subtests fixture manager instance.
        test_class: Target class blueprint under test.
        new_value: Candidate raw value to apply to the mutable instance.
        verbose: Enables isolated pytest subtests reporting for this wrapper.
        verbose_value_change: Enables isolated subtests reporting inside the nested ``assert_value_change``.
        intro: Optional prefix string added to the generated subtest identity name.
    """
    subintro = "test_mutable_behavior::"

    # 1. Create mutable instance
    instance = None
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}create_mutable_instance",
        verbose=verbose,
    ):
        try:
            instance = test_class(mutable=True)
        except Exception as exc:
            pytest.fail(f"Failed to create mutable instance for '{test_class.__name__}': {exc}")

        assert instance is not None

    # 1.1 Guard clause: Halt execution if mutable instance creation failed
    if instance is None:
        return

    # 2. Capture original Python object identity
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}capture_original_identity",
        verbose=verbose,
    ):
        original_id = id(instance)

    # 3. Apply new value via shared value change assertion
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}apply_value",
        verbose=verbose,
    ):
        assert_value_change(
            subtests,
            instance,
            value=new_value,
            verbose=verbose_value_change and verbose,
            intro=intro,
        )

    # 4. Object identity MUST remain unchanged
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}identity_preserved",
        verbose=verbose,
    ):
        if id(instance) != original_id:
            pytest.fail(
                f"Mutable instance of '{test_class.__name__}' changed identity after value update, "
                f"but mutable instances must preserve identity."
            )


_DESIGN_NOTES = """
# assert_mutable_behavior (Mutable State Behavior Gate)

## Purpose
Verifies the runtime mutability contract when an object instance is initialized with `mutable=True`. 
It guarantees that in-place state updates succeed via property setters while preserving the exact 
Python object identity (`id(instance)`), ensuring no hidden instance re-creation occurs.

## Execution Pipeline Steps
1. **Mutable Instantiation & Guard Gate:** Instantiates `test_class(mutable=True)` within a protected 
   interception block. Halts execution early via a guard clause if instance creation fails to prevent 
   uninitialized attribute access in downstream steps.
2. **Identity Snapshot:** Captures the memory address / identity of the newly created instance (`id(instance)`).
3. **In-Place Mutation Intercept:** Delegates value validation, setter invocation, and state update 
   verification to `assert_value_change`.
4. **Identity Preservation Assertion:** Asserts that the memory address remains strictly unchanged 
   (`id(instance) == original_id`) after the mutation pass completes.

## Pipeline Lifecycle Role
Acts as a behavioral assertion blade within test runners like `assert_simple_object`. 
By pairing with `assert_immutable_behavior`, it guarantees full symmetry and contract compliance 
across both mutable and immutable execution modes of the framework.
"""