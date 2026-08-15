from .raise_unvalide_history_import_file import raise_unvalide_history_import_file
from .raise_unvalide_owner_class_mismatch import raise_unvalide_owner_class_mismatch


_DESIGN_NOTES = """
# Validations for History Transfer

## Purpose
Provides structured raise functions used by the history import/export pipeline.
These validations ensure that:

- the imported history container is a valid dictionary,
- the owner class of the imported history matches the current instance.

These checks protect the integrity of history restoration and prevent
cross‑component contamination.

## Components

| Component                               | Type     | Description                                          |
| :---------------------------------------| :--------| :--------------------------------------------------- |
| `raise_unvalide_history_import_file`    | Function | Ensures the import container is a dictionary.        |
| `raise_unvalide_owner_class_mismatch`   | Function | Validates owner class identity during import.        |
"""
