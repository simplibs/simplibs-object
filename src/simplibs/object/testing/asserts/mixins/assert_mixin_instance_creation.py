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
    mutable: bool = True,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """Assert that a target blueprint class can be instantiated with a specific mixin attached.

    Validates that both the base blueprint class and the mixin satisfy framework inheritance requirements,
    executes dynamic instantiation with ``mixins=(mixin_class,)``, and verifies that the mixin's members
    are correctly injected into the resulting runtime instance/class namespace.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        mixin_class: Target mixin class blueprint under test.
        mutable: Defines whether the underlying instance should be created in mutable mode (default True).
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
    instance = None
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}create_instance",
        verbose=verbose,
    ):
        try:
            instance = test_class(mixins=(mixin_class,), mutable=mutable)
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

    # 3.1 Guard clause: If instance creation failed, abort downstream member verification
    if instance is None:
        return None

    # 4. Verify mixin members presence in runtime instance namespace
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}mixin_members_injected",
        verbose=verbose,
    ):
        # Ignorujeme atributy definované na samotném SimpleMixin a object,
        # protože slouží jako kompilační direktivy a nevkládají se do cílového class_dict.
        base_mixin_attrs = set(dir(SimpleMixin))

        # Testujeme pouze atributy specificky deklarované na testovaném mixinu
        mixin_members = {
            name for name in dir(mixin_class)
            if not (name.startswith("__") and name.endswith("__"))
               and name not in base_mixin_attrs
        }

        missing_members = [
            name for name in mixin_members
            if not hasattr(instance, name)
        ]

        if missing_members:
            pytest.fail(
                f"Mixin '{mixin_class.__name__}' members {missing_members} "
                f"were not found on the created instance of '{test_class.__name__}'."
            )

    return instance


_DESIGN_NOTES = """
# assert_mixin_instance_creation (Dynamic Mixin Instantiation Gate)

## Purpose
Verifies the integration between the framework's dynamic instance builder and a given mixin class. 
It ensures that a base blueprint class (`SimpleObject` or `SimpleConstant`) can be instantiated with 
a candidate mixin, and that the mixin members properly bind into the runtime class namespace.

## Verification Pipeline
1. **Blueprint Validation:** Confirms `test_class` derives from `SimpleConstant` (which covers `SimpleObject` as well).
2. **Mixin Contract Validation:** Confirms `mixin_class` derives from `SimpleMixin`.
3. **Dynamic Instantiation & Guard Gate:** Invokes `test_class(mixins=(mixin_class,))` within a protected context, 
   ensuring zero runtime construction errors. Aborts early via a guard clause if creation fails.
4. **Member Injection Gate:** Verifies that all non-dunder attributes, properties, and methods defined on `mixin_class` 
   are present on the created runtime instance namespace.

## Pipeline Lifecycle Role
Serves as the structural setup and verification gate within mixin testing runners (e.g., `assert_simple_mixin`). 
By returning the created `instance`, it enables downstream mixin assertions to inspect specific slots, properties, 
and methods on a live, mixin-enriched runtime object.
"""