# Outers
from ......protocols import SimpleMetadataType
# Inners
from ......_utils.properties import create_properties_for_inner


def _collect_stepper_properties(
    meta: SimpleMetadataType,
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
