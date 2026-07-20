from typing import TYPE_CHECKING
from collections.abc import Callable
from types import FunctionType
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol


def _clone_classmethod(
    cm: "ClassMethodProtocol"
) -> classmethod:
    """Accepts a classmethod object and returns a brand new, fully isolated classmethod descriptor instance.

    Deeply decouples the underlying function by reconstructing its native frame elements,
    preventing side effects and reference bleeding across inheritance boundaries.
    """

    # 1. Extract the underlying function object from the classmethod descriptor wrapper
    func = cm.__func__

    # 2. Reconstruct a brand new function object by passing raw execution components
    new_func: Callable = FunctionType(
        func.__code__,
        func.__globals__,
        name=func.__name__,
        argdefs=func.__defaults__,
        closure=func.__closure__,
    )

    # 3. Transfer and isolate the parameter and return type annotations
    new_func.__annotations__ = dict(func.__annotations__)

    # 4. Transfer and isolate keyword-only argument default maps
    if func.__kwdefaults__:
        new_func.__kwdefaults__ = dict(func.__kwdefaults__)
    else:
        new_func.__kwdefaults__ = None

    # 5. Transfer custom runtime state attributes bound to the function namespace
    if func.__dict__:
        new_func.__dict__.update(func.__dict__)

    # 6. Return a fresh classmethod descriptor wrapping the newly isolated function
    return classmethod(new_func)


_DESIGN_NOTES = """
# _clone_classmethod

## Core Architectural Role
The `_clone_classmethod` utility handles low-level descriptor isolation. When a framework orchestrator (such as `verify_classmethod`) intercepts developer-defined lifecycle hooks (`_logic`, `_decompose`, etc.) within deep inheritance configurations, modifying or injecting metadata directly into the existing method references creates shared-state bugs. Because Python classmethods are bound descriptors, modifying a method on a child class would mutate the shared parent class's underlying function reference. This function acts as a circuit breaker by deep-cloning the method down to its low-level bytecode components, ensuring that any downstream framework adjustments remain entirely isolated to the target class context.

## Detailed Breakdown of the Reconstructive Cloning Process

### Phase 1: Bypassing the Descriptor Wrapper
A `classmethod` object in Python acts as a structural descriptor wrapper. To manipulate the execution frame, the function must peel back this wrapper using `cm.__func__`. This extracts the raw, un-bound `FunctionType` instance containing the actual logic compiled by the Python runtime.

### Phase 2: Primitive Function Reconstruction
To create a true architectural clone rather than a shallow reference copy, the utility builds a brand new function object from scratch using the low-level type constructor `types.FunctionType`. It manually passes the structural execution pillars:
* `func.__code__`: The immutable compiled bytecode object (instructions, variable names, and constants).
* `func.__globals__`: A reference to the dictionary containing the global variables of the module where the function was defined.
* `func.__name__`: The exact literal identifier string of the method.
* `func.__defaults__` (`argdefs`): The ordered evaluation tuple containing default values for standard positional and keyword parameters.
* `func.__closure__`: The tuple of cells containing bindings for the function's free variables, ensuring inner closures maintain integrity.

### Phase 3: Metadata Isolation & Dictionary Unlinking
Once the new function object is instantiated, it still lacks supplementary runtime dictionaries. Because dictionaries are mutable reference types, simply assigning them would link the old and new functions together. The function prevents this via explicit isolation copying:
1. **Annotations (`__annotations__`)**: Clones the type hinting maps into a fresh `dict` wrapper, ensuring the framework's static validation engines can query parameter schemas safely without modifying parent types.
2. **Keyword Defaults (`__kwdefaults__`)**: Checks for keyword-only parameters. If present, it creates a decoupled copy; if absent, it strictly sets the namespace pointer to `None` to conform to internal bytecode specifications.
3. **Custom Attributes (`__dict__`)**: Copies any dynamic runtime attributes attached to the method object using `.update()`, preserving custom user-defined decorator tags or monitoring hooks.

### Phase 4: Re-Wrapping the Descriptor
Finally, the newly created and fully isolated `new_func` is wrapped back into a fresh instance of Python's built-in `classmethod` descriptor wrapper. When this cloned descriptor is attached back to the class layout or invoked via Python's descriptor protocol (`__get__`), it behaves identically to the original method, but remains safely decoupled from all ancestors.
"""