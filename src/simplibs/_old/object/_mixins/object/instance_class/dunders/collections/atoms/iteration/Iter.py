from typing import Iterator, Any


class IterMixin:
    """
    Iterace přes jména vnitřních prvků (inners).
    """

    # Očekává
    meta: Any

    def __iter__(self) -> Iterator[str]:
        """Iterace přes jména vnitřních prvků."""
        if not self.meta.inners:
            return iter([])
        return iter(inner.name_snake for inner in self.meta.inners)



__DOCT__ = """
**Purpose:**
`__iter__` must return an *iterator* object — an object with a `__next__` method.
For collections, `__iter__` returns a fresh iterator each time (so you can iterate
multiple times independently). For iterators themselves, `__iter__` returns `self`
(so they work in `for` loops directly). This is the foundation of Python's iteration
protocol.

**Signature:**
```python
# On a collection (iterable):
def __iter__(self):
    return iter(self._data)   # or MyIterator(self._data)

# On an iterator itself:
def __iter__(self):
    return self   # iterators return themselves
```

**Called automatically when:**
```python
for item in obj:    # Python calls iter(obj), which calls obj.__iter__()
list(obj)           # any consumption via for-loop protocol
zip(obj, other)
[x for x in obj]
```

**Relationships:**
- `__next__` is its inseparable partner on the iterator side.
- If `__iter__` is absent but `__getitem__` is present, Python creates an automatic
  index-based iterator (legacy fallback).
- Async counterpart: `__aiter__`.

**Example:**
```python
class CountDown:
    def __init__(self, start): self.start = start

    def __iter__(self):
        return CountDownIterator(self.start)

class CountDownIterator:
    def __init__(self, n): self.n = n

    def __iter__(self): return self   # iterators return self

    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

for n in CountDown(3):
    print(n)   # 3, 2, 1
```
"""