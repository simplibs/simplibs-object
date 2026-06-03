from typing import Type, TYPE_CHECKING, Any
# Inners
from .SimpleMetaType import SimpleMetaType


# 1. Definice pro typovou kontrolu
if TYPE_CHECKING:

    # 1.1 Vnitřní import tříd
    from ...SimpleBase import SimpleBase
    from ...SimpleConstant import SimpleConstant
    from ...SimpleObject import SimpleObject

    # 1.2 Typ reprezentující konkrétní instance (např. moje_auto)
    SimpleInstanceType = SimpleBase | SimpleConstant | SimpleObject

    # 1.3 Typ reprezentující samotné základní třídy, které mají metadata UNSET (např. SimpleBase, SimpleConstant, SimpleObject)
    BaseSimpleClassType = Type[SimpleBase] | Type[SimpleConstant] | Type[SimpleObject]

    # 1.4 Typ reprezentující Ddefiniční třídy, které už mají metadata (např. Auto, Motorka)
    class SimpleClassType(BaseSimpleClassType):
        meta: SimpleMetaType

    # 1.5 Typ reprezentující vytvořenou instanci
    class SimpleObjectInstanceType(SimpleClassType):
        _value: Any

# 2. Definice pro běh
else:
    SimpleInstanceType = Any
    BaseSimpleClassType = type
    SimpleClassType = type
