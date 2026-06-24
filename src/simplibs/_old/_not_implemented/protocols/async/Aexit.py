class AexitNotImplemented:
    """
    Výstup z async context manageru (__aexit__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject je synchronní. Async protokoly jsou volitelné
           rozšíření pro specifické use-cases.
    """
    __slots__ = ()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...


__DOCT__ = """
**Purpose:**
`__aexit__` is the async counterpart of `__exit__`. Called at the end of an `async with`
block. Receives the same `(exc_type, exc_val, exc_tb)` arguments as `__exit__`. Can
`await` cleanup coroutines. Return truthy to suppress exceptions; `False`/`None` to
propagate.

**Signature:**
```python
async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
    await self._close()
    return False   # do not suppress exceptions
```

**Called automatically when:**
```python
# at the end of any 'async with' block
async with obj:
    raise ValueError("oops")   # __aexit__ is still called
```

**Relationships:**
- Inseparable from `__aenter__`.
- Sync counterpart: `__exit__`.
- `asynccontextmanager` from `contextlib` provides a generator-based alternative.

---
"""