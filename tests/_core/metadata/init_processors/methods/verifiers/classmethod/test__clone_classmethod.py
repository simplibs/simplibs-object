from typing import TYPE_CHECKING, Callable
from types import FunctionType
# Annotations
if TYPE_CHECKING:
    from ......protocols.methods import ClassMethodProtocol


def _clone_classmethod(
    cm: "ClassMethodProtocol",
) -> classmethod:
    """Creates a fully isolated clone of a classmethod."""

    # 1. Extract underlying function
    func = cm.__func__

    # 2. Rebuild a new function object
    new_func: Callable = FunctionType(
        func.__code__,
        func.__globals__,
        name=func.__name__,
        argdefs=func.__defaults__,
        closure=func.__closure__,
    )

    # 3. Copy annotations
    new_func.__annotations__ = dict(func.__annotations__)

    # 4. Copy keyword-only defaults
    new_func.__kwdefaults__ = (
        dict(func.__kwdefaults__) if func.__kwdefaults__ else None
    )

    # 5. Copy custom attributes
    if func.__dict__:
        new_func.__dict__.update(func.__dict__)

    # 6. Wrap into a fresh classmethod descriptor
    return classmethod(new_func)



_DESIGN_NOTES = """
# _clone_classmethod

## Purpose
Creates a fully isolated clone of a classmethod.  
Used when a subclass inherits a method but needs its own independent copy so that
metadata injection does not modify the parent class.

## Why cloning is required
Python's `classmethod` wraps a single underlying function object.  
If a subclass modifies that function (annotations, defaults, attributes), the
changes propagate upward to the parent class.  
This breaks isolation and causes shared‑state bugs.

Cloning prevents this by reconstructing a new function object.

## How cloning works
1. **Extract the underlying function**  
   `cm.__func__` gives the raw function object.

2. **Rebuild a new function**  
   A new `FunctionType` is created using:
   - bytecode (`__code__`)
   - globals (`__globals__`)
   - name (`__name__`)
   - defaults (`__defaults__`)
   - closure (`__closure__`)

3. **Copy metadata safely**
   - annotations → copied into a new dict  
   - keyword defaults → copied or set to None  
   - custom attributes → copied via `.update()`

4. **Wrap back into classmethod**
   The new function is wrapped in a fresh `classmethod` descriptor.

## Notes
This helper is used only inside the method‑verification pipeline.  
It is intentionally minimal and does not perform validation.
"""