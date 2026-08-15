from .reacalculate_inners import reacalculate_inners

_DESIGN_NOTES = """
# Helpers for Composite Updates

## Purpose
Provides utilities for recalculating inner nodes during composite updates.
These helpers ensure structural consistency when composite values change.

## Internal Components Registry

| Component             | Type     | Description                                      |
| :-------------------- | :------- | :----------------------------------------------- |
| `reacalculate_inners` | Function | Recomputes inner values recursively.             |
"""
