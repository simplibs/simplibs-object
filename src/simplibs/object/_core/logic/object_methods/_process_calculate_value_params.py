from typing import Any, TYPE_CHECKING
# Inners
from .validations import (
    raise_too_many_positional_args_error,
    raise_duplicate_argument_error,
    raise_unknown_parameter_error,
)
# Annotations
if TYPE_CHECKING:
    from ...protocols.classes import SimpleObjectProtocol


def _process_calculate_value_params(
    cls: "SimpleObjectProtocol",
    *args,
    **kwargs,
) -> dict[str, Any]:
    """Processes positional and keyword parameters for composite value calculation."""

    # 1. Load inner element mapping
    inners_map = cls.meta.inners_map

    # 2. Guard clause — too many positional arguments
    if len(args) > len(inners_map):
        raise_too_many_positional_args_error(
            cls,
            given_count=len(args),
            allowed_count=len(inners_map),
        )

    # 3. Prepare data structures
    clean_kwargs: dict[str, Any] = {}
    args_iter = iter(args)

    # 4. Iterate through inner elements in order
    for param_name, inner_cls in inners_map.items():

        # 4.1 Try to consume positional argument
        try:
            value = next(args_iter)

            # If the same parameter also appears in kwargs → error
            if param_name in kwargs:
                raise_duplicate_argument_error(cls, param_name)

        # 4.2 No positional argument → fall back to kwargs
        except StopIteration:
            value = kwargs.pop(param_name, None)

        # 4.3 Load default if no value provided
        if value is None:
            value = inner_cls.meta.default

        # 4.4 Validate provided value
        else:
            inner_cls.validate(value)

        # 4.5 Store validated value
        clean_kwargs[param_name] = value

    # 5. Detect unknown keyword parameters
    if kwargs:
        raise_unknown_parameter_error(cls, list(kwargs.keys()))

    # 6. Return processed parameter dictionary
    return clean_kwargs


_DESIGN_NOTES = """
# _process_calculate_value_params

## Purpose
Processes positional and keyword arguments passed to `calculate_value` and maps
them to the inner elements of a composite object. Ensures strict, predictable
parameter handling and provides structured error reporting for all invalid cases.

---

## Behavior

### 1. Positional Argument Count
- Ensures that the number of positional arguments does not exceed the number of
  inner elements.
- Violations trigger `raise_too_many_positional_args_error`.

### 2. Duplicate Parameter Detection
- Detects when a parameter is supplied both positionally and as a keyword.
- Violations trigger `raise_duplicate_argument_error`.

### 3. Unknown Keyword Arguments
- After processing all known parameters, any remaining keyword arguments are
  considered invalid.
- Violations trigger `raise_unknown_parameter_error`.

### 4. Default Handling
- If a parameter is not provided, its default value is loaded from metadata.

### 5. Validation
- All provided values are validated using the inner element’s validation pipeline.

---

## Notes
- This function is used internally by `calculate_value`.
- It ensures that composite objects behave predictably and consistently.
- All diagnostics are delegated to structured `SimpleRuntimeError` helpers.
- The public-facing documentation belongs to `SimpleObject.calculate_value`.
"""