class LengthHintNotImplemented:
    """
    Hint pro optimalizaci délky iterátoru (__length_hint__).

    V SimpleObject: NEIMPLEMENTOVÁNO (redundantní s __len__)
    Důvod: Python automaticky použije __len__ jako fallback.
           Explicitní __length_hint__ není potřeba.
    """
    __slots__ = ()

    def __length_hint__(self):
        ...


"""
collections/LengthHint.py ⚠️
Logika: Hint pro iterátor — stejné jako __len__.
Problém: Redundantní s Len.py. Python použije __len__ jako fallback, pokud __length_hint__ chybí.
Doporučení: Přesunout do not_implemented s vysvětlením "Python automaticky odvozuje z __len__".

"""


# collections/LengthHint.py
class LengthHintMixin:
    __slots__ = ()
    def __length_hint__(self) -> int:
        # Hint pro iterátory — defaultně stejné jako __len__
        if hasattr(self, "meta") and self.meta.inners:
            return len(self.meta.inners)
        return 0

__DOCT__ = """
**Purpose:**
`__length_hint__` is an *optional performance hint* — it tells Python approximately
how many items an iterator will yield, without requiring an exact answer. Python uses
this to pre-allocate memory when consuming iterators into lists (`list(it)`) or when
calling `operator.length_hint(it)`. If the hint is wrong, nothing breaks — it is purely
an optimization.

Contrast with `__len__`: `__len__` must be exact and non-negative; `__length_hint__` may
be an estimate and may return 0 when the true length is unknown.

**Signature:**
```python
def __length_hint__(self) -> int:
    return max(0, self._estimated_remaining)   # approximate is fine
```

**Called automatically when:**
```python
import operator
operator.length_hint(obj)   # direct call
list(obj)                   # Python uses it internally for pre-allocation
```

**Relationships:**
- `__len__` takes precedence: if defined, `length_hint()` uses `__len__`.
- Only useful on *iterators* (not on collections — those should define `__len__`).
- Used by CPython's list/tuple construction code as a memory pre-allocation hint.

**Example:**
```python
class ChunkedReader:
    def __init__(self, chunks):
        self._chunks = iter(chunks)
        self._remaining = len(chunks)

    def __iter__(self): return self

    def __next__(self):
        self._remaining = max(0, self._remaining - 1)
        return next(self._chunks)

    def __length_hint__(self) -> int:
        return self._remaining   # approximate — fine if wrong

reader = ChunkedReader(range(1000))
result = list(reader)   # CPython pre-allocates ~1000 slots, avoids repeated resizing
```
"""