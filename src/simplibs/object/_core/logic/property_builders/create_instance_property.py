from typing import Any, TYPE_CHECKING
from operator import attrgetter
# Annotations
if TYPE_CHECKING:
    from ...protocols.metadata import SimpleMetadataLike


def create_instance_property(
    inner_meta: "SimpleMetadataLike",
    path: tuple[str, ...],
) -> property:
    """Creates a read-only property for accessing an inner instance."""

    # 1. Prepare inner instance resolver
    get_inner_instance = attrgetter(*path)

    # 2. Create getter
    def getter(self) -> Any:
        return get_inner_instance(self)

    # 3. Add return annotation
    getter.__annotations__ = {"return": Any}

    # 4. Build docstring
    doc_string = (
        f"Instance of the inner element `{inner_meta.name_snake}`.\n\n"
        f"The getter returns the instance of the atom or composition stored in the "
        f"private slot `{inner_meta.name_private}`.\n"
        f"This property is read-only – assigning a new instance is not allowed."
    )

    # 5. Return read-only property
    return property(
        fget=getter,
        doc=doc_string,
    )


_DESIGN_NOTES = """
# create_instance_property

## Purpose
Provides a read-only property that exposes the *instance* of an inner element
(atom or composite). This is the structural counterpart to `value` properties:
while `value` exposes the normalized value, this property exposes the underlying
instance object.

## Behavior
1. Uses `attrgetter(*path)` to resolve the inner instance efficiently.
2. Returns the inner instance directly, without wrapping or transforming it.
3. The property is strictly read-only:
   - No setter is generated.
   - Users cannot replace inner instances manually.
4. The property is generated for:
   - direct inners of composite classes,
   - nested inners when mixins expand the inner tree.

## Notes
- This property is essential for introspection, debugging, and advanced user
  interactions with composite structures.
- It complements `create_value_property`, which exposes the *value* of the inner
  node.
- Inner instances are always stored in private slots (e.g., `_motor`), and this
  property provides the safe public API for accessing them.

"""