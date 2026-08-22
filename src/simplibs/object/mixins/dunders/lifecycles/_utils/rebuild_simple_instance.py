from typing import Any, Tuple, Type


def rebuild_simple_instance(
    owner_class: Type[Any],
    mixins: Tuple[Type[Any], ...],
    as_atom: bool,
    mutable: bool,
    state: dict,
) -> Any:
    """Module-level, picklable reconstruction helper for PickleReduce."""

    # 1. Create bare runtime instance via blueprint caller
    instance = owner_class(mixins=mixins, as_atom=as_atom, mutable=mutable)

    # 2. Restore state via __setstate__ (handles mutable and immutable branches)
    result = instance.__setstate__(state)

    # 3. Return newly created instance (immutable mode) or mutated instance (mutable mode)
    return result if result is not None else instance


_DESIGN_NOTES = """
# rebuild_simple_instance

## Purpose
Serves as a module-level, top-level picklable reconstruction helper.
Because dynamic runtime instance classes (`*Instance`) cannot be resolved
by name during unpickling, this function acts as the static factory invoked
by Python's pickle engine.

## Lifecycle Pipeline
1. **Bare Instance Construction**
   Invokes the blueprint class `owner_class` with the original configuration
   (`mixins`, `as_atom`, `mutable`) to compile the runtime class and allocate
   a bare instance.

2. **State Restoration**
   Executes `instance.__setstate__(state)` to decode and apply the serialized
   dictionary payload.

3. **Dual-Mode Materialization**
   - **Mutable mode**: `__setstate__` mutates the instance in-place and returns `None`
     or `self`; the original `instance` is returned.
   - **Immutable mode**: `__setstate__` delegates to `from_dict`, which produces a brand-new
     snapshot-based instance; the new instance `result` is returned.

## Architectural Notes
- By handling state injection directly inside this factory function, pickle's default
  in-place expectation is safely bridged to support immutable snapshot workflows.
"""