_DESIGN_NOTES = """
Settings subsystem for the Simple object library.

This package contains optional configuration modules that allow users to
customize certain aspects of the library’s behavior. The subsystem is
minimal by design and follows Python best practices for non-intrusive
configuration.

Available modules:

- logging: Provides the internal library logger and an optional callback
           for reacting to value changes inside Simple objects.

Usage example:

    import simplibs.object.settings.logging as simple_logging

    # Enable debug logging
    import logging
    logging.getLogger("simple").setLevel(logging.DEBUG)

    # Register a callback
    simple_logging.on_value_change = lambda cls, value, event: print(
        f"{cls.__name__}: {event} -> {value}"
    )

## Purpose
The settings subsystem provides optional configuration modules for the
Simple object library. It is intentionally minimal and non-intrusive,
following best practices used by major Python libraries.

The subsystem does not define global configuration classes or mutable
singletons. Instead, it exposes small, focused modules that users may
import and configure explicitly.

---

## Structure

| Module   | Description                                                        |
| :--------| :----------------------------------------------------------------- |
| logging  | Internal logger + optional callback for reacting to value changes. |

The subsystem may be extended in the future with additional modules
(e.g., debugging, profiling), but the current design keeps it lightweight
and easy to understand.

---

## Philosophy

### 1. Explicit configuration
Users configure settings explicitly:

```python
import simplibs.object.settings.logging as simple_logging
simple_logging.on_value_change = ...
```

No hidden global state, no implicit initialization.

### 2. Non-intrusive behavior
The library never:

- configures logging handlers,
- modifies the root logger,
- sets logging levels,
- installs global hooks.

Users retain full control.

### 3. Minimal surface area
The `settings` package does not reexport modules.  
This avoids ambiguity and keeps imports explicit:

```python
from simplibs.object.settings import logging  # discouraged
from simplibs.object.settings import logging as simple_logging  # explicit
```

Explicit imports make the subsystem easier to maintain and reason about.

---

## Notes
- The subsystem is internal but safe for users to import.
- Modules inside `settings` are stable and predictable.
- The design avoids global mutable configuration objects.
- Logging is the only settings module currently provided.
"""