# ⚛️ `SimpleConstant` — Declarative atom

`SimpleConstant` is the fundamental building block of the whole system — it
represents a single typed value (an "atom") that can validate and normalize
itself. Atoms are used both on their own (e.g. as typed, self-validating
values in another library) and as inner elements (`_inners`) of `SimpleObject`
composite objects.

```
SimpleBase
└── SimpleConstant     ← you are here
    └── SimpleObject
```

---

## 🧭 Contents

* [Declarative interface](#declarative-interface)
  * [`_type`](#_type)
  * [`_default`](#_default)
  * [`_validate`](#_validate)
* [Public API](#public-api)
  * [`validate_type`](#validate_type)
  * [`validate`](#validate)
  * [`is_valid`](#is_valid)
  * [`normalize`](#normalize)
  * [`bool_or_raise_validate_error`](#bool_or_raise_validate_error)
* [The validation pipeline as a whole](#the-validation-pipeline-as-a-whole)

[⬅️ Back to main README](../../README.md)

---

## Declarative interface

This is everything the user writes by hand when defining a constant:

```python
class Age(SimpleConstant):
    _type = int
    _default = 20

    @classmethod
    def _validate(cls, value, *, return_bool=False):
        if value < 0:
            return cls.bool_or_raise_validate_error(
                value, "Age cannot be negative.", return_bool=return_bool
            )
        return True
```

### `_type`

A required type annotation. The metadata (`SimpleConstantMetadata`) processes
it at class-definition time and exposes it as `cls.meta.value_type` — this is
the single source that all type validation in the system is based on.

### `_default`

A required default value. It must pass type validation against `_type`
already at class-definition time — so an invalid default is caught
immediately, not later at runtime on the first instance.

### `_validate`

An optional hook for extended validation beyond a plain type check. If the
user doesn't override it, the default implementation returns `True` — i.e.
"no further rules, a type match is enough." The method can:

* return `True`/`False`,
* raise a custom exception,
* use the helper
  [`bool_or_raise_validate_error`](#bool_or_raise_validate_error) for a
  structured error report.

[▲ Back to Contents](#-contents)

---

## Public API

All the methods below are just thin wrappers on `SimpleConstant` — they
contain minimal logic and delegate to internal functions in
`_core/logic/constant_methods/`. This pattern (thin public wrapper + internal
function with `_DESIGN_NOTES`) repeats throughout the whole library.

### `validate_type`

Deterministic type validation, based purely on metadata — without involving
the user's `_validate` logic.

**Parameters:**
* `value` (*Any*): the value to check.
* `return_bool` (*bool*, default `False`): if `True`, returns `False`
  instead of raising an exception.

**Return value:**
* `True`, if the value matches the type.
* `False`, if `return_bool=True` and the type doesn't match.
* `None`, if `return_bool=False` and validation passes (implicit return).

**Exceptions:**
* `SimpleRuntimeError`, if `return_bool=False` and the type doesn't match.

**Under the hood:**
```python
def validate_type(cls, value, *, return_bool=False):
    if isinstance(value, cls.meta.value_type):
        return True
    if return_bool:
        return False
    raise_type_error(cls, value)
```

The whole function is deliberately minimal — the only thing it does beyond a
plain `isinstance` check is decide whether to "return a bool, or raise a
structured error." All the diagnostics (what exactly doesn't match, how to
fix it) are delegated to `raise_type_error`.

[▲ Back to Contents](#-contents)

---

### `validate`

Runs the full validation pipeline: type validation **plus** the user's
`_validate` logic.

**Parameters:**
* `value` (*Any*): the value to check.
* `return_bool` (*bool*, default `False`).

**Return value:**
* `True`/`False`/`None`, following the same convention as `validate_type`.

**Exceptions:**
* `SimpleRuntimeError`, if `return_bool=False` and validation fails.

**Under the hood:**
```python
def validate(cls, value, *, return_bool=False):
    try:
        result = (
            cls.validate_type(value, return_bool=return_bool)
            and cls.meta.validate(value, return_bool=return_bool)
        )
    except Exception as e:
        if return_bool:
            return False
        if isinstance(e, SimpleObjectError):
            raise
        raise_unexpected_validation_error(cls, value, e)

    if result is False and not return_bool:
        raise_validation_error(cls, value)

    return result
```

Three things worth noting here:

1. **Short-circuit evaluation (`and`).** The user's `_validate` doesn't run
   at all if type validation fails — there's no point validating a value of
   the wrong type against domain rules.
2. **Distinguishing expected from unexpected exceptions.** If the user's
   `_validate` raises a `SimpleObjectError`, it's treated as an "expected"
   structured error and simply propagates unchanged. Anything else
   (typically a bug in user code) gets wrapped via
   `raise_unexpected_validation_error`, so the error message stays
   consistent across the whole system.
3. **`return_bool=True` means exceptions are fully suppressed** — even
   unexpected ones. This is a deliberate trade-off: in boolean mode, the
   caller wants a simple yes/no answer, not a traceback.

[▲ Back to Contents](#-contents)

---

### `is_valid`

A convenience wrapper around `validate(..., return_bool=True)`.

**Parameters:**
* `value` (*Any*): the value to check.

**Return value:**
* `bool` — `True` if the value is valid, `False` otherwise. Never raises an
  exception.

**Usage example:**
```python
if Age.is_valid(-5):
    ...
else:
    print("Invalid age")
```

[▲ Back to Contents](#-contents)

---

### `normalize`

Normalizes an input value according to the metadata — handling `None`,
default-identity optimization, and validation in a single step.

**Parameters:**
* `value` (*Any*): the value to normalize.
* `process_none` (*bool*, default `False`): if `True`, `None` is replaced
  with the default value instead of raising an error.

**Return value:**
* `Any`: the normalized value (either the default instance, or the
  validated input value).

**Exceptions:**
* `SimpleRuntimeError`, if the value is `None` and `process_none=False`, or
  if validation fails.

**Under the hood:**
```python
def normalize(cls, value, *, process_none=False):
    if value is None:
        if process_none:
            return cls.meta.default
        raise_missing_value_error(cls)

    try:
        if value == cls.meta.default:
            return cls.meta.default
    except Exception:
        pass

    cls.validate(value)
    return value
```

**Why `None` is forbidden throughout the system:** composite objects compute
their value from their inner elements (`_inners`) — if any of them could be
`None`, there'd be no way to compute a result from it. The metadata already
enforces this at class-definition time (`_default` must not be `None`);
`normalize` enforces the same thing at runtime for values coming from the
user.

**Default-identity optimization:** if the input value equals the default, the
`cls.meta.default` instance itself is returned directly instead of running a
fresh validation. This saves unnecessary work and keeps a stable identity for
a repeatedly used default value. The comparison is wrapped in `try/except`
because not every value is necessarily comparable to the default at all
(`==` can raise an exception for an arbitrary type) — in that case, it simply
falls through to full validation.

[▲ Back to Contents](#-contents)

---

### `bool_or_raise_validate_error`

A helper method intended **exclusively** for use inside the user's
`_validate` — it lets you write concise validation rules without manually
assembling structured exceptions.

**Parameters:**
* `value` (*Any*): the value being validated.
* `problem` (*str*): a human-readable description of what's wrong.
* `return_bool` (*bool*, default `False`): if `True`, returns `False`
  instead of raising an exception.

**Return value:**
* `False`, if `return_bool=True`.

**Exceptions:**
* `SimpleRuntimeError` (with `ValueError` as the underlying exception), if
  `return_bool=False`.

**Usage example:**
```python
@classmethod
def _validate(cls, value, *, return_bool=False):
    if value < 0:
        return cls.bool_or_raise_validate_error(
            value, "Value must be non-negative.", return_bool=return_bool
        )
    return True
```

Because the method itself respects `return_bool`, all you need to do inside
`_validate` is `return` its result — there's no need to write your own
`if/else` for boolean-vs-exception mode in user code.

[▲ Back to Contents](#-contents)

---

## The validation pipeline as a whole

The three methods chain together in a clear order:

```
validate_type  →  _validate (user hook, via cls.meta.validate)  →  normalize
```

* `validate_type` — the fastest, cheapest check: does the type match?
* `validate` — builds on `validate_type`, bringing in domain rules from
  `_validate`.
* `normalize` — the highest level, used for actual value assignment: handles
  `None`, default identity, and finally calls `validate`.

This layered structure means you can pick exactly the level of strictness and
behavior you need at any given moment — from a raw type check all the way up
to full normalization with a fallback to the default.

➡️ Next: [README_SIMPLE_OBJECT](README_SIMPLE_OBJECT.md)

[▲ Back to Contents](#-contents)
