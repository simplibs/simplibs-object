from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def _get_collision_path(
    current_class: "SimpleClassLike",
    collision_name: str,
) -> str | None:
    """Returns structural path to the class causing a name collision."""

    # 1. Direct match
    if current_class.meta.name_snake == collision_name:
        return current_class.__name__

    # 2. Scan inners
    raw_inners = getattr(current_class, "_inners", ())

    for inner in raw_inners:
        if collision_name in inner.meta.node_names_set:
            sub_path = _get_collision_path(inner, collision_name)
            if sub_path:
                return f"{current_class.__name__}/{sub_path}"

    # 3. No match
    return None


_DESIGN_NOTES = """
# _get_collision_path

## Purpose
Computes a structural breadcrumb path to the class where a name collision originates.
Used by name‑collision validators to produce clear diagnostic messages.

## Behavior
1. Checks whether the current class owns the name.
2. If not, scans `_inners` using `node_names_set` as a fast pre-filter.
3. Recursively descends only into branches guaranteed to contain the collision.
4. Returns a path like `Order/Delivery/Address` or `None` if not found.

## Notes
Internal helper; does not raise exceptions. Pure path computation.
"""