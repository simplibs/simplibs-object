from .assert_calculate_value_method import assert_calculate_value_method
from .assert_decompose_value_method import assert_decompose_value_method
from .assert_validate_method import assert_validate_method


_DESIGN_NOTES = """
# Testing Asserts Methods Sub-Package

## Purpose
Provides specialized assertions for framework-level methods including value calculation pipelines,
decomposition behaviors, and custom user validation routines.

## Internal Components Registry

| Component                       | Type     | Description                                                               |
| :------------------------------ | :------- | :------------------------------------------------------------------------ |
| `assert_calculate_value_method` | Function | Asserts correct calculation logic and inner updates for computed leaves.  |
| `assert_decompose_value_method` | Function | Validates top-down decomposition into child node states.                  |
| `assert_validate_method`        | Function | Tests execution and error reporting of custom user validation rules.     |
"""