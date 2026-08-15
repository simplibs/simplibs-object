from .raise_snapshot_incompatible_error import raise_snapshot_incompatible_error

_DESIGN_NOTES = """
# Snapshot Validation Utilities

## Purpose
Provides structured diagnostic errors for snapshot comparison failures. Ensures
that invalid or incompatible snapshots never propagate through history or
immutability pipelines.

## Internal Components Registry

| Component                         | Type     | Description                                         |
| :-------------------------------- | :------- | :-------------------------------------------------- |
| `raise_snapshot_incompatible_error` | Function | Raises structured error for incompatible snapshots. |
"""
