from .rebuild_simple_instance import rebuild_simple_instance


_DESIGN_NOTES = """
# Lifecycles Utils

## Purpose
Provides low-level reconstruction helpers and internal utilities supporting
the lifecycle and serialization mixin implementations.

## Components

| Component                 | Type     | Description                                                          |
| :------------------------ | :------- | :------------------------------------------------------------------- |
| `rebuild_simple_instance` | Function | Module-level factory helper for unpickling dynamic runtime instances.|

## Notes
- These utilities are intended for internal framework mechanics and pickle
  protocol callbacks; they are not part of the primary public API.
"""