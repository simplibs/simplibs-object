from .SimpleBaseProtocol import SimpleBaseProtocol
from .SimpleConstantProtocol import SimpleConstantProtocol
from .SimpleObjectProtocol import SimpleObjectProtocol

# Prvek definující největší množinu (superset pro anotace)
SimpleClassLike = SimpleObjectProtocol

# Prvek definující nejmenší množinu (minimální rozhraní pro ověření typu)
SimpleClassType = SimpleBaseProtocol