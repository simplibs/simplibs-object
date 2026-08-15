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

    # 1. Prepare raw layout metadata
    raw_method = owner_class.__dict__.get(method_name, UNSET)
    bound_method = getattr(owner_class, method_name)

    # 2. Check if the attribute is a classmethod descriptor
    if isinstance(bound_method, classmethod):
        bound_method: ClassMethodProtocol

        # 2.1 Local override → validate
        if raw_method:
            return True, bound_method

        # 2.2 Inherited _validate → never re-validate
        if method_name == "_validate":
            return False, bound_method

        # 2.3 Check direct inheritance from SimpleObject
        from .......SimpleObject import SimpleObject
        is_direct_descendant = SimpleObject in owner_class.__bases__

        # 2.4 Deep subclass → clone if structural keys exist
        if not is_direct_descendant:
            need_validations = bool(owner_class.__dict__.keys() & {"_inners", "_type", "_logic"})
            output = _clone_classmethod(bound_method) if need_validations else bound_method
            return need_validations, output

        # 2.5 Optional _decompose hook missing → skip
        if method_name == "_decompose":
            return False, UNSET

    # 3. Build exception metadata
    exception_info = exception_info_for_classmethod(bound_method)
    expected_structure = expected_structure_for_classmethod(
        bound_method,
        expected_params,
        expected_args_params_count,
    )

    # 4. Run micro-validations
    validate_method_is_defined(
        method_name,
        owner_class,
        exception_info,
        expected_structure
    )

    validate_method_is_callable(
        raw_method,
        exception_info,
        expected_structure
    )

    validate_method_is_classmethod(
        raw_method,
        exception_info,
        expected_structure
    )

    return False, UNSET



_DESIGN_NOTES = """
# verify_classmethod

## Purpose
Acts as the central gatekeeper for classmethod validation.  
It determines whether a method should be validated, cloned, inherited, or rejected.

## Step-by-step behavior

### 1. Namespace extraction
Two views of the method are captured:
- `raw_method` → local class namespace (`__dict__`)
- `bound_method` → resolved through full MRO

### 2. Descriptor routing
If the method is a `classmethod`, the function evaluates:

- **Local override** → validate  
- **Inherited `_validate`** → skip  
- **Deep subclass** → clone if structural keys exist  
- **Missing `_decompose`** → skip gracefully  

### 3. Exception metadata
If the method is not a classmethod, the function prepares:
- `exception_info` → (class_name, method_name, context)
- `expected_structure` → blueprint of the correct method signature

### 4. Micro-validations
Three validators diagnose:
- missing definition  
- non-callable attribute  
- missing `@classmethod` decorator  

Each validator receives both metadata tuples.

## Notes
This function is used for all three method types:
- `_validate`
- `_logic`
- `_decompose`

It is the first step in the method‑processing pipeline.
"""