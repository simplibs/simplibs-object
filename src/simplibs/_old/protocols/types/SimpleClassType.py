# Outers
from ..classes import (
    SimpleConstantProtocol,
    SimpleObjectProtocol
)


# Typový alias pro základní třídy
SimpleClassType = SimpleObjectProtocol | SimpleConstantProtocol
