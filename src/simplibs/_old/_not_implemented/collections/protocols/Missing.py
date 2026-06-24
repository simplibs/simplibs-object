class MissingNotImplemented:
    """
    Fallback pro chybějící klíč v dict (__missing__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: __missing__ funguje jen pro podtřídy dict.
           SimpleObject má vlastní __getitem__ který vyhodí KeyError.
    """
    __slots__ = ()

    def __missing__(self, key):
        ...


"""
collections/Missing.py ❌
Logika: Hook pro dict.__getitem__ když klíč chybí.
Problém: Getitem.py už vyhodí KeyError — __missing__ je volán pouze z dict nativní implementace, ne z custom __getitem__.
Doporučení: Do not_implemented s vysvětlením "Funguje jen pro podtřídy dict, ne custom __getitem__."
"""
# collections/Missing.py
class MissingMixin:
    __slots__ = ()
    def __missing__(self, key):
        # Volá se z __getitem__ pokud klíč neexistuje (dict-like chování)
        # Výchozí: raise KeyError stejně jako dict
        raise KeyError(f"Klíč '{key}' nenalezen v {self.__class__.__name__}")

__DOCT__ = """
**Purpose:**
Called by `dict.__getitem__` (and dict subclasses) when a key is not found, *before*
raising `KeyError`. This is how `collections.defaultdict` works — `__missing__` creates
and returns a default value, and also stores it in the dict. Only useful in dict subclasses;
Python does not call it on arbitrary mapping classes.

**Signature:**
```python
def __missing__(self, key):
    default = self._factory()
    self[key] = default   # optionally store for next access
    return default
```

**Called automatically when:**
```python
# only in dict subclasses:
d = MyDict()
d["nonexistent"]   # calls d.__missing__("nonexistent") before KeyError
```

**Relationships:**
- Only relevant in `dict` subclasses (Python calls it via `dict.__getitem__`).
- This is how `defaultdict` is implemented.
- `__getitem__` is the entry point that leads to `__missing__`.

**Example:**
```python
class AutoList(dict):
    '''A dict that auto-creates empty lists for missing keys.'''
    def __missing__(self, key):
        self[key] = []
        return self[key]

al = AutoList()
al["fruits"].append("apple")
al["fruits"].append("banana")
print(al)   # {'fruits': ['apple', 'banana']}
```
"""