from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from ...._commons.constants import OWNER_CLASS, VALUE
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.core_mixins import SerializationProtocol
    from ....._core.protocols.alias_typings import StateDict


def to_dict(
    self: "SerializationProtocol",
    *,
    constant_only: bool = False,
) -> "StateDict":
    """
    Serializes the instance into a readable dictionary structure.
    Composite nodes are expanded into nested dictionaries according to their
    structural path in `nodes_tuple`.
    """

    # 1. Define base variables
    result = {OWNER_CLASS: self.meta.owner_class}
    last_composite_key = UNSET
    last_composite_dict = {}

    # 2. Iterate through nodes_tuple in structural order
    for instance, path in self._nodes_tuple:

        # 2.1 Define per-node variables
        value = instance._value
        current_dict = result
        last_key = path[0]

        # 2.2 Handle composite nodes (non-root)
        if len(path) > 1:

            # 2.2.1 Extract last and second-to-last keys
            last_key = path[-1]
            before_last_key = path[-2]

            # 2.2.2 Reuse previously cached composite dictionary
            if last_composite_key == before_last_key:
                current_dict = last_composite_dict

            # 2.2.3 Create a new composite dictionary
            else:

                # 2.2.3.1 Build nested structure for all keys except the last
                for key in path[:-1]:
                    current_dict = current_dict.setdefault(key, {})

                # 2.2.3.2 Cache composite dictionary for next iteration
                if last_key == VALUE:
                    last_composite_key = before_last_key
                    last_composite_dict = current_dict

        # 2.3 Write the node value (unless filtered out)
        if not (constant_only and last_key == VALUE):
            current_dict[last_key] = value

    # 3. Return the final dictionary
    return result


_DESIGN_NOTES = """
# to_dict

## Purpose
Converts an instance into a structured dictionary representation based on
`nodes_tuple`. This dictionary is the foundation for JSON serialization,
snapshot creation, debugging tools, immutability pipelines, and history
tracking.

The function expands composite nodes into nested dictionaries according to
their structural path, while constants remain as flat key-value pairs.

## Architectural role
`to_dict` is a core export mechanism used by:

- `SerializationMixin` (public API: `to_dict`, `to_json`)
- `SnapshotMixin` (snapshot creation)
- `HistoryMixin` (state diffs)
- immutability helpers (building new instances)
- debugging utilities (printing internal state)
- JSON pipelines (external integrations)

It provides a **deterministic**, **stable**, and **structure-aware** view of the
entire object tree.

## How it works
The function iterates through `nodes_tuple`, which contains `(instance, path)`
pairs describing the full object structure.

For each node:

1. **Determine the dictionary level**  
   Composite nodes require nested dictionaries based on their path.

2. **Reuse composite dictionaries**  
   To avoid repeatedly reconstructing nested structures, the function caches
   the last composite dictionary (`last_composite_dict`) and reuses it when
   possible.

3. **Write the node value**  
   Constants are written directly. Composite nodes write their `_value` under
   the `VALUE` key.

4. **Optional filtering**  
   When `constant_only=True`, composite nodes are skipped.

## Deterministic output
The resulting dictionary is:

- **stable** — identical for identical instance structures,
- **ordered** — follows the order of `nodes_tuple`,
- **structurally faithful** — mirrors the composite hierarchy,
- **safe for JSON** — contains only primitive values and nested dicts.

This determinism is essential for snapshot comparison, diffing, and immutability.

## Why composite caching exists
Without caching, each composite node would reconstruct its nested dictionary
structure from scratch, causing:

- unnecessary allocations,
- slower serialization,
- inconsistent dictionary identity,
- increased GC pressure.

Caching ensures:

- linear performance,
- predictable behavior,
- minimal memory churn.

## Stability guarantee
Any change to this function would affect:

- JSON output,
- snapshot creation,
- immutability pipelines,
- history tracking,
- debugging tools,
- serialization consistency.

Therefore, `to_dict` is treated as a **core invariant** of the Simple system.

## Notes
- This function is intentionally low-level and not part of the public API.
- All structural logic is delegated to `nodes_tuple`.
- All composite logic is based on the `VALUE` constant.
"""