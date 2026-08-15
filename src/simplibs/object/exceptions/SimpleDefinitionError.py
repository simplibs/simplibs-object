# Inners
from .base_exception import SimpleObjectError


class SimpleDefinitionError(SimpleObjectError):
    """
    Exception raised when a declarative Simple class contains invalid metadata
    or violates structural rules during class definition.

    This error indicates that the class itself is incorrectly written during code
    creation, even before any instance or runtime value is processed.
    """


_DESIGN_NOTES = """
# SimpleDefinitionError — Definition-Time Exception

## Purpose
`SimpleDefinitionError` is raised when the *declarative class definition* of a
`SimpleConstant` or `SimpleObject` is invalid. It signals that a developer
made a structural mistake in the class declaration, metadata configuration, or
blueprint definition.

The primary consumer of this exception is the **metadata engine and class builder
logic** executing at import or class-creation time.

---

## When It Occurs
Typical situations include:

- forbidden attributes defined on a class (e.g., `_default` defined on a composite),
- malformed, missing, or incompatible `_inners` declarations,
- invalid type annotations or type declarations in metadata,
- structural inconsistencies detected while parsing declarative blueprints.

These errors occur **during code writing and class declaration**, not during runtime
usage or data processing.

---

## Notes
- Inherits from `SimpleObjectError`, so it can be caught via `except SimpleObjectError`.
- Intended for developers defining Simple classes, surfacing errors at import/definition time.
"""