from .create_names import create_names


_DESIGN_NOTES = """
# Class Name Processing Package

## Purpose
Provides the primary processing pipeline for decomposing, validating, and establishing the deterministic string identity tokens for Simple classes.

## Internal Components Registry

| Component      | Type     | Description                                                                          |
| :------------- | :------- | :----------------------------------------------------------------------------------- |
| `create_names` | Function | The main public entrypoint that derives tokenized, snake_case, and private class identifiers. |
"""