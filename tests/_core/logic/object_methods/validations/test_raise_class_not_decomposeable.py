import pytest
from unittest.mock import Mock

from simplibs.sentinels import UNSET
from simplibs.exception.testing import (
    assert_exception_function,
)
from simplibs.object._core.logic.object_methods.validations.raise_class_not_decomposeable import (
    raise_class_not_decomposeable,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "has_decompose, offenders_data, expected_reason, expected_offenders_str",
    [
        # Scénář 1: Třída sama nemá decompose metodu
        (
            False,
            [],
            "Composite 'TestClass' does not define a method for decomposing values.",
            "None",
        ),
        # Scénář 2: Třída má decompose metodu, ale vnitřní prvky nejsou decomposable
        (
            True,
            [("InnerA", False, False), ("InnerB", False, False)],
            "Composite 'TestClass' defines a decomposition method, but some of its inner composite elements cannot be decomposed.",
            "InnerA, InnerB",
        ),
        # Scénář 3: Třída má decompose metodu a vnitřní konstanta (is_constant=True) se ignoruje
        (
            True,
            [("ConstantInner", True, False), ("NonDecomposableInner", False, False)],
            "Composite 'TestClass' defines a decomposition method, but some of its inner composite elements cannot be decomposed.",
            "NonDecomposableInner",
        ),
    ],
)
def test_raise_class_not_decomposeable(
    subtests,
    has_decompose: bool,
    offenders_data: list[tuple[str, bool, bool]],
    expected_reason: str,
    expected_offenders_str: str,
) -> None:
    """Test that attempting direct value assignment on non-decomposeable composites raises SimpleRuntimeError."""

    dummy_meta = Mock()
    dummy_meta.class_name = "TestClass"
    dummy_meta.decompose = Mock() if has_decompose else UNSET

    inners = []
    for class_name, is_constant, is_decomposeable in offenders_data:
        inner_mock = Mock()
        inner_mock.meta.class_name = class_name
        inner_mock.meta.is_constant = is_constant
        inner_mock.meta.is_decomposeable = is_decomposeable
        inners.append(inner_mock)

    dummy_meta.inners = inners

    assert_exception_function(
        subtests,
        raise_class_not_decomposeable,

        invalid_params=(dummy_meta,),
        exception_type=SimpleRuntimeError,

        error_name="COMPOSITE VALUE ASSIGNMENT ERROR",
        label="composite_not_decomposeable",
        expected="A composite that supports direct value assignment",
        value="TestClass",
        problem="Direct assignment of a value to composite 'TestClass' is not possible. ",
        context=(
            f"{expected_reason}",
            f"Inner non-decomposable elements: {expected_offenders_str}.",
        ),
        how_to_fix=(
            "This composite cannot accept a value directly because it cannot decompose "
            "the provided value into its inner elements.",
            "You can still modify the composite by changing its constant inner values, "
            "which will update the composite from the bottom up.",
            "If the composite is intentionally non-decomposable, this behavior is expected.",
        ),
        exception=TypeError,

        verbose=False,
    )