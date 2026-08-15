from .create_new_instance import create_new_instance
from .create_snapshot_dict import create_snapshot_dict
from .reacalculate_owner_value import reacalculate_owner_value

_DESIGN_NOTES = """
# Common Immutability Helpers

## Purpose
Provides core helper functions shared across all immutability pipelines.
These utilities handle snapshot creation, instance reconstruction, and owner
value recalculation.

## Internal Components Registry

| Component                | Type     | Description                                      |
| :----------------------- | :------- | :----------------------------------------------- |
| `create_new_instance`    | Function | Builds new instance and restores snapshot.       |
| `create_snapshot_dict`   | Function | Creates dictionary snapshot from nodes.          |
| `recalculate_owner_value`| Function | Recomputes composite owner values.               |
"""
