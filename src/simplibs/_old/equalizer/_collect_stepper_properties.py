from typing import TYPE_CHECKING
# Inners
from ._create_stepper_property import _create_stepper_property
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike


def _collect_stepper_properties(
    meta: "SimpleMetadataLike",
    path: tuple[str, ...],
    result: dict
) -> None:


    prop_name = "_".join(p.lstrip("_") for p in path) + "_stepper"
    result[prop_name] = _create_stepper_property(path)

    if not meta.is_constant:

        for inner in meta.inners:


            inner_meta = inner.meta
            new_path = path + (inner_meta.name_private,)


            _collect_stepper_properties(inner_meta, new_path, result)
