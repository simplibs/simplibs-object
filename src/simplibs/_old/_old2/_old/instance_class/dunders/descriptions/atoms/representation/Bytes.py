from typing import Any
from ....methods.modificators.ModifyInstance import ModifyInstance

__all__ = ["BytesMixin"]

class BytesMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __bytes__(self):
        try:
            return bytes(self.value)
        except (TypeError, ValueError):
            # runtime neakceptuje NotImplemented z conversion metod.
            # Musí buď vrátit hodnotu, nebo vyhodit TypeError.
            raise TypeError(f"Nelze převést {self.__class__.__name__} na int: {e}")


__DOCT__ = """
**Purpose:**
Defines `bytes(obj)`. This is the byte-string equivalent of `__str__`. It should return
a `bytes` object representing the object's binary form — useful for network protocols,
binary file formats, and serialization. Note that `bytes(obj)` calls `__bytes__` only if
the argument is not an integer or iterable; for general-purpose use, `__reduce__` /
`__getstate__` (pickle) is more common.

**Signature:**
```python
def __bytes__(self) -> bytes:
    return self.value.encode("utf-8")
```

**Called automatically when:**
```python
bytes(obj)   # calls obj.__bytes__()
```

**Relationships:**
- The binary counterpart of `__str__`.
- For serialization to bytes with reconstruction support, prefer `__reduce__` / `__getstate__`.

**Example:**
```python
class Packet:
    def __init__(self, data: str):
        self.data = data

    def __bytes__(self) -> bytes:
        payload = self.data.encode("utf-8")
        length  = len(payload).to_bytes(4, "big")
        return length + payload

p = Packet("hello")
print(bytes(p))   # b'\x00\x00\x00\x05hello'
```

"""