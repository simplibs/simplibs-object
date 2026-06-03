"""
Konverze jako __ceil__, __floor__, __round__, __int__, __float__, __complex__
— ty by správně neměly vracet NotImplemented při chybě, ale vyhazovat TypeError.
Python runtime totiž NotImplemented z těchto metod neakceptuje a chová se nepředvídatelně.
Zatím to nech jak je, ale tohle bude chtít opravu v dalším kole.

"""


# numeric/conversions/Index.py
class IndexMixin:
    __slots__ = ()
    value: Any

    def __index__(self):
        # Použití objektu jako indexu pole/slice
        # Musí vracet int — pokud value není int, TypeError je správná odpověď
        try:
            return int(self.value)
        except (TypeError, ValueError):
            # runtime neakceptuje NotImplemented z conversion metod.
            # Musí buď vrátit hodnotu, nebo vyhodit TypeError.
            raise TypeError(f"{self.__class__.__name__} nelze použít jako index — value musí být celé číslo")

__DOCT__ = """
**Purpose:**
`__index__` is a *stronger* declaration than `__int__`. It says "this object IS an integer
for all purposes where Python needs a lossless integer" — specifically: sequence indexing
(`list[obj]`), slicing (`list[obj:obj]`), `bin()`, `oct()`, `hex()`, `numpy` array
indexing, and `struct.pack` integer formats. Unlike `__int__`, which can do lossy
conversion (e.g., `float → int`), `__index__` must return an `int` that is
*exactly equivalent* to the object's value.

If your class wraps an integer value with no fractional component, you want `__index__`,
not just `__int__`. Python 3.8+ shows a `DeprecationWarning` if `__int__` is used where
`__index__` is expected.

**Signature:**
```python
def __index__(self) -> int:
    return int(self._value)   # must be lossless
```

**Called automatically when:**
```python
my_list[obj]       # sequence indexing
my_list[obj:obj]   # slicing
bin(obj)           # binary representation
oct(obj)           # octal
hex(obj)           # hexadecimal
operator.index(obj)
```

**Relationships:**
- Stricter superset of `__int__`: if you define `__index__`, Python can derive `__int__`.
- Belongs conceptually next to `numeric/conversions/Int.py`.
- `__int__` allows lossy conversion; `__index__` does not.

**Example:**
```python
class ByteValue:
    '''An integer value guaranteed to fit in one byte (0-255).'''
    def __init__(self, v: int):
        assert 0 <= v <= 255
        self._v = v

    def __index__(self) -> int:
        return self._v

    def __int__(self) -> int:
        return self._v

b = ByteValue(65)
data = [10, 20, 30, 40, 50]
print(data[b])   # 50 — works because __index__ is defined
print(hex(b))    # 0x41
print(bin(b))    # 0b1000001
```
"""