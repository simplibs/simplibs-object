from typing import TYPE_CHECKING
import json
# Inners
from .Infrastructure import Infrastructure
from ._utils.serialization import to_dict, from_dict, from_dict_constants
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.core_mixins import SerializationProtocol
    from ..._core.protocols.alias_typings import StateDict


class Serialization(Infrastructure):
    """
    Universal master mixin for complete object serialization and
    deserialization.

    Covers both export (to_dict, to_json) and import (from_dict,
    from_json, update). Thanks to a built-in closed type system, it
    automatically reacts to whether the object operates in mutable mode
    (in-place mutation) or immutable mode (returns a modified new
    instance).
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - EXPORT TO DICT / JSON
    # ----------------------------------------

    def to_dict(
        self: "SerializationProtocol",
        *,
        constant_only: bool = False
    ) -> "StateDict":
        """Serializes the instance into a readable flat dict."""
        return to_dict(self, constant_only=constant_only)

    def to_json(
        self: "SerializationProtocol",
        **kwargs
    ) -> str:
        """Serializes the instance into a JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)

    # ----------------------------------------
    # Methods - IMPORT & UPDATE FROM DICT / JSON
    # ----------------------------------------

    def from_dict(
        self: "SerializationProtocol",
        user_dict: "StateDict"
    ) -> "SerializationProtocol":
        """
        Reconstructs the instance's state from the given dict.

        - In mutable mode: modifies the instance directly in place.
        - In immutable mode: returns a new, modified instance.
        """
        return from_dict(self, user_dict)

    def from_json(
        self: "SerializationProtocol",
        json_str: str
    ) -> "SerializationProtocol":
        """Reconstructs the instance's state from a JSON string."""
        return self.from_dict(json.loads(json_str))

    def update_constants(
        self: "SerializationProtocol",
        user_dict: "StateDict"
    ) -> "SerializationProtocol":
        """
        Updates constants (atoms) from the given dict.
        The dict may be partial. Respects mutable/immutable mode.
        """
        return from_dict_constants(self, user_dict)


_DESIGN_NOTES = """
# Serialization

## Purpose
The universal, "master" import/export mixin — `to_dict()`/`to_json()` for
reading an instance out as plain data, and `from_dict()`/`from_json()`/
`update_constants()` for rebuilding or updating one from plain data.

## Compatibility
- No compatibility flags — deliberately universal. Rather than branching
  on mutability itself, this mixin relies on `from_dict`/`from_dict_constants`
  internally detecting the instance's mode and doing the right thing.

## Logic
- `to_dict(constant_only=False)` and `to_json(**kwargs)` are thin
  wrappers over the `to_dict` utility — `to_json` simply forwards
  `self.to_dict()` into `json.dumps`, passing through any extra kwargs
  (indent, sort_keys, etc.) and forcing `ensure_ascii=False` so non-ASCII
  text serializes readably rather than as escape sequences.
- `from_dict(user_dict)` delegates entirely to the `from_dict` utility,
  which is where the mutable-vs-immutable branching actually lives:
  **mutable** instances are updated in place and `self` is effectively
  returned; **immutable** instances get a new instance back, unaffected
  by the original.
- `from_json(json_str)` is just `json.loads` piped into `from_dict`.
- `update_constants(user_dict)` is the partial-update variant — it only
  touches constants (atoms), and accepts a dict that doesn't need to
  cover every field, delegating to `from_dict_constants`.

## Notes
- Because this mixin builds on `Infrastructure` (→ `NodesDicts` +
  `Snapshot`), the serialization utilities it calls have direct access to
  the node tree and snapshot machinery without re-deriving it.
- `PickleState` (in the dunders package) builds directly on top of this
  mixin's `to_dict()`/`from_dict()` for `pickle` support — this is the
  shared foundation both "plain" serialization and pickling rely on.
"""
