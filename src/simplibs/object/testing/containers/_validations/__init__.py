from .raise_inner_value_empty_path import raise_inner_value_empty_path
from .raise_inner_value_invalid_path_type import raise_inner_value_invalid_path_type


_DESIGN_NOTES = """
# Testing Containers Internal Validations

## Purpose
Provides internal validation functions and structured error triggers for container data structures.
Note: Since this folder starts with an underscore (`_`), its components remain strictly internal.

## Internal Components Registry

| Component                             | Type     | Description                                                               |
| :------------------------------------ | :------- | :------------------------------------------------------------------------ |
| `raise_inner_value_empty_path`        | Function | Raises a structured error when an `InnerValue` path resolves to empty.    |
| `raise_inner_value_invalid_path_type` | Function | Raises a structured error when an `InnerValue` path contains non-strings. |
"""