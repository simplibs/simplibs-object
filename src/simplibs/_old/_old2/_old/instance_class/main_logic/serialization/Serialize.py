from datetime import datetime, date
from pathlib import Path
from enum import Enum


# serialization/Serialize.py
class SerializeValueMixin:
    """Serializace hodnot objektu do dict-kompatibilní podoby."""
    __slots__ = ()

    def _serialize_value(self, value, _seen=None):
        """Převede hodnotu na JSON-serializovatelnou formu."""
        # Kontrola cyklické rekurze
        if _seen is None:
            _seen = set()

        obj_id = id(value)
        if obj_id in _seen:
            raise ValueError("Circular reference detected during serialization")
        _seen.add(obj_id)

        # JSON primitivy
        if isinstance(value, (str, int, float, bool, type(None))):
            return value

        # Kolekce
        if isinstance(value, (list, tuple, set)):
            return [self._serialize_value(v, _seen) for v in value]

        if isinstance(value, dict):
            return {str(k): self._serialize_value(v, _seen) for k, v in value.items()}

        # Běžné deterministické typy
        if isinstance(value, (datetime, date)):
            return value.isoformat()

        if isinstance(value, Path):
            return str(value)

        if isinstance(value, Enum):
            return value.value

        # Explicitní kontrakt — pokus o to_dict s _seen
        if callable(getattr(value, "to_dict", None)):
            try:
                return value.to_dict(_seen=_seen)
            except TypeError:
                # Objekt nepodporuje _seen, zavoláme bez něj
                return value.to_dict()

        raise TypeError(
            f"Object of type {type(value).__name__} is not serializable. "
            "Override _serialize_value() to support this type."
        )

"""
1) Analýza SerializeValueMixin
Tento mixin je skvělý v tom, že řeší největší noční můru serializace: Cyklické reference.

Co je vynikající:

Detekce cyklů (_seen): Použití id(value) a setu je standardní a bezpečný způsob, jak zabránit nekonečné rekurzi.

ISO formát: Použití .isoformat() pro data je nejlepší praxe (standard RFC 3339).

Kontrakt to_dict: To, že zkoušíš volat to_dict na vnořených objektech, umožňuje tvým SimpleObjectům krásně spolupracovat v hlubokých strukturách.

Na co si dát pozor:

Transformace klíčů v dictu: str(k): ... – To je rozumné pro JSON (který vyžaduje stringové klíče), ale pokud má uživatel v dictu jako klíče integery a chce je zachovat i po serializaci (třeba pro interní potřeby), tato transformace je nevratná.

Mutable default: _seen=None a následné vytvoření setu je správně. Jen pamatuj, že při volání to_dict zvenčí bude muset uživatel vědět, že má začít s prázdným setem, nebo to nechat na tvém mixinu.
"""