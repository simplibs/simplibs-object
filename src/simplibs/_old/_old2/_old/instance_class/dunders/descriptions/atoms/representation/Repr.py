from typing import Any


class ReprMixin:
    """
    Technická reprezentace objektu (__repr__).
    """
    __slots__ = ()
    value: Any

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"



__DOCT__ = """
**Purpose:**
Defines the *developer/debugging* string representation. Should ideally be an expression
that — when passed to `eval()` — reconstructs the object (though this is aspirational for
complex objects). It is shown in the REPL, in containers (`print([obj])`), in tracebacks
(`%r` format spec), and with `repr(obj)`. **If you only define one string method, define
`__repr__`** — it is the universal fallback.

**Signature:**
```python
def __repr__(self) -> str:
    return f"{type(self).__name__}({self.value!r})"
```

**Called automatically when:**
```python
repr(obj)          # explicit
# REPL: evaluating an expression that returns obj
[obj]              # repr used inside container __repr__
f"{obj!r}"         # explicit repr in f-string
"%r" % obj         # old-style format
```

**Relationships:**
- Universal fallback: if `__str__` is missing, `str(obj)` uses `__repr__`.
- If `__repr__` is missing too, Python uses `<ClassName object at 0x...>`.
- `__str__` is the user-facing counterpart.
"""