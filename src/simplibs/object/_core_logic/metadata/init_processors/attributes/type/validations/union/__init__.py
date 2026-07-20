from .raise_union_type_contain_none import raise_union_type_contain_none


_DESIGN_NOTES = """
# Union Type Validation Sub-Package

## Purpose
Isolates exception factories and internal evaluation constraints tailored specifically for modern native Python Union expressions.

## Internal Components Registry

| Component                      | Type     | Description                                                                          |
| :----------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `raise_union_type_contain_none`| Function | Explicit error generator triggered when a modern native union contains a NoneType.  |
"""