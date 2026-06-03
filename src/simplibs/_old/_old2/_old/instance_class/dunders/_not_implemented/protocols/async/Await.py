class AwaitNotImplemented:
    """
    Awaitable protokol (__await__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject není coroutine. Pro async operace použij
           dedikovaný async wrapper.
    """
    __slots__ = ()

    def __await__(self):
        ...


__DOCT__ = """
**Purpose:**
`__await__` makes an object *awaitable* — usable with the `await` keyword. It must return
an *iterator* (not an async iterator) that drives the coroutine machinery. In practice,
you almost never implement this directly — Python coroutines (`async def` functions),
`asyncio.Future`, and `asyncio.Task` implement it for you. You would implement it only
when building custom low-level awaitable types (e.g., for a custom event loop or for
wrapping C extensions).

**Signature:**
```python
def __await__(self):
    # must return an iterator (sync, not async)
    # e.g., yield from asyncio.Future.__await__(self)
    return (yield from self._future.__await__())
```

**Called automatically when:**
```python
await obj   # Python calls obj.__await__() to get the iterator
```

**Relationships:**
- Enables `await` syntax; the object becomes an *awaitable*.
- `__aiter__` / `__anext__` are for async iteration (different concept).
- `asyncio.Future`, `asyncio.Task`, and coroutines define this internally.

**Example:**
```python
import asyncio

class SleepFor:
    def __init__(self, seconds): self.seconds = seconds
    def __await__(self):
        return asyncio.sleep(self.seconds).__await__()

async def main():
    await SleepFor(0.1)
    print("Done sleeping!")

asyncio.run(main())
```
"""