# context/Enter.py
class EnterMixin:
    __slots__ = ()
    def __enter__(self):
        return self

__DOCT__ = """
**Purpose:**
`__enter__` is called at the start of a `with` block. Its return value is bound to the
`as` target (if provided). The method can return `self` (when the object itself is the
resource) or any other value (when you want to expose a different interface inside the block).

**Signature:**
```python
def __enter__(self):
    self._setup()
    return self   # or return some other object
```

**Called automatically when:**
```python
with obj as x:   # calls obj.__enter__(), binds result to x
    ...
with obj:        # return value discarded if no 'as'
    ...
```

**Relationships:**
- Inseparable from `__exit__` — you must always define both.
- Async counterpart: `__aenter__`.
- The `contextlib.contextmanager` decorator provides an alternative generator-based approach.

**Example:**
```python
class Timer:
    import time

    def __enter__(self):
        self._start = self.time.time()
        return self   # expose self for access inside the block

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = self.time.time() - self._start
        print(f"Elapsed: {elapsed:.3f}s")
        return False   # do not suppress exceptions

with Timer() as t:
    sum(range(10_000_000))
# prints: Elapsed: 0.234s (approximately)
```
"""