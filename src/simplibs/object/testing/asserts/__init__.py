from .base import (
    assert_class_inheritance,
    assert_instance_creation,
    assert_user_instance_creation,
    assert_value_change,
)
from .methods import (
    assert_calculate_value_method,
    assert_decompose_value_method,
    assert_validate_method,
)
from .mixins import (
    assert_instance_hasattr,
    assert_mixin_inheritance,
    assert_mixin_instance_creation,
    assert_mixins_slots_values,
)
from .mutability import (
    assert_immutable_behavior,
    assert_mutable_behavior,
)
from .reactivity import (
    assert_reactivity_downward,
    assert_reactivity_upward,
)


_DESIGN_NOTES = """
# Testing Asserts Sub-Package Root

## Purpose
Aggregates all testing assertion functions across base, methods, mixins, mutability, and reactivity sub-modules.

## Internal Components Registry

| Component                       | Type     | Description                                                               |
| :------------------------------ | :------- | :------------------------------------------------------------------------ |
| `assert_class_inheritance`      | Function | Validates base class hierarchy and mandatory inheritance rules.           |
| `assert_instance_creation`      | Function | Verifies correct instantiation and default attribute state.               |
| `assert_user_instance_creation` | Function | Validates initialization with explicit user-provided input parameters.   |
| `assert_value_change`           | Function | Asserts state mutation and value changing behavior on instance.           |
| `assert_calculate_value_method`  | Function | Asserts correct calculation logic and inner updates for computed leaves.  |
| `assert_decompose_value_method`  | Function | Validates top-down decomposition into child node states.                  |
| `assert_validate_method`         | Function | Tests execution and error reporting of custom user validation rules.     |
| `assert_instance_hasattr`         | Function | Validates presence and accessibility of mixin attributes on an instance.  |
| `assert_mixin_inheritance`        | Function | Asserts proper mixin class structure and base inheritance.               |
| `assert_mixin_instance_creation`  | Function | Asserts successful instantiation of test containers using mixins.         |
| `assert_mixins_slots_values`      | Function | Inspects `__slots__` layout and memory safety across mixin structures.    |
| `assert_immutable_behavior`      | Function | Asserts that modifications on locked or immutable instances raise errors. |
| `assert_mutable_behavior`        | Function | Validates normal assignment and state mutation operations.               |
| `assert_reactivity_downward`     | Function | Validates top-down decomposition propagation into inner instances.       |
| `assert_reactivity_upward`       | Function | Asserts bottom-up reactive calculation updates upon inner leaf changes.   |
"""