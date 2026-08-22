from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.testing.containers._validations.raise_inner_value_invalid_path_type import (
    raise_inner_value_invalid_path_type,
)


def test_raise_inner_value_invalid_path_type(subtests) -> None:
    """Tests that raise_inner_value_invalid_path_type raises SimpleRuntimeError."""

    invalid_path = ("address", 123)
    invalid_part = 123

    assert_exception_function(
        subtests,
        raise_inner_value_invalid_path_type,
        invalid_params=(invalid_path, invalid_part),
        exception_type=SimpleRuntimeError,
        error_name="INNER VALUE INVALID PATH TYPE ERROR",
        label="path",
        expected="A string or sequence of string attribute identifiers.",
        value="int",
        problem=(
            "One or more segments in the provided path are not string identifiers.",
            "Encountered invalid path segment: 123 of type 'int'.",
        ),
        context=(
            "Full path argument provided: ('address', 123)",
            "Invalid segment item: 123",
        ),
        how_to_fix=(
            "Ensure all path segments are valid string property names.",
            "If using a tuple/list path, pass tuples of strings like ('address', 'city', 'zip').",
            "Do not pass integers, objects, or non-string types within the path sequence.",
        ),
        exception=TypeError,
        verbose=False,
    )