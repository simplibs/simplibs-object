from .process_type import process_type


_DESIGN_NOTES = """
# Attribute Type Processing Package

## Purpose
Orchestrates the metadata extraction pipeline responsible for validating, parsing, and normalizing class type boundary parameters across all domain structures.

## Internal Components Registry

| Component      | Type     | Description                                                                          |
| :------------- | :------- | :----------------------------------------------------------------------------------- |
| `process_type` | Function | The single public pipeline entrypoint that transforms raw type layouts into flat, native UnionTypes. |
"""