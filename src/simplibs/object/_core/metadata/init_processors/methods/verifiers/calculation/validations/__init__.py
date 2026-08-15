from .raise_method_raised_exceptions import raise_method_raised_exceptions
from .raise_method_return_unvalide_outcome_type import raise_method_return_unvalide_outcome_type


_DESIGN_NOTES = """
# Calculation Validation Sub-Package

## Purpose
Isolates diagnostic panic routines responsible for catching and handling evaluations that violate runtime execution schemas.

## Internal Components Registry

| Component                                     | Type     | Description                                                                          |
| :-------------------------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `raise_method_raised_exceptions`              | Function | Standardized wrapper converting unexpected computation errors into domain exceptions. |
| `raise_method_return_unvalide_outcome_type`   | Function | Panics when a method computation yields an object mismatching schema expectations.   |
"""