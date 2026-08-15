from typing import Any, TYPE_CHECKING
import pytest
from simplibs.exception.testing import maybe_subtest
# Outers
from ....mixins.base_class import SimpleMixin
from ....SimpleConstant import SimpleConstant
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassType, SimpleMixinType


# noinspection PyTypeChecker
def assert_mixin_instance_creation(
    subtests: Any,
    mixin_class: "SimpleMixinType",
    test_class: "SimpleClassType",
    *,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """Assert that a target blueprint class can be instantiated with a specific mixin attached.

    Validates that both the base blueprint class and the mixin satisfy framework inheritance requirements,
    executes dynamic instantiation with ``mixins=(mixin_class,)``, and verifies that the mixin class
    is correctly injected into the resulting runtime class's Method Resolution Order (MRO).

    Args:
        subtests: The native pytest subtests fixture manager instance.
        mixin_class: Target mixin class blueprint under test.
        test_class: Base framework blueprint class used to bind the mixin.
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.

    Returns:
        The instantiated runtime object created with the mixin attached.
    """
    subintro = "assert_mixin_instance_creation::"

    # 1. Validate base test_class inheritance contract
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_test_class",
        verbose=verbose,
    ):
        test_class: type
        if not issubclass(test_class, SimpleConstant):
            pytest.fail(
                f"Test class '{test_class.__name__}' must inherit from "
                f"SimpleConstant or SimpleObject."
            )

    # 2. Validate mixin inheritance contract
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_mixin_class",
        verbose=verbose,
    ):
        mixin_class: type
        if not issubclass(mixin_class, SimpleMixin):
            pytest.fail(
                f"Mixin '{mixin_class.__name__}' does not inherit from SimpleMixin."
            )

    # 3. Instantiate target class with mixin injection
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}create_instance",
        verbose=verbose,
    ):
        try:
            instance = test_class(mixins=(mixin_class,))
        except Exception as exc:
            pytest.fail(
                f"Failed to create instance of '{test_class.__name__}' "
                f"with mixin '{mixin_class.__name__}': {exc}"
            )

        if instance is None:
            pytest.fail(
                f"Instance creation returned None for class '{test_class.__name__}' "
                f"with mixin '{mixin_class.__name__}'."
            )

    # 4. Verify mixin presence in runtime MRO
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}mixin_in_mro",
        verbose=verbose,
    ):
        if mixin_class not in instance.__class__.__mro__:
            pytest.fail(
                f"Mixin '{mixin_class.__name__}' is not present in the MRO of the "
                f"created instance. Instance class MRO: {instance.__class__.__mro__}"
            )

    return instance


_DESIGN_NOTES = """
# assert_mixin_instance_creation (Dynamic Mixin Instantiation Gate)

## Purpose
Verifies the integration between the framework's dynamic instance builder and a given mixin class. 
It ensures that a base blueprint class (`SimpleObject` or `SimpleConstant`) can be instantiated with 
a candidate mixin, and that the mixin class properly binds into the runtime class hierarchy.

## Verification Pipeline
1. **Blueprint Validation:** Confirms `test_class` derives from `SimpleConstant` (which covers `SimpleObject` as well).
2. **Mixin Contract Validation:** Confirms `mixin_class` derives from `SimpleMixin`.
3. **Dynamic Instantiation:** Invokes `test_class(mixins=(mixin_class,))` within a protected context, 
   ensuring zero runtime construction errors.
4. **MRO Inspection Gate:** Inspects `instance.__class__.__mro__` to guarantee that `mixin_class` is explicitly 
   present in the runtime class inheritance chain.

## Pipeline Lifecycle Role
Serves as the structural setup and verification gate within mixin testing runners (e.g., `assert_simple_mixin`). 
By returning the created `instance`, it enables downstream mixin assertions to inspect specific slots, properties, 
and methods on a live, mixin-enriched runtime object.
"""