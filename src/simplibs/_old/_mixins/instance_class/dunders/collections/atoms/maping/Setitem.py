"""
collections/Setitem.py ⚠️
Současný kód:
pythondef __setitem__(self, key, value):
    valid_keys = {inner.name_snake for inner in self.meta.inners}
    if key not in valid_keys:
        raise KeyError(...)
    setattr(self, key, value)
Otázka k diskusi: Má SimpleObject podporovat obj['age'] = 31?
Dva přístupy:

Ne — SimpleObject je value-based, změny přes update_value(). → Do not_implemented.
Ano, jako syntaktický cukr — obj['age'] = 31 je zkratka za setattr(obj, 'age', 31). → Nechat.

Můj názor: Pokud obj['age'] vrací hodnotu (přes Getitem), pak by obj['age'] = X mělo fungovat symetricky. → Nechat, ale přejmenovat složku z collections na mapping (protože to je mapping protokol, ne obecné collections).

"""

# collections/Setitem.py
class SetitemMixin:
    # Poznámka: Mutace přes index — pokud chceme mutable mapping, pak:
    __slots__ = ()
    def __setitem__(self, key, value):
        valid_keys = {inner.name_snake for inner in self.meta.inners}
        if key not in valid_keys:
            raise KeyError(f"Prvek '{key}' není definován jako vnitřní součást {self.__class__.__name__}")
        setattr(self, key, value)

__DOCT__ = """
**Purpose:**
Defines subscript *write* access: `obj[key] = value`. Implementing this (alongside
`__getitem__`) makes your class a *mutable* container. You can validate the key or value
here before storing.

**Signature:**
```python
def __setitem__(self, key, value) -> None:
    self._data[key] = value
```

**Called automatically when:**
```python
obj[key] = value   # calls obj.__setitem__(key, value)
obj[1:3] = [a, b]  # slice assignment
```

**Relationships:**
- Paired with `__getitem__` (readable) and `__delitem__` (deletable).
- Together with `__getitem__`, forms the minimum mutable mapping/sequence protocol.
"""