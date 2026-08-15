from .raise_locked_value_error import raise_locked_value_error


_DESIGN_NOTES = """
# Value Helper Validation Sub-Package

## Purpose
Provides structured error generators used by value property builders. These
helpers ensure consistent diagnostics when value mutation is not permitted.

## Internal Components Registry

| Component                 | Type     | Description                                      |
| :------------------------ | :------- | :------------------------------------------------ |
| `raise_locked_value_error` | Function | Raised when a locked instance attempts mutation.  |
"""
