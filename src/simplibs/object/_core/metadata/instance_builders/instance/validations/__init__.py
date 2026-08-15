from .validate_class_is_not_base_class import validate_class_is_not_base_class
from .validate_hashing_for_immutable_value import validate_hashing_for_immutable_value
from .validate_mixins import validate_mixins
from .validate_param_is_bool import validate_param_is_bool


_DESIGN_NOTES = """
# Instance Validations Sub-Package

## Purpose
Provides core validation functions used during instance creation. Ensures correct
class identity, hashing requirements for immutable instances, mixin compatibility,
and strict boolean configuration parameters.

## Internal Components Registry

| Component                           | Type     | Description                                                |
| :---------------------------------- | :------- | :--------------------------------------------------------- |
| `validate_class_is_not_base_class`  | Function | Blocks instantiation of Simple framework base classes.     |
| `validate_hashing_for_immutable_value` | Function | Ensures default value is hashable for immutable instances. |
| `validate_mixins`                   | Function | Validates mixin identity and compatibility constraints.    |
| `validate_param_is_bool`            | Function | Enforces strict boolean typing for configuration flags.    |
"""
