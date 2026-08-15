from .raise_class_not_decomposeable import raise_class_not_decomposeable
from .raise_duplicate_argument_error import raise_duplicate_argument_error
from .raise_too_many_positional_args_error import raise_too_many_positional_args_error
from .raise_unknown_parameter_error import raise_unknown_parameter_error

_DESIGN_NOTES = """
# Object Method Validation Errors Sub-Package

## Purpose
Contains all structured error generators used during composite value calculation
and decomposition. These functions ensure consistent, user-facing diagnostics
across the entire object-method pipeline.

## Internal Components Registry

| Component                               | Type     | Description                                                                |
| :-------------------------------------- | :------- | :------------------------------------------------------------------------- |
| `raise_class_not_decomposeable`         | Function | Raised when a composite does not support decomposition.                    |
| `raise_duplicate_argument_error`        | Function | Raised when a parameter is passed both positionally and by keyword.        |
| `raise_too_many_positional_args_error`  | Function | Raised when too many positional arguments are supplied.                    |
| `raise_unknown_parameter_error`         | Function | Raised when unknown keyword arguments are supplied.                        |
"""
