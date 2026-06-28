from .core_classes import InstanceBaseProtocol, AtomInstanceProtocol, CompositeInstanceProtocol
from .SimpleInstanceBaseProtocol import SimpleInstanceBaseProtocol
from .SimpleConstantInstanceProtocol import SimpleConstantInstanceProtocol
from .SimpleObjectInstanceProtocol import SimpleObjectInstanceProtocol

# Prvek definující největší množinu (superset pro anotace)
SimpleInstanceClassLike = CompositeInstanceProtocol
SimpleInstanceLike = SimpleObjectInstanceProtocol

# Prvek definující nejmenší množinu (minimální rozhraní pro ověření typu)
SimpleInstanceClassType = AtomInstanceProtocol
SimpleInstanceType = SimpleConstantInstanceProtocol