from typing import Any, TYPE_CHECKING
import pytest
from simplibs.exception.testing import maybe_subtest

# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike


# noinspection PyTypeChecker
def assert_decompose_value_method(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """Assert that the composite class method ``decompose_value`` correctly decomposes default values.

    Performs a deep validation check against composite object classes by extracting expected inner default
    values from metadata, invoking ``decompose_value(test_class.meta.default)`` to execute the underlying
    ``_decompose`` implementation at runtime, and verifying that the returned tuple matches the expected
    inner defaults.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        test_class: Composite class blueprint under test.
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.
    """
    subintro = "test_decompose_value::"

    # 1. Prepare expected decomposed values from inner defaults
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}prepare_expected",
        verbose=verbose,
    ):
        expected = tuple(inner.meta.default for inner in test_class.meta.inners)
        assert expected, f"Composite class '{test_class.__name__}' must define at least one inner component."

    # 2. Decompose default value (runtime test of underlying _decompose)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}decompose_value",
        verbose=verbose,
    ):
        try:
            decomposed = test_class.decompose_value(test_class.meta.default)
        except Exception as exc:
            pytest.fail(f"decompose_value raised an unexpected exception on '{test_class.__name__}': {exc}")

    # 3. Compare decomposed tuple with expected inner defaults
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}compare_with_expected",
        verbose=verbose,
    ):
        assert decomposed == expected, (
            f"Decomposed payload '{decomposed!r}' does not match expected inner defaults "
            f"'{expected!r}' for '{test_class.__name__}'."
        )


_DESIGN_NOTES = """
# assert_decompose_value_method (Composite Decomposition Logic Gate)

## Purpose
Validates the structural execution of the composite decomposition method (`decompose_value`) 
at the class blueprint level. It verifies that the underlying custom decomposition routine (`_decompose`) 
correctly breaks down the class-level default value into an explicit tuple of matching inner default values.

## Execution Pipeline Steps
1. **Expected Inner Sequence Resolution:** Extracts the expected tuple of inner default values 
   (`tuple(inner.meta.default for inner in test_class.meta.inners)`). Asserts that `test_class` 
   is a valid composite with defined inner metadata.
2. **Decomposition Execution Gate:** Invokes `test_class.decompose_value(test_class.meta.default)` inside 
   a protected interception block, verifying that `_decompose` executes without runtime exceptions.
3. **Decomposition Structural Matching:** Asserts that the returned tuple strictly matches the expected 
   inner defaults, ensuring bidirectional consistency between `_logic` and `_decompose`.

## Pipeline Lifecycle Role
Acts as the structural counterpart to `assert_calculate_value_method` within composite testing orchestrators 
(e.g., `assert_simple_object`). It guarantees that downward reactivity and value distribution pipelines 
can reliably decompose composite states into child component values.
"""