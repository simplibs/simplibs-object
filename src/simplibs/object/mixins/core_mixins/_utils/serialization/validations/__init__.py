from .raise_unvalid_state_dict_input import raise_unvalid_state_dict_input
from .raise_unvalid_owner_class_mismatch_for_state_dict import raise_unvalid_owner_class_mismatch_for_state_dict
from .raise_missing_composite_key import raise_missing_composite_key
from .raise_invalid_composite_structure import raise_invalid_composite_structure
from .raise_missing_value_key import raise_missing_value_key


_DESIGN_NOTES = """
# Validations for Serialization (from_dict)

## Purpose
Provides structured raise functions used by the universal state reconstruction
pipeline (`from_dict`). These validations ensure that:

- the input container is a valid dictionary,
- the owner class matches the expected component type,
- composite branches contain all required nested keys,
- composite structures are valid dictionaries,
- atomic VALUE keys are present and correct.

## Components

| Component                                           | Type     | Description                                              |
| :-------------------------------------------------- | :------- | :------------------------------------------------------- |
| `raise_unvalid_state_dict_input`                    | Function | Ensures the input is a dictionary.                       |
| `raise_unvalid_owner_class_mismatch_for_state_dict` | Function | Validates owner class identity.                          |
| `raise_missing_composite_key`                       | Function | Raised when a composite branch key is missing.           |
| `raise_invalid_composite_structure`                 | Function | Raised when a composite branch is not a dictionary.      |
| `raise_missing_value_key`                           | Function | Raised when the final VALUE key is missing.              |
"""
