from .Enter import EnterMixin
from .Exit import ExitMixin

__all__ = (
    "EnterMixin",
    "ExitMixin",
)


__DOCT__ = """
# GROUP: `context/`

> **Group purpose:**
> The context manager protocols — the machinery behind the `with` statement.
> Context managers provide *guaranteed* setup and teardown, regardless of whether the
> body raises an exception. This is the correct, Pythonic alternative to `__del__` for
> resource management. File handles, database connections, locks, and transactions all
> benefit from being used as context managers.
"""