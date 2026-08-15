from typing import Any, TYPE_CHECKING
from simplibs.exception.testing import maybe_subtest
# Outers
from ....SimpleConstant import SimpleConstant
from ....SimpleObject import SimpleObject
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike

def assert_class_inheritance(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """
    Validates that the target class is a valid SimpleObject/SimpleConstant blueprint.

    Logic:
        - If the class defines `_inners` (even via inheritance), it must inherit from SimpleObject.
        - Otherwise, it must inherit from SimpleConstant.

    This is the shallow structural gate used by assert_simple_object.
    """

    subintro = "test_class_inheritance::"

    # 1. Validace předka konstanty
    if not hasattr(test_class, "_inners"):
        with maybe_subtest(
            subtests,
            name=f"{intro}{subintro}test_inheritance_simple_constant",
            verbose=verbose,
        ):
            # noinspection PyTypeChecker
            assert issubclass(test_class, SimpleConstant)

    # 2. Validace předka kompozitní třídy
    else:
        with maybe_subtest(
            subtests,
            name=f"{intro}{subintro}test_inheritance_simple_object",
            verbose=verbose,
        ):
            # noinspection PyTypeChecker
            assert issubclass(test_class, SimpleObject)
