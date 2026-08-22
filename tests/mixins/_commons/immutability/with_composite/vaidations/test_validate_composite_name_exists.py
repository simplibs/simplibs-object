from types import SimpleNamespace
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_composite.vaidations.validate_composite_name_exists import (
    validate_composite_name_exists,
)


def test_validate_composite_name_exists_success() -> None:
    """Tests that valid composite node name passes validation without error."""

    dummy_instance = SimpleNamespace(meta=SimpleNamespace(node_names_set={"node_a", "node_b"}))
    validate_composite_name_exists(dummy_instance, "node_a")


def test_validate_composite_name_exists_raises_error(subtests) -> None:
    """Tests that non-existent composite node name raises SimpleRuntimeError with KeyError exception type."""

    class MyClass:
        meta = SimpleNamespace(node_names_set={"node_a", "node_b"})

    dummy_instance = MyClass()

    assert_exception_function(
        subtests,
        validate_composite_name_exists,
        invalid_params=(dummy_instance, "unknown_node"),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY COMPOSITE UPDATE ERROR",
        label="composite name",
        value="unknown_node",
        expected="Name must refer to a valid composite node.",
        problem=(
            "Composite 'unknown_node' does not exist in the instance metadata.",
            "Immutable composite update cannot be applied.",
        ),
        context=(
            "Composite update attempted on instance 'MyClass'.",
        ),
        how_to_fix=(
            "Ensure that the provided name refers to a composite node.",
            "Check the instance metadata for available composite names.",
            "If the name refers to a constant, use with_constant instead.",
        ),
        exception=KeyError,
        verbose=False,
    )