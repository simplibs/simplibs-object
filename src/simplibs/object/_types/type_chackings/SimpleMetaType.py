from typing import TYPE_CHECKING


# 1. Definice pro typovou kontrolu
if TYPE_CHECKING:

    # 1.1 Vnitřní import třídy pro metadtata
    from ..._metadata import SimpleMeta, SimpleBaseMetadata, SimpleConstantMetadata, SimpleObjectMetadata

    # 1.2 Typ reprezentující metadata
    SimpleMetaType = SimpleMeta | SimpleBaseMetadata | SimpleConstantMetadata | SimpleObjectMetadata

# 2. Definice pro běh
else:
    SimpleMetaType = Any
