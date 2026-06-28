from typing import TYPE_CHECKING
# Outers
from .....base_utils.properties import create_properties_for_inner
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike


def create_properties_for_inners(
    meta: "SimpleMetadataLike",
    *,
    mutable: bool = True
) -> dict:
    """
    Generuje property pro všechny přímé inners.
    """

    return {
        k: v
        for inner in meta.inners
        for k, v in create_properties_for_inner(
            inner.meta,
            path=(),
            mutable=mutable
        ).items()
    }
