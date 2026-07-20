from typing import Any, TYPE_CHECKING
from collections.abc import Callable
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike
    from ......protocols.instance import SimpleInstanceLike


def create_root_value_setter(
    meta: "SimpleMetadataLike",
    base_class_name: str
) -> Callable:
    """Generates the reactive _root_value_setter mutator method closure for a specific component.

    Ensures transactional value writes, normalization checks, internal state tracking,
    and controls the upstream reactive recalculation bubbling propagation mechanics.
    """

    def _root_value_setter(
        self: "SimpleInstanceLike",
        value: Any,
        recalculate_up: bool = True
    ) -> None:
        """Internal routine managing state mutation with controlled reactive bubbling."""

        # 1. Normalize and validate incoming raw value payload through the system constraints
        new_value = self.normalize(value, process_none=True)

        # 2. Performance short-circuit check: evaluate equality against the current internal state
        # noinspection PyBroadException
        try:
            if self._value == new_value:
                return
        except Exception:
            pass

        # 3. Perform the explicit low-level value assignment mutation
        self._value = new_value

        # 4. Dispatch the value alteration event to the internal logging pipeline tracking framework
        from simplibs.object.settings.logging import log_value_event
        log_value_event(self.__class__, new_value, event="change")

        # 5. Trigger downstream reactive graph synchronization on the composition owner layer
        if self._owner and recalculate_up:
            # noinspection PyProtectedMember
            self._owner._recalculate_self()

    # Re-bind reflection parameters to guarantee clean inspection and diagnostic debugging maps
    _root_value_setter.__name__ = "_root_value_setter"
    _root_value_setter.__qualname__ = f"{base_class_name}._root_value_setter"
    _root_value_setter.__annotations__ = {"value": Any, "recalculate_up": bool, "return": None}

    _root_value_setter.__doc__ = (
        f"Secures atomic data mutation directly into {meta.class_name} instances.\n"
        f"\n"
        f"Executes normalizations, tracks structural value drift against existing data,\n"
        f"and triggers reactive parent recalculation loops (upstream bubbling) upon mutation.\n"
    )

    return _root_value_setter


_DESIGN_NOTES = """
# create_root_value_setter

## Purpose
Acts as the central reactive mutation engine for all mutable Atomic and Composite instances within the metadata layer. It wraps state manipulation with validation safeguards and orchestrates the event propagation cascade throughout the composition tree.

## Architectural Design Decisions

### 1. Short-Circuit Equality Isolation
* The comparison `if self._value == new_value:` prevents redundant data writes, log pollution, and heavy recalculation sweeps when incoming data equals the current state.
* The explicit `try/except Exception: pass` block is an architectural safety net against custom user-defined objects or third-party structures that might raise comparison exceptions (e.g., custom arrays or database handles). In those instances, the system safely ignores the short-circuit and forces a state update.

### 2. Transactional Reactive Upstream Bubbling
* State mutation is decoupled from propagation logic through the conditional execution of `self._owner._recalculate_self()`.
* The `recalculate_up` parameter provides crucial granular flow control during bulk dataset loads or multi-property transaction bindings, allowing external orchestrators to suppress bubbling until all operations finish, preventing intermediate invalid data calculations.

### 3. Dynamic Lazy Logging Binding
* Importing `log_value_event` lazily inside the body of the setter routine breaks circular dependency cycles that commonly plague highly integrated type systems during initialization phases. It ensures execution logging footprints remain isolated within active runtime states.
"""