from typing import TYPE_CHECKING
from collections.abc import Callable
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike
    from ......protocols.instance import SimpleInstanceClassLike


def _get_inner_instance_class(
    inner_meta: "SimpleMetadataLike",
    mutable: bool
) -> "SimpleInstanceClassLike":
    if mutable:
        return (
            inner_meta.atom_class_mutable
            if inner_meta.is_constant
            else inner_meta.composite_class_mutable
        )
    return (
        inner_meta.atom_class_immutable
        if inner_meta.is_constant
        else inner_meta.composite_class_immutable
    )