from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.testing.containers._validations.raise_inner_value_empty_path import (
    raise_inner_value_empty_path,
)


def test_raise_inner_value_empty_path(subtests) -> None:
    """Tests that raise_inner_value_empty_path raises SimpleRuntimeError."""

    assert_exception_function(
        subtests,
        raise_inner_value_empty_path,
        invalid_params=(),
        exception_type=SimpleRuntimeError,
        error_name="INNER VALUE EMPTY PATH ERROR",
        label="path",
        expected="A non-empty string path (e.g. 'address.city') or iterable of path parts.",
        problem=(
            "Provided path evaluated to an empty sequence.",
            "An InnerValue requires a valid target property path to perform navigation.",
        ),
        context="Attempted to construct an InnerValue container with an empty string or empty sequence.",
        how_to_fix=(
            "Ensure the path parameter is a dot-separated string like 'age' or 'address.city'.",
            "Do not pass empty strings '' or empty tuples/lists () as the path.",
        ),
        exception=ValueError,
        verbose=False,
    )