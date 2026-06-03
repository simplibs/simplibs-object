class NextNotImplemented:
    """
    Iterator protokol - další prvek (__next__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject je Iterable (má __iter__), ne Iterator (stavový).
           __iter__ vrací fresh iterátor, objekt sám nemá iterační stav.
    """
    __slots__ = ()

    def __next__(self):
        ...



__DOCT__ = """
**Purpose:**
`__next__` produces the next value from an iterator. When the sequence is exhausted,
it must raise `StopIteration` — this is how Python knows to exit the `for` loop.
Raising `StopIteration` inside a generator is equivalent and handled automatically.
Once exhausted, an iterator should continue raising `StopIteration` on all subsequent
calls (not reset).

**Signature:**
```python
def __next__(self):
    if self._exhausted:
        raise StopIteration
    value = self._current
    self._advance()
    return value
```

**Called automatically when:**
```python
next(iterator)      # explicit, calls iterator.__next__()
for x in iterator:  # Python calls next() repeatedly until StopIteration
```

**Relationships:**
- Always paired with `__iter__` — you cannot have a valid iterator without both.
- `StopIteration` is the sentinel, not a real error — never suppress it inside generators (Python 3.7+).
- Async counterpart: `__anext__`.

**Example:**
```python
class Fibonacci:
    def __init__(self, limit):
        self.limit = limit
        self.a, self.b = 0, 1

    def __iter__(self): return self

    def __next__(self):
        if self.a > self.limit:
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        return value

print(list(Fibonacci(100)))   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```
"""