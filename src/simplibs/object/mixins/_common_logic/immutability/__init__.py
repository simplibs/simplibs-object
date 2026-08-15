from .with_constant import with_constant
from .with_constants import with_constants
from .with_composite import with_composite
from .with_any import with_any
from .with_constant.utils.create_new_instance import create_new_instance


_DESIGN_NOTES = """
# Immutability Pipeline

## Purpose
Provides the high-level immutable update operations used throughout the Simple
object framework. These functions form the public immutability API and route
updates to the correct structural pipelines.

In addition, this module re-exports `create_new_instance`, a core utility used
across all immutability operations to construct fresh instances from snapshots.

## Internal Components Registry

| Component             | Type     | Description                                      |
| :-------------------- | :------- | :----------------------------------------------- |
| `with_constant`       | Function | Updates a single constant value immutably.       |
| `with_constants`      | Function | Applies multiple constant updates immutably.     |
| `with_composite`      | Function | Updates composite nodes and recalculates inners. |
| `with_any`            | Function | Unified entry point for mixed update operations. |
| `create_new_instance` | Function | Builds a new instance from a snapshot.           |
"""
