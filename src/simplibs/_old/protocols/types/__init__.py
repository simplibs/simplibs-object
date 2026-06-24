from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .SimpleClassType import SimpleClassType
    from .SimpleInstanceType import SimpleInstanceType
    from .SimpleMetadataType import SimpleMetadataType
else:
    # Runtime fallback, abychom nezpůsobili pád při přímém importu z tohoto initu
    from typing import Any
    SimpleClassType = Any
    SimpleInstanceType = Any
    SimpleMetadataType = Any