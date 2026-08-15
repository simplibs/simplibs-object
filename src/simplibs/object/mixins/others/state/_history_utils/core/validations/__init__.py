from .raise_history_limit_not_positive_integer import raise_history_limit_not_positive_integer
from .raise_unvalide_snapshot_index import raise_unvalide_snapshot_index
from .raise_unvalide_snopshot_reference import raise_unvalide_snopshot_reference
from .raise_unvalide_snopshot_timestamp import raise_unvalide_snopshot_timestamp
from .raise_unvalide_timestamp import raise_unvalide_timestamp


_DESIGN_NOTES = """
# Validations for History Core

## Purpose
Provides structured raise functions used by the core history utilities
(`find_snapshot`, `set_history_limit`, timestamp navigation).  
These validations ensure that:

- snapshot indices are valid,
- timestamp inputs are correct,
- snapshot references are of supported types,
- timestamp lookups fail with clear diagnostics,
- history limits are positive integers.

## Components

| Component                                   | Type     | Description                                              |
| :------------------------------------------- | :------- | :------------------------------------------------------- |
| `raise_history_limit_not_positive_integer`   | Function | Ensures history limit is a positive integer.             |
| `raise_unvalide_snapshot_index`              | Function | Raised when snapshot index is out of range.              |
| `raise_unvalide_snopshot_reference`          | Function | Raised when snapshot reference is neither int nor datetime. |
| `raise_unvalide_snopshot_timestamp`          | Function | Raised when timestamp lookup fails.                      |
| `raise_unvalide_timestamp`                   | Function | Raised when timestamp input is not a datetime.           |
"""
