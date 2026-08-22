from .validate_mixin_is_class import validate_mixin_is_class
from .validate_mixin_is_simple_base_subclass import validate_mixin_is_simple_base_subclass
from .raise_mixin_not_allowed_for_composite import raise_mixin_not_allowed_for_composite
from .raise_mixin_not_allowed_for_constant import raise_mixin_not_allowed_for_constant
from .raise_mixin_not_allowed_for_immutable import raise_mixin_not_allowed_for_immutable
from .raise_mixin_not_allowed_for_mutable import raise_mixin_not_allowed_for_mutable
from .raise_mixin_not_support_default_value_type import raise_mixin_not_support_default_value_type


_DESIGN_NOTES = """
# Mixin Validations Sub-Package

## Purpose
Provides identity and compatibility validators for mixins used during instance
construction. Ensures that mixins match structural mode, mutability, and default
value constraints.

## Internal Components Registry

| Component                                   | Type     | Description                                              |
| :------------------------------------------ | :------- | :------------------------------------------------------- |
| `validate_mixin_is_class`                   | Function | Ensures mixin is a class object.                        |
| `validate_mixin_is_simple_base_subclass`    | Function | Verifies mixin inherits from SimpleMixin.               |
| `raise_mixin_not_allowed_for_composite`     | Function | Blocks `_constant_only` mixins on composite instances.  |
| `raise_mixin_not_allowed_for_constant`      | Function | Blocks `_composite_only` mixins on atomic instances.    |
| `raise_mixin_not_allowed_for_immutable`     | Function | Blocks `_mutable_only` mixins on immutable instances.   |
| `raise_mixin_not_allowed_for_mutable`       | Function | Blocks `_immutable_only` mixins on mutable instances.   |
| `raise_mixin_not_support_default_value_type`| Function | Enforces `_only_types` default value type constraints.  |
"""
