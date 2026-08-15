from .assert_reactivity_downward import assert_reactivity_downward
from .assert_reactivity_upward import assert_reactivity_upward


_DESIGN_NOTES = """
# Testing Asserts Reactivity Sub-Package

## Purpose
Provides assertions for testing multi-directional reactive state updates across composite object trees.

## Internal Components Registry

| Component                   | Type     | Description                                                               |
| :-------------------------- | :------- | :------------------------------------------------------------------------ |
| `assert_reactivity_downward`| Function | Validates top-down decomposition propagation into inner instances.       |
| `assert_reactivity_upward`  | Function | Asserts bottom-up reactive calculation updates upon inner leaf changes.   |
"""