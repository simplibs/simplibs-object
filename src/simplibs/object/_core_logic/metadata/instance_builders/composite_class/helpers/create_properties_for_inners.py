# Outers
from .....protocols import SimpleMetadataType
from ....._utils.properties import create_properties_for_inner


def create_properties_for_inners(
    meta: SimpleMetadataType,
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
