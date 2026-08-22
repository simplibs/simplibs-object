from typing import Any, TYPE_CHECKING
from types import UnionType
from simplibs.sentinels import UNSET
# Inners
from .verifiers.classmethod import verify_classmethod
from .verifiers.params import verify_params
from .verifiers.calculation import verify_calculation
from .verifiers.annotations_and_defaults import verify_annotations_and_defaults
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleClassLike
    from ....protocols.methods import ClassMethodProtocol


def process_classmethod(
    method_name: str,
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    expected_args_defaults: tuple[Any, ...],
    expected_kwargs_defaults: dict[str, Any],
    expected_param_types: dict[str, type | UnionType],
    expected_return_type: type | UnionType,
    owner_class: "SimpleClassLike",
    test_value: tuple = (),
    return_calculated_value: bool = False,
) -> Any:
    """Runs full verification, normalization, and dry-run execution of a classmethod."""

    # 1. Resolve method descriptor and inheritance validation gate
    need_validations, bound_method = verify_classmethod(
        method_name=method_name,
        owner_class=owner_class,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count,
    )

    # 2. Pokud je metoda volitelná a není na třídě přítomna, vrací se UNSET bez spouštění dry-runu
    if bound_method is UNSET:
        return (UNSET, UNSET) if return_calculated_value else UNSET
    bound_method: "ClassMethodProtocol"

    # 3. Perform signature and annotation validations if needed
    if need_validations:

        # 3.1 Validate parameters
        verify_params(
            expected_params=expected_params,
            expected_args_params_count=expected_args_params_count,
            bound_method=bound_method,
        )

        # 3.2 Build unified annotation map
        bound_method_annotations = {
            **expected_param_types,
            "return": expected_return_type,
        }

        # 3.3 Validate developer overrides (annotations/defaults)
        func = bound_method.__func__
        if func.__annotations__ or func.__defaults__ or func.__kwdefaults__:
            verify_annotations_and_defaults(
                bound_method=bound_method,
                expected_params=expected_params,
                expected_args_params_count=expected_args_params_count,
                bound_method_annotations=bound_method_annotations,
                expected_args_defaults=expected_args_defaults,
                expected_kwargs_defaults=expected_kwargs_defaults,
            )

        # 3.4 Inject normalized defaults and annotations
        func.__defaults__ = expected_args_defaults
        func.__kwdefaults__ = expected_kwargs_defaults
        func.__annotations__ = bound_method_annotations

    # 4. Execute deterministic dry-run calculation
    calculated_value = verify_calculation(
        bound_method=bound_method,
        test_value=test_value,
        expected_return_type=expected_return_type,
        owner_class=owner_class,
    )

    # 5. Return method or (method, calculated_value)
    if return_calculated_value:
        return bound_method, calculated_value

    return bound_method



_DESIGN_NOTES = """
# process_classmethod

## Purpose
Coordinates the entire method validation pipeline:
- descriptor resolution,
- signature validation,
- annotation/default normalization,
- and deterministic dry-run execution.

## Behavior

### 1. Descriptor resolution
`verify_classmethod` determines whether the method is newly defined or inherited.
If inherited and already validated, the pipeline skips structural checks.

### 2. Structural validation
If validation is required:
- `verify_params` enforces parameter names and counts.
- A unified annotation map is constructed.
- If the developer declared annotations/defaults, `verify_annotations_and_defaults`
  validates them.

### 3. Signature normalization
The function frame is updated with:
- positional defaults,
- keyword-only defaults,
- normalized annotations.

### 4. Operational validation
`verify_calculation` performs a controlled dry-run:
- catches runtime exceptions,
- validates return type,
- validates `_decompose` structure.

### 5. Output
Returns either:
- the validated classmethod, or
- the classmethod and its dry-run result.
"""