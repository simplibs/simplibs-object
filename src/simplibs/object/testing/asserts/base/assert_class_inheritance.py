from typing import Any, TYPE_CHECKING
from simplibs.exception.testing import maybe_subtest
# Outers
from ....SimpleConstant import SimpleConstant
from ....SimpleObject import SimpleObject
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike


# noinspection PyTypeChecker
def assert_class_inheritance(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """Assert that the target class satisfies the required Simple object inheritance contract.

    Validates that the provided blueprint class correctly inherits from either
    ``SimpleObject`` or ``SimpleConstant`` based on its structural definition.

    Logic:
        - If the class defines the ``_inners`` attribute (even via inheritance),
          it must derive from ``SimpleObject``.
        - Otherwise, it must derive from ``SimpleConstant``.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        test_class: Target class blueprint under test.
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.
    """
    subintro = "test_class_inheritance::"

    # 1. Validate inheritance for atomic constant classes
    if not hasattr(test_class, "_inners"):
        with maybe_subtest(
            subtests,
            name=f"{intro}{subintro}test_inheritance_simple_constant",
            verbose=verbose,
        ):
            assert issubclass(test_class, SimpleConstant)

    # 2. Validate inheritance for composite object classes
    else:
        with maybe_subtest(
            subtests,
            name=f"{intro}{subintro}test_inheritance_simple_object",
            verbose=verbose,
        ):
            assert issubclass(test_class, SimpleObject)


_DESIGN_NOTES = """
# assert_class_inheritance (Structural Blueprint Inheritance Gate)

## Purpose
Acts as the entry-level structural gate for verifying that a class under test is a valid 
blueprint derived from the core framework base classes (`SimpleObject` or `SimpleConstant`).

## Structural Routing Logic
The assertion inspects the target class signature to route verification dynamically:
1. **Atomic Constants (`not hasattr(test_class, "_inners")`):** Verifies that classes 
   representing single atomic value containers derive directly from `SimpleConstant`.
2. **Composite Objects (`hasattr(test_class, "_inners")`):** Verifies that classes 
   defining composite node hierarchies derive directly from `SimpleObject`.

## Pipeline Lifecycle Role
This shallow structural check serves as a Fail-Fast boundary in orchestrators such as 
`assert_simple_object`. By ensuring the class properly inherits from the framework's 
base primitives before executing deeper instance creation or reactivity tests, it prevents 
misleading runtime errors caused by malformed or non-framework class inputs.
"""