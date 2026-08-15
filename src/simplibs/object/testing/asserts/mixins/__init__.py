from .assert_instance_hasattr import assert_instance_hasattr
from .assert_mixin_inheritance import assert_mixin_inheritance
from .assert_mixin_instance_creation import assert_mixin_instance_creation
from .assert_mixins_slots_values import assert_mixins_slots_values


_DESIGN_NOTES = """
# Testing Asserts Mixins Sub-Package

## Purpose
Provides dedicated assertions for inspecting and testing `SimpleMixin` components,
verifying inheritance, instance composition, attribute availability, and `__slots__` layout.

## Internal Components Registry

| Component                        | Type     | Description                                                               |
| :------------------------------- | :------- | :------------------------------------------------------------------------ |
| `assert_instance_hasattr`        | Function | Validates presence and accessibility of mixin attributes on an instance.  |
| `assert_mixin_inheritance`       | Function | Asserts proper mixin class structure and base inheritance.               |
| `assert_mixin_instance_creation` | Function | Asserts successful instantiation of test containers using mixins.         |
| `assert_mixins_slots_values`     | Function | Inspects `__slots__` layout and memory safety across mixin structures.    |
"""