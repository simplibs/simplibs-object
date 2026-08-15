from typing import Any, TYPE_CHECKING
import pytest
from simplibs.exception.testing import maybe_subtest
# Outers
from ....mixins.base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleMixinType


# noinspection PyTypeChecker
def assert_mixin_inheritance(
    subtests: Any,
    mixin_class: "SimpleMixinType",
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """Assert that the target mixin class satisfies the required SimpleMixin inheritance contract.

    Validates that the provided mixin target is a valid class type and explicitly derives
    from the framework base class ``SimpleMixin``. Serves as the primary structural gate
    for mixin validation pipelines.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        mixin_class: Target mixin class blueprint under test.
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.
    """
    subintro = "assert_mixin_inheritance::"

    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}inherits_from_simplemixin",
        verbose=verbose,
    ):
        # 1. Target must be a valid class type
        if not isinstance(mixin_class, type):
            pytest.fail(
                f"Provided mixin target '{mixin_class!r}' is not a class. "
                f"Mixins must be class types deriving from SimpleMixin."
            )

        # 2. Target must inherit from SimpleMixin
        if not issubclass(mixin_class, SimpleMixin):
            pytest.fail(
                f"Mixin class '{mixin_class.__name__}' does not inherit from SimpleMixin. "
                f"All mixin classes must subclass SimpleMixin to maintain compatibility "
                f"with the Simplibs instance builder."
            )


_DESIGN_NOTES = """
# assert_mixin_inheritance (Mixin Base Class Inheritance Gate)

## Purpose
Acts as the preliminary structural fail-fast boundary for verifying that a candidate mixin class 
conforms to the fundamental framework interface by deriving from `SimpleMixin`.

## Execution Pipeline Steps
1. **Class Type Gate:** Confirms that `mixin_class` is a valid Python type (`isinstance(mixin_class, type)`), 
   rejecting instantiated objects or invalid types before deep checks occur.
2. **Inheritance Contract Assertion:** Verifies `issubclass(mixin_class, SimpleMixin)`. If the target class 
   does not derive from `SimpleMixin`, it emits an explicit failure message highlighting incompatibility 
   with the dynamic instance builder.

## Pipeline Lifecycle Role
Functions as the entry gate in mixin test orchestrators (e.g., `assert_simple_mixin`). 
By asserting base inheritance upfront, it prevents subtle downstream runtime failures during dynamic 
instance creation and attribute binding stages.
"""