from .build_nodes_tuple import build_nodes_tuple

_DESIGN_NOTES = """
# Nodes Tuple Utilities

## Purpose
Provides the core structural traversal utilities used to build the canonical
(nodes_tuple) representation of an object. These utilities form the foundation
for snapshot creation, serialization, immutability pipelines, and history
tracking.

## Internal Components Registry

| Component              | Type     | Description                                         |
| :--------------------- | :------- | :-------------------------------------------------- |
| `build_nodes_tuple`    | Function | Wraps traversal and produces the final tuple.       |
"""
