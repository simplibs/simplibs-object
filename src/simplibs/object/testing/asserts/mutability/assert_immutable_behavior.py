from typing import Any
import pytest
from simplibs.exception.testing import maybe_subtest


# noinspection PyTypeChecker
def assert_immutable_behavior(
    subtests: Any,
    test_class: Any,
    *,
    new_value: Any,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """Assert that the target class correctly enforces immutability semantics.

    Validates that an instance instantiated with ``mutable=False`` rejects state updates via its value setter,
    raises an exception on modification attempts, and preserves both its python object identity and internal state.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        test_class: Target class blueprint under test.
        new_value: Candidate raw value to attempt applying via setter.
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.
    """
    subintro = "test_immutable_behavior::"

    # 1. Create immutable instance
    instance = None
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}create_immutable_instance",
        verbose=verbose,
    ):
        try:
            instance = test_class(mutable=False)
        except Exception as exc:
            pytest.fail(f"Failed to create immutable instance for '{test_class.__name__}': {exc}")

        assert instance is not None

    # 1.1 Guard clause: Halt execution if immutable instance creation failed
    if instance is None:
        return

    # 2. Capture original identity and value state
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}capture_original_state",
        verbose=verbose,
    ):
        original_id = id(instance)
        original_value = instance.value

    # 3. Attempt to apply new value (must raise an exception)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}setter_must_fail",
        verbose=verbose,
    ):
        try:
            instance.value = new_value
        except Exception:
            pass  # Expected behavior for immutable instances
        else:
            pytest.fail(
                f"Immutable instance of '{test_class.__name__}' allowed value update, "
                f"but immutable instances must reject setter calls."
            )

    # 4. Identity MUST remain unchanged
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}identity_preserved",
        verbose=verbose,
    ):
        if id(instance) != original_id:
            pytest.fail(
                f"Immutable instance of '{test_class.__name__}' changed python object identity "
                f"after failed value update attempt."
            )

    # 5. Value MUST remain unchanged
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}value_preserved",
        verbose=verbose,
    ):
        if instance.value != original_value:
            pytest.fail(
                f"Immutable instance of '{test_class.__name__}' changed its internal value "
                f"from {original_value!r} to {instance.value!r} after failed setter call."
            )


_DESIGN_NOTES = """
# assert_immutable_behavior (Immutability Enforcement Gate)

## Purpose
Verifies the runtime immutability contract when an object instance is initialized with `mutable=False`. 
It ensures that the property setter strictly guards internal state, throwing exceptions upon 
mutation attempts while guaranteeing full preservation of object identity and value consistency.

## Execution Pipeline Steps
1. **Immutable Instantiation & Guard Gate:** Instantiates `test_class(mutable=False)` inside a protected context. 
   Halts execution early via a guard clause if instance creation fails to prevent uninitialized attribute access.
2. **State Snapshot:** Captures the initial Python object ID (`id(instance)`) and value state (`instance.value`).
3. **Setter Interception Gate:** Attempts `instance.value = new_value`. Asserts that an exception is raised, 
   failing fast via `pytest.fail` if the assignment succeeds.
4. **Identity Preservation Assertion:** Asserts that object ID remains identical (`id(instance) == original_id`).
5. **Value State Preservation Assertion:** Asserts that internal value remains untouched (`instance.value == original_value`).

## Pipeline Lifecycle Role
Acts as a behavioral assertion blade in test orchestrators (such as `assert_simple_object`). 
It guarantees that framework instances configured for write-once or immutable runtime patterns 
strictly reject side-effect state mutations.
"""