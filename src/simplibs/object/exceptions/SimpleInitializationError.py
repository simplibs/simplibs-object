# Inners
from .base_exception import SimpleObjectError


class SimpleInitializationError(SimpleObjectError):
    """
    Exception raised during the instantiation of a Simple instance or mixin.

    This error indicates that the class metadata is valid, but the runtime
    creation/initialization failed due to missing required parameters, mixin
    incompatibilities, or structural setup failures.
    """


_DESIGN_NOTES = """
# SimpleInitializationError — Instantiation-Time Exception

## Purpose
`SimpleInitializationError` is raised exclusively during the initialization phase of a
`SimpleConstant`, `SimpleObject`, or associated mixin. It signals that:

- the class definition and metadata are fully valid,
- but the **runtime instantiation process** failed.

The primary consumer of this exception is the **instance initialization pipeline,
`__init__` builders, and mixin composition checks**.

---

## When It Occurs
Typical situations include:

- missing or incompatible positional/keyword arguments passed during `__init__`,
- mixin dependency conflicts or failed mixin contract verifications,
- structural initialization failures when assembling composite inner instances,
- attempts to instantiate an abstract or improperly configured mixin structure.

---

## Notes
- Inherits from `SimpleObjectError`, so it can be caught via `except SimpleObjectError`.
- Clearly separates instantiation/setup problems from definition errors and runtime data errors.
"""