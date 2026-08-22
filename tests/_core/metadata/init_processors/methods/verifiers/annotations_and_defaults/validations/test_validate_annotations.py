from unittest.mock import Mock
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.annotations_and_defaults.validations.validate_annotations import (
    validate_annotations,
)


def test_validate_annotations_pass() -> None:
    """Tests that valid annotations or empty annotations pass validation."""

    mock_func = Mock()
    mock_func.__annotations__ = {"a": int, "b": str}
    mock_bound_method = Mock()
    mock_bound_method.__func__ = mock_func

    expected_annotations = {"a": int | str, "b": str}
    exception_info = ("TestClass", "test_method", "Context")
    expected_structure = ("Blueprint",)

    # Valid subset annotation passes
    validate_annotations(
        bound_method_annotations=expected_annotations,
        bound_method=mock_bound_method,
        exception_info=exception_info,
        expected_structure=expected_structure,
    )

    # Empty annotations pass immediately
    mock_func.__annotations__ = {}
    validate_annotations(
        bound_method_annotations=expected_annotations,
        bound_method=mock_bound_method,
        exception_info=exception_info,
        expected_structure=expected_structure,
    )


def test_validate_annotations_raises_error(subtests) -> None:
    """Tests that mismatching type annotations raise SimpleDefinitionError."""

    mock_func = Mock()
    mock_func.__annotations__ = {"a": str}
    mock_bound_method = Mock()
    mock_bound_method.__func__ = mock_func

    expected_annotations = {"a": int}
    exception_info = ("TestClass", "test_method", "TestContext")
    expected_structure = ("Expected structure line 1",)

    assert_exception_function(
        subtests,
        validate_annotations,
        invalid_params=(
            expected_annotations,
            mock_bound_method,
            exception_info,
            expected_structure,
        ),
        exception_type=SimpleDefinitionError,
        error_name="METHOD SIGNATURE ERROR",
        label="_annotation",
        expected="int",
        value="str",
        problem="Annotation for 'a' does not match expected types.",
        context="TestContext",
        how_to_fix=(
            "Change the annotation to match 'int'.",
            "The annotation must be the same type or a valid subset.",
            "You may also remove the annotation entirely; the framework will inject it automatically.",
            "Expected structure line 1",
        ),
        exception=TypeError,
        verbose=False,
    )