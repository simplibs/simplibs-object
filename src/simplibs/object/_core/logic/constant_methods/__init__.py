from .validate_type import validate_type
from .validate import validate
from .normalize import normalize
from .bool_or_raise_validate_error import bool_or_raise_validate_error

_DESIGN_NOTES = """
# Constant Methods Sub-Package

## Purpose
Provides the core functional building blocks used by `SimpleConstant` and
`SimpleObject` classes to perform type validation, user-defined validation,
normalization, and structured error handling.

## Internal Components Registry

| Component                        | Type     | Description                                                                |
| :------------------------------- | :------- | :------------------------------------------------------------------------- |
| `validate_type`                  | Function | Performs deterministic type validation based on metadata.                  |
| `validate`                       | Function | Executes the full validation pipeline (type + user-defined).               |
| `normalize`                      | Function | Normalizes values, handles None rules, and enforces default semantics.     |
| `bool_or_raise_validate_error`   | Function | Helper for user-defined `_validate` methods to raise structured errors.    |
"""
