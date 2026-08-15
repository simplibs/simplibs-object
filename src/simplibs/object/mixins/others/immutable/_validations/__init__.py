from .raise_with_changes_input_not_dict import raise_with_changes_input_not_dict


_DESIGN_NOTES = """
# Validations for ImmutableMethods

## Purpose
Provides structured raise functions used by the immutable update API
(`with_changes`). These validations ensure that:

- the input container for multiple updates is a dictionary,
- the immutable update pipeline receives well‑formed data.

## Components

| Component                               | Type     | Description                                      |
| :---------------------------------------| :--------| :----------------------------------------------- |
| `raise_with_changes_input_not_dict`     | Function | Ensures `changes_dict` is a dictionary.          |
"""
