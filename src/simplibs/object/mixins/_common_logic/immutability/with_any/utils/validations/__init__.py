from .raise_with_any_unknown_name import raise_with_any_unknown_name
from .raise_split_changes_unknown_name import raise_split_changes_unknown_name


_DESIGN_NOTES = """
# Validations for with_any (utils)

## Purpose
Provides structured raise functions used by the low‑level dispatch logic of
`with_any`, specifically inside `process_single_change` and `split_changes`.  
These validations ensure that:

- the update name corresponds to an existing constant or composite node,
- malformed or unknown update names are rejected early,
- the immutability pipeline remains deterministic and safe.

## Components

| Component                             | Type     | Description                                               |
| :-------------------------------------| :--------| :-------------------------------------------------------- |
| `raise_with_any_unknown_name`         | Function | Raised when update name is not constant/composite (single change). |
| `raise_split_changes_unknown_name`    | Function | Raised when update name is not constant/composite (classification). |
"""
