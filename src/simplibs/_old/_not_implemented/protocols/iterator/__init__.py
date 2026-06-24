

__DOCT__ = """
# GROUP: `iteration/`

> **Group purpose:**
> The iterator protocols — the mechanism behind `for` loops, list comprehensions,
> `zip()`, `map()`, `filter()`, and any other construct that consumes a sequence lazily.
> Python distinguishes between *iterables* (things you can iterate over, define `__iter__`)
> and *iterators* (stateful cursors that produce one value at a time, define both
> `__iter__` and `__next__`). An iterable produces fresh iterators; an iterator IS
> the cursor and is typically exhausted after one pass.
"""