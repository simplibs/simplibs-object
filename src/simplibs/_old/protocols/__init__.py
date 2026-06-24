# 1. IMPORTY PROTOKOLŮ (Pro běh i pro typy)
from .classes import (
    SimpleMetaProtocol,
    SimpleBaseProtocol,
    SimpleConstantProtocol,
    SimpleObjectProtocol,
)
from .instance import (
    SimpleInstanceBaseProtocol,
    SimpleAtomInstanceProtocol,
    SimpleCompositeInstanceProtocol,
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

# 2. IMPORTY ČISTÝCH TYPŮ (Zcela napřímo!)
# Protože spodní init v types/ už má v sobě TYPE_CHECKING ochranu,
# tento import je zde v runtime naprosto bezpečný a čistý.
from .types import SimpleClassType, SimpleInstanceType, SimpleMetadataType

# 3. EXPORT MANIFEST
__all__ = [
    # Classes
    "SimpleBaseProtocol",
    "SimpleConstantProtocol",
    "SimpleObjectProtocol",
    # Instance
    "SimpleInstanceBaseProtocol",
    "SimpleAtomInstanceProtocol",
    "SimpleCompositeInstanceProtocol",
    # Metadata
    "SimpleMetaProtocol",
    "SimpleBaseMetadataProtocol",
    "SimpleConstantMetadataProtocol",
    "SimpleObjectMetadataProtocol",
    # Methods & Generics
    "ClassMethodProtocol",
    "LogicSignature",
    "P",
    "R",
    # Pure Types
    "SimpleClassType",
    "SimpleInstanceType",
    "SimpleMetadataType"
]