class AenterNotImplemented:
    """
    Vstup do async context manageru (__aenter__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject je synchronní. Async protokoly jsou volitelné
           rozšíření pro specifické use-cases.
    """
    __slots__ = ()

    async def __aenter__(self):
        ...


__DOCT__ = """
**Purpose:**
`__aenter__` is the async counterpart of `__enter__`. It is a coroutine called at the
start of an `async with` block. It can `await` other coroutines (e.g., opening an async
database connection) before returning the resource. Return value is bound to the `as` target.

**Signature:**
```python
async def __aenter__(self):
    await self._open()
    return self
```

**Called automatically when:**
```python
async with obj as resource:   # awaits obj.__aenter__()
    ...
```

**Relationships:**
- Inseparable from `__aexit__`.
- Sync counterpart: `__enter__`.
- Common in async database drivers, HTTP clients, and connection pools.

**Example:**
```python
import asyncio

class AsyncDBConnection:
    async def __aenter__(self):
        print("Opening connection...")
        await asyncio.sleep(0.01)   # simulate async connect
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection...")
        await asyncio.sleep(0.01)   # simulate async close
        return False

async def main():
    async with AsyncDBConnection() as conn:
        print("Working with connection")

asyncio.run(main())
# Opening connection...
# Working with connection
# Closing connection...
```
"""