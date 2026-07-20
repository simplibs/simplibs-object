# Inners
from .SimpleError import SimpleError


class SimpleLogicError(SimpleError):
    """Exception for errors occurring during data manipulation (validation, creation, update)."""


_DESIGN_NOTES = """
# SimpleLogicError

## Purpose
This exception covers the entire data lifecycle inside `SimpleObject`. It is raised when the metadata is perfectly valid, but the specific data (values) provided do not comply with the defined rules.

## Logic
Inherits from `SimpleError`. It is used within `base_logic` mixins for:
- Type check failures (ValidateType).
- User validation failures (Validate).
- Normalization errors (Normalize).
- Issues during value decomposition or composition (Create/Update/Decompose).

## Notes
By separating this from `SimpleMetadataError`, we provide the user with a clear tool to distinguish between a poorly written class definition (code issue) and incorrectly provided data (runtime instance issue).
"""