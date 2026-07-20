from typing import TYPE_CHECKING
from collections.abc import Callable
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike
    from ......protocols.instance.core_classes import CompositeInstanceProtocol


def create_recalculate_self(
    meta: "SimpleMetadataLike",
    base_class_name: str
) -> Callable:
    """Generates the reactive _recalculate_self execution method closure for a Composite base class.

    Aggregates active child state value maps, triggers the composite calculation engine,
    updates local state, and bubbles changes upstream through the container graph hierarchy.
    """

    def _recalculate_self(
        self: "CompositeInstanceProtocol"
    ) -> None:

        # 1. Harvest a key-value data map containing the current exposed state of all child nodes
        current_values = {
            inner.meta.name_snake: getattr(self, inner.meta.name_private).value
            for inner in meta.inners
        }

        # 2. Trigger the dynamic structural business logic formula calculation engine
        new_value = self.calculate_value(**current_values)

        # 3. State short-circuit check: only execute updates and bubbling if data drift is detected
        # noinspection PyBroadException
        try:
            if self._value == new_value:
                return
        except Exception:
            pass

        # Persist the newly materialized compound data state payload
        self._value = new_value

        # 4. If this composition container is nested inside another parent, bubble the update upstream
        if self._owner:
            # noinspection PyProtectedMember
            self._owner._recalculate_self()

    # Re-bind reflection specifications to preserve clean stack traces and profiling identifiers
    _recalculate_self.__name__ = "_recalculate_self"
    _recalculate_self.__qualname__ = f"{base_class_name}._recalculate_self"
    _recalculate_self.__annotations__ = {"return": None}

    _recalculate_self.__doc__ = (
        f"Recalculates the composite value state for {meta.class_name} and bubbles notifications upstream.\n"
        f"\n"
        f"Executes a bottom-up reactive calculation cycle. "
        f"Triggered automatically whenever an underlying child parameter or sub-tree state mutates.\n"
    )

    return _recalculate_self


_DESIGN_NOTES = """
# create_recalculate_self

## Purpose
Acts as the upward reactive aggregation engine for composition models. When a deep leaf parameter changes, the change triggers this routine on its container. The routine sweeps across immediate child slots, re-runs `calculate_value` to synthesize a new composite state, and bubbles the result up to the root of the graph.

## Architectural Design Decisions

### 1. Dictionary-Driven Decoupled Aggregation
* The dictionary comprehension constructs an isolated key-value signature map using public `name_snake` identifiers as keys, mapping them to values extracted from private slot references (`inner.meta.name_private`).
* Passing this dictionary via keyword expansion (`**current_values`) into `calculate_value` creates a clean boundary for business logic methods. User-defined calculations can consume values as standard arguments without needing to parse internal tree structures or structural slots.

### 2. Upstream Propagation Short-Circuit Safeguards
* Complex business logic calculations often map distinct, changing child inputs to identical compound output structures.
* The equality check `if self._value == new_value:` halts unnecessary bubbling early. If the calculated composite state remains unchanged, the routine returns immediately, preventing propagation waves from draining CPU cycles across large, multi-tiered structural models.
* The safety `try/except Exception: pass` block prevents comparison errors in custom objects from crashing the recalculation loop, forcing a fallback state overwrite to keep the data state valid.

### 3. Bottom-Up Synthesis Direction (Bubbling)
* The conditional branch `if self._owner:` checks if this node is an embedded sub-tree component or a root-level orchestrator.
* If a parent container exists, the routine triggers `_owner._recalculate_self()`. This completes the reactive chain: leaf mutations trigger a sequential bottom-up recalculation wave, ensuring every parent container automatically reflects the accurate state of its nested children.
"""