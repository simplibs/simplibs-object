from typing import Any, NoReturn
# Outers
from ......exceptions import SimpleRuntimeError


def raise_locked_value_error(
    value: Any,
    class_name: str,
) -> NoReturn:

    raise SimpleRuntimeError(
        error_name="VALUE LOCKED",
        label="value_is_locked",
        expected="Unlocked instance",
        value=value,
        problem=(
            f"Instance '{class_name}' is locked and its value "
            f"cannot be modified."
        ),
        context=f"{class_name}.value = {value}",
        how_to_fix=(
            "Unlock the instance before modifying its value.",
            "If the instance uses the Permission mixin, call:",
            "    obj.unlock()",
            "",
            "If the instance exposes '_locked' directly, set:",
            "    obj._locked = False",
        ),
        exception=AttributeError,
    )


_DESIGN_NOTES = """
# Locked Value Error — SimpleRuntimeError

## Purpose
This error is raised when a user attempts to modify the value of a Simple
instance that is currently locked. Locking is a user‑controlled mechanism that
prevents further mutation of the instance’s value. It is implemented through the
`Permission` mixin or by directly manipulating the `_locked` attribute.

The error is part of the public-facing logic layer and therefore uses
`SimpleRuntimeError`.

---

## Why This Error Exists
Simple instances normally allow value mutation (unless immutable). However,
developers may choose to temporarily or permanently lock an instance to prevent
accidental changes. This is especially useful in:

- configuration objects,
- computed composite values,
- runtime snapshots,
- safety-critical workflows.

The `_locked` flag is intentionally simple: a single boolean checked in every
value setter. This avoids complex mixin logic and ensures that locking works
uniformly across atomic and composite instances.

---

## How Locking Works
Locking is typically controlled via the `Permission` mixin:

```python
obj.lock()
obj.value = 10  # → raises SimpleRuntimeError
```

The mixin exposes:

- `is_locked` — read-only property,
- `lock()` — sets `_locked = True`,
- `unlock()` — sets `_locked = False`.

Alternatively, advanced users may manipulate `_locked` directly.

---

## When It Occurs
The error is raised whenever:

1. The instance’s `_locked` flag is `True`.
2. A value setter (root or inner) is invoked.
3. The setter detects the locked state and aborts the mutation.

This applies to:

- atomic instances,
- composite instances,
- inner value setters,
- root value setters.

---

## Notes
- The error uses `SimpleRuntimeError` because it is a **runtime data manipulation**
  problem, not a metadata or instantiation issue.
- The setter includes the fix instructions directly in the error message.
- The `_locked` flag defaults to `False` for all instances.
- The check is intentionally lightweight and always present, even when unused.
"""