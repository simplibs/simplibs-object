# Outers
from ..metadata import (
    SimpleBaseMetadataProtocol,
    SimpleConstantMetadataProtocol,
    SimpleObjectMetadataProtocol
)


# Typový alias metadatové třídy
SimpleMetadataType = SimpleObjectMetadataProtocol # | SimpleConstantMetadataProtocol | SimpleBaseMetadataProtocol
