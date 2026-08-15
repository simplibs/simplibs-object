from .compare_snapshots import compare_snapshots

_DESIGN_NOTES = """
# Snapshot Utilities

## Purpose
Provides core utilities for working with snapshots, including comparison logic
used by history tracking, debugging tools, and immutability pipelines.

## Internal Components Registry

| Component           | Type     | Description                                  |
| :------------------ | :------- | :------------------------------------------- |
| `compare_snapshots` | Function | Computes structural diffs between snapshots. |
"""
