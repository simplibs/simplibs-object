from typing import Any, TYPE_CHECKING
import pytest
from simplibs.sentinels import UNSET
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

    expected: tuple[Any, ...] = ()

    # 1. Prepare expected decomposed values from inner defaults
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}prepare_expected",
        verbose=verbose,
    ):
        inners = getattr(getattr(test_class, "meta", None), "inners", ())
        expected = tuple(inner.meta.default for inner in inners)
        if not expected:
            pytest.fail(
                f"Composite class '{getattr(test_class, '__name__', str(test_class))}' "
                f"must define at least one inner component."
            )

    # 1.1 Guard clause: Halt execution if expected inner values could not be resolved
    if not expected:
        return

    decomposed: Any = UNSET

    # 2. Decompose default value (runtime test of underlying _decompose)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}decompose_value",
        verbose=verbose,
    ):
        try:
            default_val = getattr(getattr(test_class, "meta", None), "default", None)
            decomposed = test_class.decompose_value(default_val)
        except Exception as exc:
            pytest.fail(
                f"decompose_value raised an unexpected exception on "
                f"'{getattr(test_class, '__name__', str(test_class))}': {exc}"
            )

    # 2.1 Guard clause: Halt execution if decompose_value failed or did not resolve
    if decomposed is UNSET:
        return

    # 3. Compare decomposed tuple with expected inner defaults
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}compare_with_expected",
        verbose=verbose,
    ):
        if decomposed != expected:
            pytest.fail(
                f"Decomposed payload '{decomposed!r}' does not match expected inner defaults "
                f"'{expected!r}' for '{getattr(test_class, '__name__', str(test_class))}'."
            )


_DESIGN_NOTES = """
# assert_decompose_value_method (Composite Decomposition Logic Gate)

## Purpose
Validates the structural execution of the composite decomposition method (`decompose_value`) 
at the class blueprint level. It verifies that the underlying custom decomposition routine (`_decompose`) 
correctly breaks down the class-level default value into an explicit tuple of matching inner default values.

## Execution Pipeline Steps
1. **Expected Inner Sequence Resolution & Guard Gate:** Extracts the expected tuple of inner default values 
   (`tuple(inner.meta.default for inner in test_class.meta.inners)`). Asserts that `test_class` defines at least 
   one inner component and halts execution early via a guard clause if resolution fails.
2. **Decomposition Execution & Guard Gate:** Invokes `test_class.decompose_value(test_class.meta.default)` inside 
   a protected interception block, verifying that `_decompose` executes without runtime exceptions. If decomposition 
   fails, an early guard clause prevents comparison assertions against uncomputed state.
3. **Decomposition Structural Matching:** Asserts that the returned tuple strictly matches the expected 
   inner defaults, ensuring bidirectional consistency between `_logic` and `_decompose`.

## Pipeline Lifecycle Role
Acts as the structural counterpart to `assert_calculate_value_method` within composite testing orchestrators 
(e.g., `assert_simple_object`). It guarantees that downward reactivity and value distribution pipelines 
can reliably decompose composite states into child component values.
"""