# context/Exit.py
class ExitMixin:
    # Poznámka: základní implementace — žádné transakční chování.
    # Pokud chceme rollback při výjimce, uživatel přepíše.
    __slots__ = ()
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False  # Neignorujeme výjimky

__DOCT__ = """
**Purpose:**
`__exit__` is called when the `with` block ends — whether normally or due to an exception.
It receives the exception info: `(None, None, None)` if no exception, or
`(type, value, traceback)` if one occurred. Return a truthy value to *suppress* the
exception (rarely desired); return `False` or `None` to let it propagate.

**Signature:**
```python
def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
    self._teardown()
    if exc_type is ValueError:
        return True   # suppress ValueError
    return False      # let other exceptions propagate
```

**Called automatically when:**
```python
# at the end of any 'with' block, exception or not
with obj:
    raise ValueError("oops")   # __exit__ receives the exception info
```

**Relationships:**
- Inseparable from `__enter__`.
- The three arguments match `sys.exc_info()` format.
- Async counterpart: `__aexit__`.

**Example:**
```python
class DatabaseTransaction:
    def __init__(self, conn): self.conn = conn

    def __enter__(self):
        self.conn.begin()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        return False   # never suppress exceptions here
```
"""