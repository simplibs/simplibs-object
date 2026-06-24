class AiterNotImplemented:
    """
    Async iterátor (__aiter__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject je synchronní. Async iterace není podporována
           v základní implementaci.
    """
    __slots__ = ()

    def __aiter__(self):
        ...


__DOCT__ = """
**Purpose:**
`__aiter__` is the async counterpart of `__iter__`. It must return an *async iterator*
object — an object with `__aiter__` and `__anext__`. Called by `async for` to obtain
the iterator before the loop begins. Unlike sync `__iter__`, this method itself is
typically *not* async (it should return the async iterator immediately, not await anything).

**Signature:**
```python
def __aiter__(self):
    return self   # if self is also the async iterator (has __anext__)
    # or return AsyncIteratorObject(self._data)
```

**Called automatically when:**
```python
async for item in obj:   # calls obj.__aiter__() first
```

**Relationships:**
- Paired with `__anext__` — cannot have one without the other.
- Sync counterpart: `__iter__`.
- For simple cases, use `async def __aiter__` is NOT needed — plain `def` returning an async iterator object.
"""