from .raise_with_any_changes_is_not_tuple import raise_with_any_changes_is_not_tuple
from .raise_with_any_child_composite_mismatch import raise_with_any_child_composite_mismatch
from .raise_with_any_contained_constant_mismatch import raise_with_any_contained_constant_mismatch


_DESIGN_NOTES = """
# Validations for with_any

## Purpose
Provides structured raise functions used by the mixed update pipeline
(`with_any`). These validations ensure that:

- the input format is correct,
- child composites match recalculated values,
- contained constants remain consistent with composite updates.

## Components

| Component                                   | Type     | Description                                      |
| :------------------------------------------- | :------- | :----------------------------------------------- |
| `raise_with_any_changes_is_not_tuple`        | Function | Ensures `changes` is a tuple.                    |
| `raise_with_any_child_composite_mismatch`    | Function | Validates child composite consistency.           |
| `raise_with_any_contained_constant_mismatch` | Function | Validates contained constant consistency.        |
"""
