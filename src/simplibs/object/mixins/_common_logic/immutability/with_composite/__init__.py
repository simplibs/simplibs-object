from .with_composite import with_composite


_DESIGN_NOTES = """
# with_composite

## Purpose
Provides the composite update operation.  
This function updates composite nodes, recalculates inner values, and
propagates changes through owner hierarchies.

## Component

| Component        | Type     | Description                               |
| :--------------- | :------- | :---------------------------------------- |
| `with_composite` | Function | Updates composite nodes immutably.        |
"""
