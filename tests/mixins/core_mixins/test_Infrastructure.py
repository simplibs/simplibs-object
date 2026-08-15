from .NodesDicts import NodesDicts
from .Snapshot import Snapshot

class Infrastructure(NodesDicts, Snapshot):
    """
    Společné infrastrukturní zázemí (uzly a snapshoty) vyžadované
    pro logiky neměnnosti, serializace a reaktivního volání.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = ()