import logging
from typing import Any, TYPE_CHECKING, Callable
# Annotations
if TYPE_CHECKING:
    from .._core.protocols.classes import SimpleClassType


# ----------------------------------------
# Internal library logger
# ----------------------------------------
_logger = logging.getLogger("simple")


# ----------------------------------------
# Optional callback for reacting to value changes
# ----------------------------------------
# Usage:
#     import simplibs.object.settings.logging as simple_logging
#     simple_logging.on_value_change = lambda cls, value, event: ...
on_value_change: Callable[["SimpleClassType", Any, str], None] | None = None


# ----------------------------------------
# Central logging entry point
# ----------------------------------------
def log_value_event(
    cls: "SimpleClassType",
    value: Any,
    event: str
) -> None:
    """
    Centralized logging function used by the entire Simple library.

    Logs the event through the internal stdlib logger and optionally
    triggers a user-defined callback.
    """

    # 1. Stdlib logging
    if _logger.isEnabledFor(logging.DEBUG):
        _logger.debug(
            "[%s] %s = %r",
            event,
            cls.__name__,
            value
        )

    # 2. Optional user callback
    if on_value_change is not None:
        # noinspection PyCallingNonCallable
        on_value_change(cls, value, event)


_DESIGN_NOTES = """
# Logging Subsystem

## Purpose
Provides a minimal, safe, and idiomatic logging interface for the Simple
object library. It integrates with Python’s standard logging module and
offers an optional callback mechanism for advanced users who want to react
to value changes inside Simple objects.

This module is intentionally lightweight and follows best practices used by
major Python libraries (requests, sqlalchemy, pydantic, fastapi).

---

## Architectural Role
The logging subsystem serves two purposes:

1. **Internal diagnostics**
   - All internal logging goes through a single logger: `"simple"`.
   - The library never configures handlers or levels — users control logging.

2. **User-defined reactions**
   - The `on_value_change` callback allows users to hook into value changes
     for debugging, monitoring, auditing, or custom behavior.

This design keeps the library predictable and non-intrusive while still
providing powerful extension points.

---

## Components

| Component               | Type     | Description                                                        |
| :---------------------- | :--------| :----------------------------------------------------------------- |
| `_logger`               | Logger   | Internal stdlib logger (`logging.getLogger("simple")`).            |
| `on_value_change`       | Callable | Optional callback triggered on value changes.                      |
| `log_value_event`       | Function | Central logging entry point used by the entire library.            |

---

## Usage Examples

### Enable debug logging
```python
import logging
logging.getLogger("simple").setLevel(logging.DEBUG)
```

### Add a custom handler
```python
handler = logging.FileHandler("simple.log")
logging.getLogger("simple").addHandler(handler)
```

### Register a callback
```python
import simplibs.object.settings.logging as simple_logging

def my_callback(cls, value, event):
    print(f"{cls.__name__}: {event} -> {value}")

simple_logging.on_value_change = my_callback
```

### What gets logged?
Any event triggered by Simple objects, such as:

- value assignment
- recalculation
- stepping
- normalization
- validation

---

## Notes
- The library **never** configures logging automatically.
- The library **never** modifies the root logger.
- The library **never** installs handlers.
- All logging is opt-in and fully controlled by the user.
- The callback mechanism is optional and disabled by default.
- This module is internal but safe to import and configure by users.

This subsystem is intentionally minimalistic, predictable, and fully aligned
with Python’s logging best practices.
"""