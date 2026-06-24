from .SimpleMetaProtocol import SimpleMetaProtocol
from .SimpleBaseMetadataProtocol import SimpleBaseMetadataProtocol
from .SimpleConstantMetadataProtocol import SimpleConstantMetadataProtocol
from .SimpleObjectMetadataProtocol import SimpleObjectMetadataProtocol

# Prvek definující největší množinu (superset pro anotace)
SimpleMetadataLike = SimpleObjectMetadataProtocol

# Prvek definující nejmenší množinu (minimální rozhraní pro ověření typu)
SimpleMetadataType = SimpleBaseMetadataProtocol