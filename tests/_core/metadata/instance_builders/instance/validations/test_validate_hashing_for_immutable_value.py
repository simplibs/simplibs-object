from unittest.mock import MagicMock
from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.validations.validate_hashing_for_immutable_value import (
    validate_hashing_for_immutable_value,
)


def test_validate_hashing_for_immutable_value_pass(sample_object_classes) -> None:
    """Tests that classes with hashable default values pass validation."""

    MyTestConstant, _ = sample_object_classes
    validate_hashing_for_immutable_value(MyTestConstant)


def test_validate_hashing_for_immutable_value_raises_error(subtests) -> None:
    """Tests that unhashable default values raise SimpleInitializationError."""

    mock_cls = MagicMock()
    mock_cls.meta.default = [1, 2, 3]
    mock_cls.meta.class_name = "MyUnhashableClass"

    assert_exception_function(
        subtests,
        validate_hashing_for_immutable_value,
        invalid_params=(mock_cls,),
        exception_type=SimpleInitializationError,
        error_name="UNHASHABLE DEFAULT",
        label="immutable_requires_hashable_default",
        value=[1, 2, 3],
        expected="Hashable default value",
        problem="Immutable instance 'MyUnhashableClass' cannot wrap a non-hashable default value.",
        context="create_instance(cls=MyUnhashableClass, mutable=False)",
        how_to_fix=(
            "Ensure that the default value is hashable.",
            "Examples of hashable values: int, float, str, tuple, frozenset.",
            "Examples of non-hashable values: list, dict, set, custom mutable objects.",
        ),
        exception=TypeError,
        verbose=False,
    )