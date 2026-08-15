from typing import Any, TYPE_CHECKING
# Inners
from .validations import raise_missing_value_error
# Annotations
if TYPE_CHECKING:
    from ...protocols.classes import SimpleConstantProtocol


def normalize(
    cls: "SimpleConstantProtocol",
    value: Any,
    *,
    process_none: bool = False,
) -> Any:
    """Normalizes a value according to constant metadata rules."""

    # 1. Handle None
    if value is None:

        # 1.1 None is allowed only when explicitly requested
        if process_none:
            return cls.meta.default

        # 1.2 Otherwise raise a structured error
        raise_missing_value_error(cls)

    # 2. Handle default value identity optimization
    # noinspection PyBroadException
    try:
        # 2.1 If the value equals the default, return the default instance
        if value == cls.meta.default:
            return cls.meta.default

    except Exception:
        # 2.2 Non-comparable values fall through to validation
        pass

    # 3. Validate the value
    cls.validate(value)

    # 4. Return validated value
    return value


_DESIGN_NOTES = """
# normalize

## Purpose
Normalizes incoming values for constant definitions. This function enforces the
rules for handling `None`, default values, and validation. It is used by both
constant and object classes whenever a value is assigned.

---

## Why `None` is forbidden
The SimpleObject ecosystem does not allow `None` as a valid value. This is
intentional:

- Composite objects compute their value from inner elements.
- If any inner element were `None`, the composite value could not be computed.
- Metadata already prevents `None` from being used as a declared default.
- `normalize` enforces this rule at runtime for user-provided values.

The only exception is when `process_none=True`, which instructs the system to
replace `None` with the class’s default value.

---

## Behavior
1. **Handling `None`**
   - If `process_none=True`, return the default value.
   - Otherwise, raise `raise_missing_value_error`.

2. **Default Value Optimization**
   - If the provided value equals the default, return the default instance.
   - This avoids unnecessary allocations and keeps identity stable.

3. **Validation**
   - All non-default values are validated through the full validation pipeline.

4. **Return**
   - Returns either the default instance or the validated value.

---

## Notes
- This function is intentionally minimal; all diagnostics are delegated to
  specialized error helpers.
- The public-facing docstring belongs to the class method `SimpleConstant.normalize`,
  not to this internal helper.
- Composite objects reuse this normalization logic through their own pipelines.
"""