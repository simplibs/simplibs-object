from typing import TYPE_CHECKING
from collections.abc import Callable
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike
    from ......protocols.instance.core_classes import CompositeInstanceProtocol


def create_recalculate_inners(
    meta: "SimpleMetadataLike",
    base_class_name: str
) -> Callable:
    """Generates the reactive _recalculate_inners execution method closure for a Composite base class.

    Decomposes the composite's root value payload and distributes individual shards down
    to immediate child nodes while suppressing cyclic recursive upstream updates.
    """

    def _recalculate_inners(
        self: "CompositeInstanceProtocol"
    ) -> None:

        # 1. Deconstruct the compound composite state value into individual inner component shards
        decomposed_values = self.decompose_value(self._value)

        # 2. Distribute data payloads into respective child node slot instances
        for inner, inner_value in zip(meta.inners, decomposed_values):

            # 2.1 Fetch the specific private slot instance of the structural child node
            inner_instance = getattr(self, inner.meta.name_private)

            # 2.2 Execute value write mutation with explicitly suppressed upstream reactive bubbling
            # noinspection PyProtectedMember
            inner_instance._root_value_setter(inner_value, recalculate_up=False)

            # 2.3 Cascading condition: if the child is a composite node, trigger its nested down-tree recalculation
            if not inner.meta.is_constant:
                # noinspection PyProtectedMember
                inner_instance._recalculate_inners()

    # Re-bind reflection specifications to preserve clean stack traces and profiling identifiers
    _recalculate_inners.__name__ = "_recalculate_inners"
    _recalculate_inners.__qualname__ = f"{base_class_name}._recalculate_inners"
    _recalculate_inners.__annotations__ = {"return": None}

    _recalculate_inners.__doc__ = (
        f"Deconstructs the core value of the {meta.class_name} composite and pushes states to its children.\n"
        f"\n"
        f"Executes a cascading downward reactive sync loop across all child nodes. "
        f"Triggered automatically whenever the primary container value mutates.\n"
    )

    return _recalculate_inners


_DESIGN_NOTES = """
# create_recalculate_inners

## Purpose
Acts as the downward data distribution hub of the reactive composition tree. When a user or system event mutates the root value of a Composite node, this routine takes the compound object, splits it into parts via `decompose_value`, and synchronizes the downstream nested nodes to reflect the changes.

## Architectural Design Decisions

### 1. Loop Recursion Loop Invariant Protection (`recalculate_up=False`)
* A severe hazard in bidirectional graph serialization is the infinite ping-pong loop: a parent updates its child, which triggers the child to alert the parent, which loops back indefinitely.
* To prevent stack overflows, the child mutation call passes `recalculate_up=False`. This tells the child: *"Accept this new value state, but do not bubble a notification back up because this change originated from above."*

### 2. Tailored Depth Cascade Topology Tracking
* The evaluation `if not inner.meta.is_constant:` checks if a child node is a terminal value parameter (an Atom) or another sub-composition container (a Composite Node).
* If the child is a container, the routine fires `inner_instance._recalculate_inners()`. This triggers a top-down serialization cascade, pushing updated data fragments down to the deepest leaf elements of the domain tree.

### 3. Zipped Positional Assignment Execution
* Relying on `zip(meta.inners, decomposed_values)` mandates a strict matching rule: `decompose_value` must return a data structure matching both the exact count and alignment order of the `meta.inners` definition array. 
* This mechanical mapping keeps runtime processing highly efficient by bypassing expensive key-based index traversals during state changes.
"""