from typing import Any


class GetitemMixin:
    """
    Přístup k vnitřním prvkům přes indexování obj['name'].
    """

    # Očekává
    meta: Any


    def __getitem__(self, key: str) -> Any:
        """Umožňuje přístup jako k dict: obj['age']."""
        valid_keys = {inner.name_snake for inner in self.meta.inners}

        if key not in valid_keys:
            raise KeyError(f"Prvek '{key}' není definován jako vnitřní součást {self.__class__.__name__}")

        return getattr(self, key)



__DOCT__ = """
**Purpose:**
Defines subscript read access: `obj[key]`. For sequences, `key` is an `int` or `slice`.
For mappings, `key` can be any hashable. This is also the hook Python uses for iteration
fallback: if `__iter__` is absent but `__getitem__` is defined, Python calls
`__getitem__(0)`, `__getitem__(1)`, etc., until `IndexError` is raised.

**Signature:**
```python
def __getitem__(self, key):
    if isinstance(key, slice):
        return type(self)(self._data[key])
    return self._data[key]
```

**Called automatically when:**
```python
obj[key]          # read access
obj[1:5]          # slice access — key is a slice object
for x in obj:     # iteration fallback (if __iter__ absent)
```

**Relationships:**
- Paired with `__setitem__` and `__delitem__` for mutable containers.
- If `__iter__` is absent, Python uses `__getitem__` starting at index 0.
- `__missing__` is called (on dict subclasses) when the key is not found.
- `__class_getitem__` is the class-level analogue for generics.

**Example:**
```python
class TimeSeries:
    def __init__(self, data): self._data = data

    def __getitem__(self, key):
        if isinstance(key, slice):
            return TimeSeries(self._data[key])
        return self._data[key]

ts = TimeSeries([10, 20, 30, 40, 50])
print(ts[2])       # 30
print(ts[1:3])     # TimeSeries([20, 30])
```
"""