from types import SimpleNamespace
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_composite.vaidations.validate_composite_is_decomposeable import (
    validate_composite_is_decomposeable,
)


def test_validate_composite_is_decomposeable_success() -> None:
    """Tests that decomposable composite passes validation without error."""

    dummy_instance = SimpleNamespace(meta=SimpleNamespace(is_decomposeable=True))
    validate_composite_is_decomposeable(dummy_instance, "composite_node")


def test_validate_composite_is_decomposeable_raises_error(subtests) -> None:
    """Tests that non-decomposable composite raises SimpleRuntimeError with TypeError exception type."""

    class MyClass:
        meta = SimpleNamespace(is_decomposeable=False)

    dummy_instance = MyClass()

    assert_exception_function(
        subtests,
        validate_composite_is_decomposeable,
        invalid_params=(dummy_instance, "non_decomposable_node"),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY COMPOSITE UPDATE ERROR",
        label="composite decomposability",
        value="non_decomposable_node",
        expected="Composite nodes must support decomposition.",
        problem=(
            "Composite 'non_decomposable_node' is not decomposable.",
            "Inner values cannot be recalculated for this node.",
        ),
        context=(
            "Composite update attempted on instance 'MyClass'.",
            "The instance metadata reports that decomposition is disabled.",
        ),
        how_to_fix=(
            "Enable decomposition for this composite node in its metadata.",
            "If the node is meant to be constant, use with_constant instead.",
            "If decomposition is intentionally disabled, do not update this node as a composite.",
        ),
        exception=TypeError,
        verbose=False,
    )