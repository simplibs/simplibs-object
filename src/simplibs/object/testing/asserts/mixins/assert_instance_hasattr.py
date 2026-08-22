from typing import Any
import pytest
from simplibs.exception.testing import maybe_subtest


# noinspection PyTypeChecker
def assert_instance_hasattr(
    subtests: Any,
    instance: Any,
    *,
    names: tuple[str, ...],
    kind: str,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """Assert generic attribute presence across runtime object instances.

    Validates that a sequence of attribute names exists on the target instance.
    This serves as a universal presence gate for verifying mixin-provided members
    such as instance slots, properties, methods, or class attributes.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        instance: Runtime object instance under test.
        names: Tuple of attribute name strings to verify on the instance.
        kind: Textual descriptor used in error messages (e.g., "slot", "attribute", "method").
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.
    """
    subintro = f"assert_instance_hasattr[{kind}]::"

    # 1. Validate input parameter types
    is_valid_input: bool = True
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_input",
        verbose=verbose,
    ):
        if not isinstance(names, tuple):
            is_valid_input = False
            pytest.fail(
                f"Parameter 'names' for kind '{kind}' must be a tuple of strings, "
                f"got: {names!r}"
            )

        for name in names:
            if not isinstance(name, str):
                is_valid_input = False
                pytest.fail(
                    f"{kind.capitalize()} name '{name!r}' is not a string. "
                    f"All {kind} names must be string identifiers."
                )

    # 1.1 Guard clause: Halt execution if parameter structure is invalid
    if not is_valid_input:
        return

    # 2. Validate attribute presence on target instance
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}check_presence",
        verbose=verbose,
    ):
        for name in names:
            if not hasattr(instance, name):
                pytest.fail(
                    f"Instance of class '{instance.__class__.__name__}' "
                    f"is missing expected {kind} '{name}'. "
                    f"Available attributes: {dir(instance)}"
                )


_DESIGN_NOTES = """
# assert_instance_hasattr (Generic Attribute Presence Gate)

## Purpose
Acts as a re-usable, parameterized structural assertion blade that verifies whether a set 
of named members exists on a target instance. It serves as the foundation for testing mixin 
propagation across slots, properties, methods, and class-level attributes.

## Verification Pipeline
1. **Input Schema & Guard Gate:** Validates that `names` is explicitly formatted as a `tuple[str, ...]`. 
   If non-string identifiers or incorrect containers are supplied, it reports a failure and aborts early 
   via a guard clause to prevent iterating invalid payloads downstream.
2. **Attribute Existence Intercept:** Iterates through `names` using `hasattr(instance, name)`. 
   If any expected attribute is absent, it raises a failure with diagnostic information, including 
   the class name and `dir(instance)` reflection dump.

## Pipeline Lifecycle Role
Functions as an atomic building block for higher-level mixin assertion modules 
(such as `assert_mixin_slots`, `assert_mixin_attributes`, or `assert_mixin_methods`). 
By abstracting parameter validation and error logging into a single generic function, 
it ensures consistent diagnostic output across all mixin structure tests.
"""