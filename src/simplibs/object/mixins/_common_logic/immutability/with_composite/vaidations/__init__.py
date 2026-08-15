from .validate_composite_name_exists import validate_composite_name_exists
from .validate_composite_is_decomposeable import validate_composite_is_decomposeable


_DESIGN_NOTES = """
# Validations for with_composite

## Purpose
Provides structural validation functions used by the composite update pipeline
(`with_composite`). These checks ensure that:

- the composite name exists,
- the composite supports decomposition.

## Components

| Component                          | Type     | Description                                 |
| :--------------------------------- | :------- | :------------------------------------------ |
| `validate_composite_name_exists`   | Function | Ensures the composite node exists.          |
| `validate_composite_is_decomposeable` | Function | Ensures the node supports decomposition.    |
"""
