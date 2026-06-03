# outers
from ..SimpleBaseMetadata import SimpleBaseMetadata
from ..SimpleConstantMetadata import SimpleConstantMetadata
from ..SimpleObjectMetadata import SimpleObjectMetadata


# Mapování systémových kořenů na jejich metadata třídy
ROOT_METADATA_MAPPING = {
    "SimpleBase": SimpleBaseMetadata,
    "SimpleConstant": SimpleConstantMetadata,
    "SimpleObject": SimpleObjectMetadata,
}
