from .raise_immutability_constant_not_found import raise_immutability_constant_not_found


_DESIGN_NOTES = """
# Validations for with_constant

## Purpose
Provides raise functions used by the constant update pipeline (`with_constant`).
These checks ensure that constant updates target existing nodes.

## Components

| Component                             | Type     | Description                         |
| :------------------------------------ | :------- | :---------------------------------- |
| `raise_immutability_constant_not_found` | Function | Raised when a constant is missing.  |
"""
