from .process_inners import process_inners


_DESIGN_NOTES = """
# Inners Processor Core Package

## Purpose
Acts as the root entry point for the structural components framework, exporting the central orchestration engine to the metadata lifecycle.

## Internal Components Registry

| Component                             | Type     | Description                                                                          |
| :------------------------------------ | :------- | :----------------------------------------------------------------------------------- |
| `process_inners`                      | Function | Runs container checks, iterates through components, and registers collision-free trees.|
"""