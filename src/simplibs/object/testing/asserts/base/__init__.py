from .assert_class_inheritance import assert_class_inheritance
from .assert_instance_creation import assert_instance_creation
from .assert_user_instance_creation import assert_user_instance_creation
from .assert_value_change import assert_value_change


_DESIGN_NOTES = """
# Testing Asserts Base Sub-Package

## Purpose
Provides fundamental assertion helpers for testing class hierarchy, core instance initialization,
user-defined creation workflows, and value mutation behavior.

## Internal Components Registry

| Component                      | Type     | Description                                                               |
| :----------------------------- | :------- | :------------------------------------------------------------------------ |
| `assert_class_inheritance`     | Function | Validates base class hierarchy and mandatory inheritance rules.           |
| `assert_instance_creation`     | Function | Verifies correct instantiation and default attribute state.               |
| `assert_user_instance_creation`| Function | Validates initialization with explicit user-provided input parameters.   |
| `assert_value_change`          | Function | Asserts state mutation and value changing behavior on instance.           |
"""