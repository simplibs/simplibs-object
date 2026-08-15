from typing import Any, TYPE_CHECKING
import pytest
from simplibs.exception.testing import maybe_subtest
# Outers
from ....mixins.base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleMixinType


def assert_mixin_inheritance(
    subtests: Any,
    mixin_class: "SimpleMixinType",
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """
    Validates that the provided mixin class inherits from SimpleMixin.

    This is the first structural gate for mixin testing.
    """

    subintro = "assert_mixin_inheritance::"

    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}inherits_from_simplemixin",
        verbose=verbose,
    ):
        # 1) Must be a class
        if not isinstance(mixin_class, type):
            pytest.fail(
                f"Provided mixin '{mixin_class!r}' is not a class. "
                f"Mixins must be class types inheriting from SimpleMixin."
            )

        # 2) Must inherit from SimpleMixin
        if not issubclass(mixin_class, SimpleMixin):
            pytest.fail(
                f"Mixin '{mixin_class.__name__}' does not inherit from SimpleMixin. "
                f"All mixins must subclass SimpleMixin to be compatible with the "
                f"Simplibs instance builder."
            )
