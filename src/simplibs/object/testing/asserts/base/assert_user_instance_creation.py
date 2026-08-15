import pytest
from typing import Any, TYPE_CHECKING
from simplibs.exception.testing import maybe_subtest
from simplibs.sentinels import UNSET, UnsetType
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike
    from ...._core.protocols import SimpleMixinLike


# noinspection PyTypeChecker
def assert_user_instance_creation(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    mixins: tuple["SimpleMixinLike", ...] | UnsetType = UNSET,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """Assert that a user-configured instance of the target class can be instantiated cleanly.

    Validates that the target blueprint class instantiates successfully using optional,
    user-provided mixins or a standard vanilla configuration (without mixins). Unlike
    ``assert_instance_creation``, this function focuses purely on user-payload instantiation
    and does not run deep structural mixin attribute propagation checks.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        test_class: Target class blueprint under test.
        mixins: Optional tuple of user-defined mixin classes to attach during instantiation.
            If UNSET, instantiates the target without mixins.
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.

    Returns:
        The created user runtime instance.
    """
    subintro = "test_user_instance_creation::"

    # 1. Prepare mixins tuple payload
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}prepare_mixins",
        verbose=verbose,
    ):
        if mixins is UNSET:
            mixins_tuple = ()
        else:
            if not isinstance(mixins, tuple):
                pytest.fail("Parameter 'mixins' must be a tuple of mixin classes.")
            mixins_tuple = mixins

    # 2. Instantiate target class with user mixins (or vanilla default)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}create_instance",
        verbose=verbose,
    ):
        try:
            instance = test_class(mixins=mixins_tuple)
        except Exception as exc:
            pytest.fail(
                f"Unexpected error during user instance creation "
                f"with mixins={mixins_tuple}: {exc}"
            )

        assert instance is not None

    return instance


_DESIGN_NOTES = """
# assert_user_instance_creation (User Instance Instantiation Gate)

## Purpose
Provides a lightweight instantiation check for user-defined configuration scenarios. 
It verifies that a blueprint class can be instantiated with custom user mixins or in a 
vanilla (mixin-free) state without raising runtime instantiation errors.

## Execution Matrix & Sentinel Handling
1. **Mixin Normalization Gate:** Evaluates the `mixins` parameter. If left as `UNSET`, it defaults 
   to an empty tuple `()`. If passed explicitly, it validates that `mixins` is formatted as a `tuple`, 
   failing fast via `pytest.fail` if an invalid type is supplied.
2. **Instantiation Intercept:** Invokes `test_class(mixins=mixins_tuple)` within a protected context, 
   capturing unexpected runtime exceptions and emitting clear diagnostic logs.

## Architectural Distinction
- **`assert_instance_creation`**: Internal structural gate that forces `TestMixin` injection to test 
  deep feature propagation (slots, properties, methods, class attributes).
- **`assert_user_instance_creation`**: User-facing scenario gate focusing strictly on successful 
  instantiation under clean or custom runtime conditions. Returns the created instance for downstream checks.
"""