# 1. IMPORTY PROTOKOLŮ (Pro běh i pro typy)
from .classes import (
    SimpleBaseProtocol,
    SimpleConstantProtocol,
    SimpleObjectProtocol,
)
from .instance import (
    SimpleInstanceBaseProtocol,
    SimpleConstantInstanceProtocol,
)
from .metadata import (
    SimpleBaseMetadataProtocol,
    SimpleConstantMetadataProtocol,
    SimpleObjectMetadataProtocol,
)
from .methods import (
    ClassMethodProtocol,
    LogicSignature,
    P,
    R,
)


# 3. EXPORT MANIFEST
__all__ = [
    # Classes
    "SimpleBaseProtocol",
    "SimpleConstantProtocol",
    "SimpleObjectProtocol",
    # Instance
    "SimpleInstanceBaseProtocol",
    "SimpleConstantInstanceProtocol",
    # Metadata
    "SimpleBaseMetadataProtocol",
    "SimpleConstantMetadataProtocol",
    "SimpleObjectMetadataProtocol",
    # Methods & Generics
    "ClassMethodProtocol",
    "LogicSignature",
    "P",
    "R",
]