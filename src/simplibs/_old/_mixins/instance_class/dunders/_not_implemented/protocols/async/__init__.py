

__DOCT__ = """
# GROUP: `async/`

> **Group purpose:**
> The asynchronous variants of the iteration and context manager protocols.
> These are used exclusively inside `async def` coroutines with `async for`,
> `async with`, and `await`. Each async dunder is the exact async counterpart of a
> sync dunder, following the same logic but returning awaitables/async iterators
> instead of regular values.
"""