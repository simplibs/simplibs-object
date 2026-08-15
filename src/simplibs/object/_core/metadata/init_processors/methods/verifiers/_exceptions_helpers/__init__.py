from .exception_info_for_classmethod import exception_info_for_classmethod
from .expected_structure_for_classmethod import expected_structure_for_classmethod


_DESIGN_NOTES = """
# Exception Helpers Sub-Package

## Purpose
Provides structural exception payload definitions and contextual reflection extraction helpers tailored for diagnostic reporting inside method signature verifiers.

## Internal Components Registry

| Component                            | Type     | Description                                                                          |
| :----------------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `exception_info_for_classmethod`     | Function | Low-level extraction utility mapping raw method attributes to basic error context.  |
| `expected_structure_for_classmethod` | Function | High-level diagnostic text and structural blueprint formatter for exception errors. |
"""