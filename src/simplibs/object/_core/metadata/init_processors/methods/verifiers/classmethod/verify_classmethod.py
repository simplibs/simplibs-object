from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from .._exceptions_helpers import (
    exception_info_for_classmethod,
    expected_structure_for_classmethod,
)
# Inners
from ._clone_classmethod import _clone_classmethod
from .validations import (
    validate_method_is_defined,
    validate_method_is_callable,
    validate_method_is_classmethod,
)
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.methods import ClassMethodProtocol


def verify_classmethod(
    method_name: str,
    owner_class: "SimpleClassLike",
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
) -> tuple[bool, "classmethod | ClassMethodProtocol"]:
    """Verifies classmethod existence, inheritance boundaries, and isolation rules."""
    from .......SimpleObject import SimpleObject

    # 1. Prepare raw layout metadata
    raw_method = owner_class.__dict__.get(method_name, UNSET)
    bound_method = getattr(owner_class, method_name)

    # 2. Early exit for default/undefined _decompose
    if (
        method_name == "_decompose"
        and raw_method is UNSET
        and getattr(bound_method, "__func__", None) is SimpleObject._decompose.__func__
    ):
        return False, UNSET

    # 3. Check if the attribute is a classmethod descriptor
    if (
        raw_method is not UNSET
        and isinstance(raw_method, classmethod)
    ) or raw_method is UNSET:
        bound_method: ClassMethodProtocol

        # 3.1 Local override → validate
        if raw_method is not UNSET:
            return True, bound_method

        # 3.2 Inherited _validate → never re-validate
        if method_name == "_validate":
            return False, bound_method

        # 3.3 Check direct inheritance from SimpleObject
        is_direct_descendant = SimpleObject in owner_class.__bases__

        # 3.4 Deep subclass → clone if structural keys exist
        if not is_direct_descendant:
            need_validations = bool(owner_class.__dict__.keys() & {"_inners", "_type", "_logic"})
            output = _clone_classmethod(bound_method) if need_validations else bound_method
            return need_validations, output

    # 4. Build exception metadata
    exception_info = exception_info_for_classmethod(bound_method)
    expected_structure = expected_structure_for_classmethod(
        bound_method,
        expected_params,
        expected_args_params_count,
    )

    # 5. Run micro-validations
    validate_method_is_defined(method_name, owner_class, exception_info, expected_structure)
    validate_method_is_callable(raw_method, exception_info, expected_structure)
    validate_method_is_classmethod(raw_method, exception_info, expected_structure)
    return False, UNSET



_DESIGN_NOTES = """
# verify_classmethod

## Purpose
Acts as the central gatekeeper for classmethod validation (`_validate`, `_logic`, `_decompose`).
It determines whether a method should be validated, cloned, inherited, or rejected before dry-run execution.

## Step-by-step behavior

### 1. Namespace extraction
Two views of the method are captured:
- `raw_method` → local class namespace (`owner_class.__dict__`). Checked to determine local override.
- `bound_method` → resolved through full MRO (`getattr(owner_class, method_name)`). Unset fallback is intentionally omitted because all supported lifecycle methods (_validate, _logic, _decompose) are guaranteed to exist in MRO contracts.

### 2. Early-exit for default `_decompose`
Decomposition is optional. `SimpleObject` defines a default fallback `@classmethod def _decompose` that returns `UNSET`.
To avoid triggering unnecessary validation pipelines or dry-run evaluation failures on nested subclasses:
- If `method_name == "_decompose"` AND `raw_method is UNSET` (not overridden locally) AND `bound_method.__func__` points to `SimpleObject._decompose.__func__` (memory identity check via `is`), the process immediately short-circuits returning `(False, UNSET)`.
- If an intermediate ancestor defines a custom `_decompose`, memory pointers won't match `SimpleObject._decompose.__func__`, allowing proper inheritance and re-validation down the hierarchy.

### 3. Descriptor routing & isolation rules
If the method is a valid `classmethod` or inherited descriptor:
- **Local override (`raw_method is not UNSET`)**: Always requires full signature and dry-run validation (`return True, bound_method`).
- **Inherited `_validate`**: Validation rules belong to the declaring class; inherited `_validate` methods are never re-validated (`return False, bound_method`).
- **Deep subclassing (non-direct descendants)**: Inherited methods are cloned using `_clone_classmethod` if the subclass alters structural keys (`_inners`, `_type`, `_logic`) to isolate method state and prevent side-effects.

### 4. Exception metadata & Micro-validations
If a method fails structural descriptor checks (e.g. defined as standard function instead of `@classmethod`), descriptive diagnostics are compiled (`exception_info`, `expected_structure`) and dispatched to targeted micro-validators:
- `validate_method_is_defined`
- `validate_method_is_callable`
- `validate_method_is_classmethod`

## Notes
- `is` comparison on `.__func__` operates at CPython pointer level (O(1) efficiency) without requiring expensive MRO traversals.
- Early exit guarantees that unhandled `_decompose` hooks will not leak `UNSET` outcomes into dry-run validators.
"""