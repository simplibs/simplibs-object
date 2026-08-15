from .Call import Call
from .Context import ContextManager


_DESIGN_NOTES = """
# Interfaces Dunders

## Purpose
Gives Simple instances two general-purpose Python protocol interfaces:
calling the instance like a function, and using it as a context manager.

## Components

| Component            | Type  | Description                                                  |
| :------------------- | :---- | :----------------------------------------------------------- |
| `Call`               | Mixin | `__call__` — syntactic sugar over the `with_any` change API. |
| `ContextManager`     | Mixin | `__enter__` / `__exit__` — inert, no-op context support.     |

## Notes
- Both mixins are universal — no compatibility restrictions on either.
- `ContextManager` never suppresses exceptions and never changes state;
  it exists purely to allow `with obj:` usage.
"""
