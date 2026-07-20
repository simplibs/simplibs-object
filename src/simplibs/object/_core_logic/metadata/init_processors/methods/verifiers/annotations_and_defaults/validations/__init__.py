from .validate_annotations import validate_annotations
from .validate_args_defaults import validate_args_defaults
from .validate_kwargs_defaults import validate_kwargs_defaults


_DESIGN_NOTES = """
# Annotations and Defaults Validation Sub-Package

## Purpose
Enforces rigid value and structural type synchronization boundaries directly against user-declared method signatures.

## Internal Components Registry

| Component                  | Type     | Description                                                                          |
| :------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `validate_annotations`     | Function | Confirms user parameter and return value type hints match framework schema expectations.|
| `validate_args_defaults`   | Function | Validates that explicit positional argument defaults strictly mirror internal schemas. |
| `validate_kwargs_defaults` | Function | Validates that explicit keyword-only argument defaults strictly mirror internal schemas.|
"""