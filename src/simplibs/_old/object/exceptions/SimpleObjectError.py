from simplibs.exception import SimpleException

class SimpleObjectError(SimpleException):
    """Základní výjimka pro celou knihovnu SimpleObject."""
    _skip_locations = ("simplibs/object",)

_DESIGN_NOTES = """
# SimpleObjectError

## Účel
Hlavní zastřešující výjimka pro celý ekosystém `SimpleObject`. 
Neslouží k přímému vyvolávání, ale jako společný předek pro všechny chyby knihovny.

## Skupina
Umožňuje uživateli zachytit jakýkoliv problém spojený s touto knihovnou:
```python
except SimpleObjectError:
    # řešení jakékoliv chyby v SimpleObject
"""