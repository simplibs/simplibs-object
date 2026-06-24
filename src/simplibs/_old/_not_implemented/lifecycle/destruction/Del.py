class DelNotImplemented:
    """
    Destruktor instance (__del__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: __del__ je nepředvídatelný v Pythonu (garbage collection).
           Může způsobit memory leaks a nedeterministické chování.
    """
    __slots__ = ()

    def __del__(self):
        ...


__DOCT__ = """
**Purpose:**
`__del__` is the *finalizer* (not to be confused with the `del` statement). It is called
by the garbage collector when the object's reference count drops to zero and it is about
to be reclaimed. It gives you one last chance to release external resources — file handles,
network connections, locks — though for this purpose `__exit__` (context managers) is
almost always preferred because it guarantees deterministic execution.

`__del__` is **not** guaranteed to be called at all: circular references can prevent it,
and at interpreter shutdown it may never run. Never rely on it for critical cleanup.

**Signature:**
```python
def __del__(self) -> None:
    # cleanup code
    pass
```

**Called automatically when:**
```python
del obj           # decrements ref count; if it hits 0, __del__ fires
# or simply when the object goes out of scope and is collected
```

**Relationships:**
- Counterpart of `__init__` / `__new__`.
- For deterministic cleanup, prefer `__enter__` / `__exit__` (context manager protocol).
- Interacts with `__reduce__` / `__getstate__` in serialization: if an object is
  unpickled and then collected, `__del__` fires on the reconstructed object.

**Example:**
```python
class ManagedResource:
    def __init__(self, name):
        self.name = name
        print(f"Acquired: {self.name}")

    def __del__(self):
        print(f"Released: {self.name}")   # not guaranteed to run!

r = ManagedResource("db_connection")
del r   # prints "Released: db_connection" (in CPython; not guaranteed elsewhere)
```
"""