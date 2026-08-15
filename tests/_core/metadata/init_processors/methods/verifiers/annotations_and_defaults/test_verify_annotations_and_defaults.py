from typing import Any, TYPE_CHECKING
# Outers
from .._exceptions_helpers import (
    exception_info_for_classmethod,
    expected_structure_for_classmethod,
)
# Inners
from .validations import (
    validate_annotations,
    validate_args_defaults,
    validate_kwargs_defaults,
)
# Annotations
if TYPE_CHECKING:
    from ......protocols.methods import ClassMethodProtocol


def verify_annotations_and_defaults(
    bound_method: "ClassMethodProtocol",
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    bound_method_annotations: dict[str, Any],
    expected_args_defaults: tuple[Any, ...],
    expected_kwargs_defaults: dict[str, Any],
) -> None:
    """Verifies type annotations and default values for classmethod signatures."""

    # 1. Build exception metadata
    exception_info = exception_info_for_classmethod(bound_method)
    expected_structure = expected_structure_for_classmethod(
        bound_method,
        expected_params,
        expected_args_params_count,
    )

    func = bound_method.__func__

    # 2. Validate annotations
    if func.__annotations__:
        validate_annotations(
            bound_method_annotations,
            bound_method,
            exception_info,
            expected_structure,
        )

    # 3. Validate positional defaults
    if func.__defaults__:
        validate_args_defaults(
            expected_args_defaults,
            expected_params,
            bound_method,
            exception_info,
            expected_structure,
        )

    # 4. Validate keyword-only defaults
    if func.__kwdefaults__:
        validate_kwargs_defaults(
            expected_kwargs_defaults,
            bound_method,
            exception_info,
            expected_structure,
        )


_DESIGN_NOTES = """
# verify_annotations_and_defaults

## Purpose
Ensures that user-declared type annotations and default values match the
framework’s deterministic metadata configuration.  
Annotations may be omitted, but if present, they must be correct.  
Defaults may be omitted, but if present, they must match `_inners`.

## Step-by-step behavior

### 1. Exception metadata
The function prepares:
- `exception_info` — (class_name, method_name, context)
- `expected_structure` — blueprint of the correct method signature

Both are passed to all validators.

### 2. Annotation validation
If the method defines annotations, `validate_annotations` checks that each
annotation is a subset of the expected type set.

### 3. Positional defaults
If positional defaults exist (`__defaults__`), `validate_args_defaults` ensures
they match the deterministic defaults defined in `_inners`.

### 4. Keyword-only defaults
If keyword-only defaults exist (`__kwdefaults__`), `validate_kwargs_defaults`
ensures they match the expected mapping.

## Notes
This orchestrator is called after `verify_classmethod` and `verify_params`.
It completes the full signature validation pipeline.
"""