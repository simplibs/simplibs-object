from .raise_immutability_batch_constant_not_found import raise_immutability_batch_constant_not_found
from .raise_immutability_constants_changes_not_tuple import raise_immutability_constants_changes_not_tuple
from .validate_inner_tuple_has_length_two import validate_inner_tuple_has_length_two
from .validate_inner_tuple_is_tuple import validate_inner_tuple_is_tuple
from .validate_inner_tuple_name_is_str import validate_inner_tuple_name_is_str


_DESIGN_NOTES = """
# Validations for with_constants

## Purpose
Provides validation and raise functions used by the batch constant update
pipeline (`with_constants`). These checks ensure correct tuple structure and
validate constant existence.

## Components

| Component                                      | Type     | Description                                      |
| :--------------------------------------------- | :------- | :----------------------------------------------- |
| `raise_immutability_batch_constant_not_found`  | Function | Raised when a batch constant is missing.         |
| `raise_immutability_constants_changes_not_tuple` | Function | Ensures the batch input is a tuple.              |
| `validate_inner_tuple_is_tuple`                | Function | Ensures each change item is a tuple.             |
| `validate_inner_tuple_has_length_two`          | Function | Ensures each change item has two elements.       |
| `validate_inner_tuple_name_is_str`             | Function | Ensures the first element of each tuple is str.  |
"""
