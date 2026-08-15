from typing import Any, TYPE_CHECKING
import pytest
from simplibs.exception.testing import maybe_subtest

# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike


# noinspection PyTypeChecker
def assert_calculate_value_method(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """Assert that the composite class method ``calculate_value`` computes values matching default metadata.

    Performs a deep validation check against composite object classes by mapping inner default
    attributes to their corresponding kwargs payload, invoking ``calculate_value(**params)`` to execute
    the underlying ``_logic`` implementation at runtime, and verifying that the returned value strictly
    matches ``test_class.meta.default``.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        test_class: Composite class blueprint under test.
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.
    """
    subintro = "test_calculate_value::"

    # 1. Prepare parameter map from inner defaults
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}prepare_parameters",
        verbose=verbose,
    ):
        params = {
            inner.meta.name_snake: inner.meta.default
            for inner in test_class.meta.inners
        }
        assert params, f"Composite class '{test_class.__name__}' must define at least one inner component."

    # 2. Compute composite value (runtime test of underlying _logic)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}calculate_value",
        verbose=verbose,
    ):
        try:
            calculated = test_class.calculate_value(**params)
        except Exception as exc:
            pytest.fail(f"calculate_value raised an unexpected exception on '{test_class.__name__}': {exc}")

    # 3. Compare computed value with class default
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}compare_with_default",
        verbose=verbose,
    ):
        assert calculated == test_class.meta.default, (
            f"Calculated value '{calculated!r}' does not match class default "
            f"'{test_class.meta.default!r}' for '{test_class.__name__}'."
        )


_DESIGN_NOTES = """
# assert_calculate_value_method (Composite Calculation Logic Gate)

## Purpose
Validates the structural execution of the composite calculation method (`calculate_value`) 
at the class blueprint level. It verifies that the underlying custom logic routine (`_logic`) 
correctly transforms a dictionary of inner node default values into the declared composite class default.

## Execution Pipeline Steps
1. **Inner Defaults Extraction:** Constructs a parameter map (`params`) pairing each inner component's 
   snake_case name (`inner.meta.name_snake`) with its default value (`inner.meta.default`). Asserts 
   that `test_class` is a valid composite with non-empty inner metadata.
2. **Logic Execution Gate:** Executes `test_class.calculate_value(**params)` inside a protected context, 
   verifying that `_logic` executes smoothly without throwing unexpected errors.
3. **Class Default Consistency Check:** Asserts that the calculated output equals `test_class.meta.default`, 
   ensuring strict alignment between class metadata declarations and actual runtime logic execution.

## Pipeline Lifecycle Role
Acts as a specialized method-level assertion blade within composite testing runners (e.g., `assert_simple_object`). 
By testing composite logic resolution without requiring full runtime object instantiation, it isolates 
pure functional calculation errors early in the test suite.
"""