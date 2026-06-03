# Outers
from ..._types import SimpleClassType
from ..SimpleConstantMetadata import SimpleConstantMetadata
from ..SimpleObjectMetadata import SimpleObjectMetadata
from ..constants import BASE_CLASS_NAMES


def create_simple_class_metadata(
    cls: SimpleClassType,
    name: str,
) -> SimpleClassType:

    # 1. Přeskočení vytváření metadata pro základní a instanční třídy
    if hasattr(cls, "_is_instance_class") or name in BASE_CLASS_NAMES:
        return cls

    # 2. Výpočet metadat (pro deklarativní třídy)
    cls.__metadata__ = (
        SimpleObjectMetadata(owner_class=cls)
        if hasattr(cls, "_inners")
        else SimpleConstantMetadata(owner_class=cls)
    )

    # 3. Navrácení třídy
    return cls