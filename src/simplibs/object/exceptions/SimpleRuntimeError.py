# Inners
from .base_exception import SimpleObjectError


class SimpleRuntimeError(SimpleObjectError):
    """
    Exception raised when provided data or operations fail logic, validation,
    or state rules during object execution.

    This error indicates that the class definition and instance setup are valid,
    but the runtime value or operation violates declared domain logic.
    """


_DESIGN_NOTES = """
# SimpleRuntimeError — Data & Operational Runtime Exception

## Purpose
`SimpleRuntimeError` represents errors caused by **runtime data or invalid user operations**.
It is raised when values passed to or operations performed on a `SimpleConstant` or
`SimpleObject` fail to satisfy domain rules.

This is the primary public-facing exception that end users will encounter when
interacting with instantiated Simple objects in application logic.

---

## When It Occurs
Typical situations include:

- type mismatches during property assignment or setter calls,
- custom validation failures inside `_validate` methods,
- normalization or conversion errors during data assignment,
- illegal state modifications (e.g., writing to a locked/immutable instance),
- calculation or decomposition failures during value propagation.

---

## Distinction from Other Exceptions
- `SimpleDefinitionError` → definition-time errors (invalid declarative blueprint)
- `SimpleInitializationError`   → instantiation-time errors (failed instance/mixin setup)
- `SimpleRuntimeError`    → **runtime data & logic errors** (invalid user input/state)
- `SimpleRuntimeError`    → test utility failures (fuzzing/filler issues)

---

## Notes
- Inherits from `SimpleObjectError`, so it can be caught via `except SimpleObjectError`.
- Main exception meant for application-level `try...except` blocks handling user data.
"""