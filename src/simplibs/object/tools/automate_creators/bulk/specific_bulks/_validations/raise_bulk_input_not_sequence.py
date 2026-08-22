from typing import Any, NoReturn
from ......exceptions import SimpleRuntimeError


def raise_bulk_input_not_sequence(
    value: Any,
    runner_name: str,
    expected_items_description: str,
) -> None | NoReturn:
    """Raises SimpleRuntimeError when bulk input for dicts or table runners is not a list or tuple."""

    raise SimpleRuntimeError(
        error_name="INVALID BULK SEQUENCE INPUT ERROR",
        label="bulk_input_is_not_sequence",
        expected=f"A list or tuple of {expected_items_description}",
        value=type(value).__name__,
        problem=(
            f"Input provided to '{runner_name}' must be a sequence (list or tuple), "
            f"received type '{type(value).__name__}' instead."
        ),
        context=f"Attempted bulk creation using runner '{runner_name}'.",
        how_to_fix=(
            f"Wrap your definition elements in a list or tuple before passing them to '{runner_name}'.",
            f"Example: {runner_name}([element_1, element_2])",
        ),
        exception=TypeError,
    )