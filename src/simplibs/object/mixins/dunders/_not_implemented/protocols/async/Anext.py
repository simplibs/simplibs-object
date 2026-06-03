class AnextNotImplemented:
    """
    Async next prvek (__anext__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject není async iterator. Nemá stavovou async iteraci.
    """
    __slots__ = ()

    async def __anext__(self):
        ...


__DOCT__ = """
**Purpose:**
`__anext__` is the async counterpart of `__next__`. It must be a coroutine (async method)
that returns the next value or raises `StopAsyncIteration` (NOT `StopIteration`) when
exhausted. Python 3.7+ explicitly forbids `StopIteration` inside coroutines, so this
distinction matters.

**Signature:**
```python
async def __anext__(self):
    value = await self._fetch_next()
    if value is None:
        raise StopAsyncIteration
    return value
```

**Called automatically when:**
```python
async for item in async_iter:   # Python awaits __anext__() each iteration
```

**Relationships:**
- Paired with `__aiter__`.
- Must raise `StopAsyncIteration` (not `StopIteration`) to signal end.
- Sync counterpart: `__next__`.

**Example:**
```python
import asyncio

class AsyncRange:
    def __init__(self, n): self.n, self.current = n, 0

    def __aiter__(self): return self

    async def __anext__(self):
        if self.current >= self.n:
            raise StopAsyncIteration
        await asyncio.sleep(0)   # simulate async work
        value = self.current
        self.current += 1
        return value

async def main():
    async for n in AsyncRange(3):
        print(n)   # 0, 1, 2

asyncio.run(main())
```
"""