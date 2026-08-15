from .find_longest_keys import find_longest_keys

_DESIGN_NOTES = """
# Helpers for Constant Batch Updates

## Purpose
Provides utilities used by the `with_constants` pipeline. These helpers
determine recalculation order and structural depth of affected constants.

## Internal Components Registry

| Component           | Type     | Description                                      |
| :------------------ | :------- | :----------------------------------------------- |
| `find_longest_keys` | Function | Determines deepest affected constant paths.      |
"""
