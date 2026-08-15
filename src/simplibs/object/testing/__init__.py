from .assert_simple_mixin import assert_simple_mixin
from .assert_simple_object import assert_simple_object
from .bulk_test import bulk_test
from .asserts import (
    assert_calculate_value_method,
    assert_class_inheritance,
    assert_decompose_value_method,
    assert_immutable_behavior,
    assert_instance_creation,
    assert_instance_hasattr,
    assert_mixin_inheritance,
    assert_mixin_instance_creation,
    assert_mixins_slots_values,
    assert_mutable_behavior,
    assert_reactivity_downward,
    assert_reactivity_upward,
    assert_user_instance_creation,
    assert_validate_method,
    assert_value_change,
)
from .containers import (
    InnerValue,
    MixinCase,
    ObjectCase,
    TestMixin,
)


__all__ = (
    # Top-Level Entry Points
    "assert_simple_mixin",
    "assert_simple_object",
    "bulk_test",
    # Containers
    "InnerValue",
    "MixinCase",
    "ObjectCase",
    "TestMixin",
    # Detailed Asserts
    "assert_calculate_value_method",
    "assert_class_inheritance",
    "assert_decompose_value_method",
    "assert_immutable_behavior",
    "assert_instance_creation",
    "assert_instance_hasattr",
    "assert_mixin_inheritance",
    "assert_mixin_instance_creation",
    "assert_mixins_slots_values",
    "assert_mutable_behavior",
    "assert_reactivity_downward",
    "assert_reactivity_upward",
    "assert_user_instance_creation",
    "assert_validate_method",
    "assert_value_change",
)

_DESIGN_NOTES = """
# Testing Sub-Package Root

## Purpose
Serves as the primary API interface for the `simplibs.object.testing` suite, exposing high-level suite runners,
dataclass case containers, individual assertion functions, and randomization fuzzing utilities.

## Internal Components Registry

| Component                       | Type     | Description                                                               |
| :------------------------------ | :------- | :------------------------------------------------------------------------ |
| `assert_simple_mixin`           | Function | Complete test suite execution runner for `SimpleMixin` targets.           |
| `assert_simple_object`          | Function | Complete test suite execution runner for `SimpleObject` targets.          |
| `bulk_test`                     | Function | Executes a collection of test cases against target classes.               |
| `InnerValue`                    | Class    | Dataclass specifying nested leaf inner path and expected values.          |
| `MixinCase`                     | Class    | Dataclass container for mixin suite configuration parameters.             |
| `ObjectCase`                    | Class    | Dataclass container for full object suite configuration parameters.       |
| `TestMixin`                     | Class    | Abstract base class target for constructing mixin tests.                  |
| `assert_calculate_value_method` | Function | Asserts calculation behavior on computed leaves.                         |
| `assert_class_inheritance`     | Function | Asserts base class inheritance hierarchy.                                 |
| `assert_decompose_value_method` | Function | Asserts top-down value decomposition into inner nodes.                   |
| `assert_immutable_behavior`     | Function | Asserts error handling on immutable/locked instance modifications.       |
| `assert_instance_creation`     | Function | Asserts default instance instantiation.                                   |
| `assert_instance_hasattr`       | Function | Asserts presence of mixin attributes on instances.                       |
| `assert_mixin_inheritance`      | Function | Asserts mixin base class structure.                                       |
| `assert_mixin_instance_creation`| Function | Asserts successful creation of mixin test targets.                        |
| `assert_mixins_slots_values`     | Function | Inspects `__slots__` layout for memory safety.                            |
| `assert_mutable_behavior`       | Function | Asserts standard mutable state assignments.                               |
| `assert_reactivity_downward`    | Function | Asserts top-down reactive tree updates.                                   |
| `assert_reactivity_upward`      | Function | Asserts bottom-up reactive calculation updates.                           |
| `assert_user_instance_creation` | Function | Asserts instantiation with explicit input parameters.                     |
| `assert_validate_method`        | Function | Asserts user-defined validation rule execution.                          |
| `assert_value_change`           | Function | Asserts state mutation and value updates.                                 |
"""