from unittest.mock import Mock
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.classmethod.validations.validate_method_is_defined import (
    validate_method_is_defined,
)


def test_validate_method_is_defined_pass() -> None:
    """Tests that a method defined directly in __dict__ passes validation."""

    class DummyOwner:
        @classmethod
        def target_method(cls):
            pass

    validate_method_is_defined(
        method_name="target_method",
        owner_class=DummyOwner,
        exception_info=("DummyOwner", "target_method", "Context"),
        expected_structure=("Blueprint",),
    )


def test_validate_method_is_defined_raises_error(subtests) -> None:
    """Tests that missing method in owner_class.__dict__ raises SimpleDefinitionError."""

    mock_owner = Mock()
    mock_owner.__dict__ = {}

    exception_info = ("MyClass", "missing_method", "TestContext")
    expected_structure = ("Expected structure line 1",)

    assert_exception_function(
        subtests,
        validate_method_is_defined,
        invalid_params=("missing_method", mock_owner, exception_info, expected_structure),
        exception_type=SimpleDefinitionError,
        error_name="METHOD LOGIC ERROR",
        label="_method",
        value="missing_method",
        expected="Method 'missing_method' must be declared in class 'MyClass'.",
        problem="Class 'MyClass' does not define this method.",
        context="TestContext",
        how_to_fix=(
            "Add 'missing_method' directly to the class definition.",
            "Decorate it with '@classmethod'.",
            "Ensure its parameters match the expected signature.",
            "Expected structure line 1",
        ),
        exception=AttributeError,
        verbose=False,
    )