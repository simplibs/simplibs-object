from .raise_type_error import raise_type_error
from .raise_missing_value_error import raise_missing_value_error
from .raise_unexpected_validation_error import raise_unexpected_validation_error
from .raise_validation_error import raise_validation_error

_DESIGN_NOTES = """
# Constant Validation Errors Sub-Package

## Purpose
Contains all structured error generators used during constant validation and
normalization. These functions ensure consistent, user-facing diagnostics across
the entire validation pipeline.

## Internal Components Registry

| Component                           | Type     | Description                                                                |
| :---------------------------------- | :------- | :------------------------------------------------------------------------- |
| `raise_type_error`                  | Function | Raised when a value does not match the declared type.                      |
| `raise_missing_value_error`         | Function | Raised when None is provided where a valid value is required.              |
| `raise_unexpected_validation_error` | Function | Wraps unexpected exceptions from user-defined validation logic.            |
| `raise_validation_error`            | Function | Raised when `_validate` returns False.                                     |
"""
