from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators._helpers._validations.raise_inner_is_not_simple_constant_subclass import (
    raise_inner_is_not_simple_constant_subclass,
)


def test_raise_inner_is_not_simple_constant_subclass(subtests) -> None:
    """Tests that raise_inner_is_not_simple_constant_subclass raises SimpleRuntimeError."""

    class_name = "MyTestComposite"
    invalid_inner = int

    assert_exception_function(
        subtests,
        raise_inner_is_not_simple_constant_subclass,
        invalid_params=(class_name, invalid_inner),
        exception_type=SimpleRuntimeError,
        error_name="INVALID INNER COMPONENT CLASS ERROR",
        label="inner_is_not_simple_constant",
        value="int",
        expected="A class deriving from SimpleConstant / SimpleObject base",
        problem=(
            "Item 'int' inside 'inners' tuple for class 'MyTestComposite' "
            "is not a valid Simple framework class subclass."
        ),
        context=(
            "Inspecting child element blueprints to construct parameter dictionary "
            "for composite class 'MyTestComposite'."
        ),
        how_to_fix=(
            "Ensure every item inside the 'inners' tuple inherits from SimpleConstant or SimpleObject.",
            "Do not pass primitive types (like int, str) or instantiated objects in the 'inners' tuple.",
            "Pass blueprint classes, e.g. inners=(MyConstantClass, MySubObjectClass).",
        ),
        exception=TypeError,
        verbose=False,
    )