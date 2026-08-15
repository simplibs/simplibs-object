from .assert_immutable_behavior import assert_immutable_behavior
from .assert_mutable_behavior import assert_mutable_behavior


_DESIGN_NOTES = """
# Testing Asserts Mutability Sub-Package

## Purpose
Contains assertions for verifying mutability constraints on instances, ensuring read-only properties
raise proper errors and mutable fields respond correctly to state updates.

## Internal Components Registry

| Component                   | Type     | Description                                                               |
| :-------------------------- | :------- | :------------------------------------------------------------------------ |
| `assert_immutable_behavior` | Function | Asserts that modifications on locked or immutable instances raise errors. |
| `assert_mutable_behavior`   | Function | Validates normal assignment and state mutation operations.               |
"""