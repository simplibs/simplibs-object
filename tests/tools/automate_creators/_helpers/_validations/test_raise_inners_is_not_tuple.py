from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators._helpers._validations.raise_inners_is_not_tuple import (
    raise_inners_is_not_tuple,
)


def test_raise_inners_is_not_tuple(subtests) -> None:
    """Tests that raise_inners_is_not_tuple raises SimpleRuntimeError."""

    class_name = "MyTestComposite"
    invalid_inners = [1, 2, 3]  # List místo tuple

    assert_exception_function(
        subtests,
        raise_inners_is_not_tuple,
        invalid_params=(class_name, invalid_inners),
        exception_type=SimpleRuntimeError,
        error_name="INVALID INNERS CONTAINER TYPE ERROR",
        label="inners_is_not_tuple",
        value="list",
        expected="A tuple containing SimpleConstant subclasses",
        problem=(
            "Provided 'inners' argument for composite class 'MyTestComposite' is not a tuple instance. "
            "Received type 'list' instead."
        ),
        context=(
            "Attempted to inspect child component blueprints for class 'MyTestComposite', "
            "but container validation failed."
        ),
        how_to_fix=(
            "Wrap inner component classes inside a tuple container, e.g. inners=(FirstInner, SecondInner).",
            "Do not pass lists, sets, or single untupled class references directly.",
        ),
        exception=TypeError,
        verbose=False,
    )