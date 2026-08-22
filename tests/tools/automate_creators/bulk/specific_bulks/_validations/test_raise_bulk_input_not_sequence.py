from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators.bulk.specific_bulks._validations.raise_bulk_input_not_sequence import (
    raise_bulk_input_not_sequence,
)


def test_raise_bulk_input_not_sequence(subtests) -> None:
    """Tests that raise_bulk_input_not_sequence raises SimpleRuntimeError for non-sequence inputs."""
    invalid_input = "not_a_sequence"
    runner_name = "create_simple_object_bulk_from_dicts"
    expected_items = "dictionaries"

    assert_exception_function(
        subtests,
        raise_bulk_input_not_sequence,
        invalid_params=(invalid_input, runner_name, expected_items),
        exception_type=SimpleRuntimeError,
        error_name="INVALID BULK SEQUENCE INPUT ERROR",
        label="bulk_input_is_not_sequence",
        value="str",
        expected="A list or tuple of dictionaries",
        problem=(
            "Input provided to 'create_simple_object_bulk_from_dicts' must be a sequence (list or tuple), "
            "received type 'str' instead."
        ),
        context="Attempted bulk creation using runner 'create_simple_object_bulk_from_dicts'.",
        how_to_fix=(
            "Wrap your definition elements in a list or tuple before passing them to 'create_simple_object_bulk_from_dicts'.",
            "Example: create_simple_object_bulk_from_dicts([element_1, element_2])",
        ),
        exception=TypeError,
        verbose=False,
    )