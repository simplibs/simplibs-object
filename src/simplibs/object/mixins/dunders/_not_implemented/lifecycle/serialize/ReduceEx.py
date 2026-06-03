class ReduceExNotImplemented:
    """
    Rozšířený pickle protokol (__reduce_ex__).

    V SimpleObject: NEIMPLEMENTOVÁNO (stačí __reduce__)
    Důvod: Python automaticky volá __reduce__ pokud __reduce_ex__ chybí.
           __reduce__ poskytuje dostatečnou funkcionalitu.
    """
    __slots__ = ()

    def __reduce_ex__(self, protocol):
        ...


__DOCT__ = """
**Purpose:**
`__reduce_ex__` is the *protocol-aware* version of `__reduce__`. It receives the pickle
protocols version (an integer, currently 0–5 in CPython) and can tailor the serialization
format accordingly. Python always calls `__reduce_ex__` first; it only falls back to
`__reduce__` if `__reduce_ex__` is not defined. The default implementation in `object`
already handles most cases through `__getstate__` / `__setstate__`.

**Signature:**
```python
def __reduce_ex__(self, protocol: int):
    return (self.__class__, (self.value,))
```

**Called automatically when:**
```python
import pickle
data = pickle.dumps(obj, protocol=5)   # calls __reduce_ex__(5)
```

**Relationships:**
- Supersedes `__reduce__` — define one or the other, not both.
- Works with `__getstate__` / `__setstate__` for state-based serialization.

**Example:**
```python
import pickle

class Versioned:
    def __init__(self, value):
        self.value = value

    def __reduce_ex__(self, protocol):
        print(f"Pickling with protocols {protocol}")
        return (Versioned, (self.value,))

v    = Versioned(42)
data = pickle.dumps(v, protocol=4)   # prints "Pickling with protocols 4"
v2   = pickle.loads(data)
print(v2.value)  # 42
```
"""