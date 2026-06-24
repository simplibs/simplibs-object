class DelitemNotImplemented:
    """
    Smazání prvku přes index (__delitem__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject je value-based object, ne mutable mapping.
           Použij update_value() pro změny s validací.
    """
    __slots__ = ()

    def __delitem__(self, key):
        ...


"""
collections/Delitem.py ❌
Současný kód:
pythondef __delitem__(self, key):
    raise TypeError(...)
Problém: Atom který vždy vyhodí výjimku není atom — je to blokace.
Doporučení: Do not_implemented s vysvětlením: "SimpleObject není mutable mapping. Použij update_value() pro změny."

"""
class DelitemMixin:
    # Poznámka: SimpleObject není mutable mapping — zvážit zda tohle dává smysl.
    # Možná spíš raise NotImplementedError aby bylo jasné že to systém nepodporuje?
    __slots__ = ()
    def __delitem__(self, key):
        raise TypeError(f"{self.__class__.__name__} nepodporuje mazání prvků")

__DOCT__ = """
**Purpose:**
Defines subscript *deletion*: `del obj[key]`. Completes the mutable container triad.
Raise `KeyError` (mappings) or `IndexError` (sequences) if the key does not exist.

**Signature:**
```python
def __delitem__(self, key) -> None:
    del self._data[key]
```

**Called automatically when:**
```python
del obj[key]     # calls obj.__delitem__(key)
del obj[1:3]     # slice deletion
```

**Relationships:**
- Completes the CRUD triad: `__getitem__` (Read), `__setitem__` (Write), `__delitem__` (Delete).
- Missing partner of `__contains__`, `__len__` in the full MutableMapping protocol.
"""