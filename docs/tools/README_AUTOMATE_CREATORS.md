# 🏭 Automate Creators — Creating classes programmatically without `class` syntax

The standard way to define something in the Simple system is to write
`class MyConstant(SimpleConstant): ...` directly in code. This tool offers
an alternative: **creating a class blueprint programmatically, at
runtime**, from values that might come from configuration, a database, or
user input. Three public functions form a clear hierarchy:

```
create_simple_object          (universal facade — decides atom vs. composition)
├── create_constant_class      (builds SimpleConstant subclasses)
└── create_object_class        (builds SimpleObject subclasses)
```

---

## 🧭 Contents

* [`create_constant_class` — a constant, created programmatically](#create_constant_class--a-constant-created-programmatically)
* [`create_object_class` — a composition, created programmatically](#create_object_class--a-composition-created-programmatically)
* [`create_simple_object` — the universal facade](#create_simple_object--the-universal-facade)
* [Helper functions](#helper-functions)
  * [`_is_lambda`](#_is_lambda)
  * [`process_validate` and `process_decompose`](#process_validate-and-process_decompose)
  * [`process_logic`](#process_logic)
  * [`load_parameters_from_inners`](#load_parameters_from_inners)
  * [`calculate_default`](#calculate_default)

[⬅️ Back to main README](../../README.md)

---

## `create_constant_class` — a constant, created programmatically

**Parameters:**
* `class_name` (*str*): the name of the new class.
* `default` (*Any*): the required default value.
* `value_type` (*type | UNSET*): an explicit type; if `UNSET`, it's derived
  from `type(default)`.
* `validate` (*Callable | UNSET*): an optional validation function or
  lambda.

**Return value:** a new `SimpleConstant` subclass (a blueprint, not an
instance).

**Under the hood (abridged):**
```python
def create_constant_class(class_name, default, value_type=UNSET, validate=UNSET):
    ...
    if value_type is UNSET:
        value_type = type(default)

    namespace = {"_default": default, "_type": value_type}

    if validate is not UNSET:
        namespace["_validate"] = classmethod(process_validate(validate))

    return type(class_name, (SimpleConstant,), namespace)
```

**Deriving the type from the value is a convenient default, not magic.**
If the user doesn't specify `value_type` explicitly, the system simply
calls `type(default)` — the same as what someone would typically write by
hand (`_type = int` for `_default = 20`). This saves typing in simple
cases, but stays fully overridable when a looser type is needed (e.g. a
union).

The function is a thin wrapper over what would otherwise require writing
out a full `class` definition — the result goes through exactly the same
`SimpleMeta`/`SimpleConstantMetadata` pipeline as a hand-written class (see
[README_SIMPLE_META](../metadata/README_SIMPLE_META.md#__new__--class-creation)),
because `type(class_name, (SimpleConstant,), namespace)` triggers exactly
the same mechanism as Python's `class` keyword.

[▲ Back to Contents](#-contents)

---

## `create_object_class` — a composition, created programmatically

**Parameters:**
* `class_name` (*str*): the name of the new class.
* `inners` (*tuple*): the inner elements.
* `logic` (*Callable*): the required computation function.
* `value_type` (*type | UNSET*): an explicit type; if `UNSET`, it's derived
  from a dry run of `logic`.
* `validate`, `decompose` (*Callable | UNSET*): optional hooks.

**Return value:** a new `SimpleObject` subclass.

**Under the hood (abridged):**
```python
def create_object_class(class_name, inners, logic, value_type=UNSET, validate=UNSET, decompose=UNSET):
    ...
    _params = load_parameters_from_inners(class_name, inners)
    _logic = process_logic(logic, _params.keys())

    if value_type is UNSET:
        _default_value = calculate_default(_logic, tuple(_params.values()))
        value_type = type(_default_value)

    namespace = {"_inners": inners, "_type": value_type, "_logic": classmethod(_logic)}
    ...
    return type(class_name, (SimpleObject,), namespace)
```

**Deriving the type is a step more complex here than for a constant** —
`type(default)` isn't enough, because a composition has no explicit
default at all (see
[README_SIMPLE_OBJECT](../core/README_SIMPLE_OBJECT.md#important-_default-must-not-be-defined)).
Instead, `logic` is **actually called once**, with default values derived
from `inners` (`calculate_default`, see below), and the result's type is
used as `value_type`. This is a smaller, manual preview of what
`SimpleObjectMetadata` does anyway (dry-running `_logic` — see
[README_METHOD_PROCESSING](../metadata/README_METHOD_PROCESSING.md#verify_calculation--dry-run-and-result-check))
— here it just has to happen a step earlier, because `value_type` needs to
be known **before** the `namespace` for `type(...)` is assembled.

**`logic` goes through signature normalization** (`process_logic`) before
any attempt is even made to compute a default from it — this handles the
most common source of friction with the programmatic API: the user
typically doesn't want to write `lambda cls, a, b: ...`, they just want
`lambda a, b: ...` (see [helper functions](#process_logic) below).

[▲ Back to Contents](#-contents)

---

## `create_simple_object` — the universal facade

**Parameters:** unifies the parameters of both creators, plus:
* `return_instance` (*bool*, default `False`): if `True`, returns an
  instance directly instead of a blueprint.
* `mixins`, `as_atom`, `mutable`: passed through to `SimpleMeta.__call__`
  if `return_instance=True`.

**Return value:** either a blueprint class, or an instance (depending on
`return_instance`).

**Under the hood:**
```python
def create_simple_object(class_name, default=UNSET, inners=UNSET, ..., return_instance=False, ...):
    if inners is UNSET:
        _class = create_constant_class(class_name=class_name, default=default, ...)
    else:
        _class = create_object_class(class_name=class_name, inners=inners, ...)

    return _class if not return_instance else _class(mixins=mixins, as_atom=as_atom, mutable=mutable)
```

**The routing rule is a single `if inners is UNSET`** — the same principle
as in `SimpleMeta.__new__`, where the presence of `_inners` distinguishes
a constant from a composition (see
[README_SIMPLE_META](../metadata/README_SIMPLE_META.md#__new__--class-creation)).
Here, the same decision is made before the class is even created, not
inside the metaclass — because `create_constant_class` and
`create_object_class` each have a different set of required parameters
(default vs. inners+logic).

**`create_simple_object` is the only public API that can return a finished
instance directly** (`return_instance=True`) — the last line just delegates
to `_class(...)`, which is exactly the call that triggers
`SimpleMeta.__call__` → `create_instance` (see
[README_CREATE_INSTANCE](../metadata/instance/README_CREATE_INSTANCE.md)). This is the
typical "create the class and the instance in one step" pattern, suited
for scenarios where nobody's going to reuse the blueprint anyway (e.g. a
one-off constant from a config file).

[▲ Back to Contents](#-contents)

---

## Helper functions

### `_is_lambda`

```python
def _is_lambda(fn):
    return callable(fn) and getattr(fn, "__name__", None) == "<lambda>"
```

A small but key detection tool — all three `process_*` functions below
behave differently depending on whether they received a named function or
an anonymous `lambda`. The detection is simple: every `lambda` in Python
has `__name__ == "<lambda>"`, regardless of what variable it's assigned
to.

[▲ Back to Contents](#-contents)

---

### `process_validate` and `process_decompose`

Both work on the same principle — they normalize the **signature** of the
user's function, not its behavior:

```python
def process_validate(validate):
    if not _is_lambda(validate):
        return validate

    def _validate(cls, value, *, return_bool=False):
        return validate(value)

    return _validate
```

```python
def process_decompose(decompose):
    if not _is_lambda(decompose):
        return decompose

    def _decompose(cls, value):
        return decompose(value)

    return _decompose
```

**Why this exists at all:** internally, the system always calls
`_validate(cls, value, *, return_bool=...)` and `_decompose(cls, value)` —
fixed signatures, enforced via `verify_params` (see
[README_METHOD_PROCESSING](../metadata/README_METHOD_PROCESSING.md#verify_params--signature-check-at-the-bytecode-level)).
But when the user writes `lambda v: v > 0` in the programmatic API, they're
missing `cls` (and, for validate, `return_bool` too) — and a lambda can't
easily be "extended" with an extra parameter without rewriting it. So both
functions leave a named function unchanged (assuming it already has the
correct signature), but **wrap** a lambda in a wrapper with the correct
signature, which internally calls the original lambda with only what it
actually needs (`value`).

**The asymmetry between these functions and `process_logic`** (see below)
isn't accidental — `process_validate`/`process_decompose` always have the
same, fixed number of parameters (`value`, and possibly `return_bool`), so
a plain `def` wrapper is enough. `process_logic` can't rely on this trick,
because the number of `_logic` parameters varies (based on the number of
`_inners`) — which is why it needs a different approach.

[▲ Back to Contents](#-contents)

---

### `process_logic`

```python
def process_logic(logic, params_name):
    if not _is_lambda(logic):
        return logic

    params = ", ".join(params_name)
    src = f"def _logic(cls, {params}): return logic({params})"

    namespace = {"logic": logic}
    exec(src, namespace)

    return namespace["_logic"]
```

Here, a plain fixed wrapper isn't enough — `_logic` needs **exactly as
many parameters as the composition has `_inners`**, and that number is
unknown in advance (it's `params_name`, derived from the specific
composition). The solution is to build the wrapper's source code **as a
string** and compile it via `exec` — for `_inners = (Width, Height)` this
would generate exactly:

```python
def _logic(cls, width, height): return logic(width, height)
```

This is one of the few places in the whole library where `exec` is used —
and it's deliberately isolated to just this spot, because it's the only
practical way to build a function with a **dynamic number of named
parameters** (as opposed to `*args`, which wouldn't satisfy the strict
signature check in `verify_params`).

[▲ Back to Contents](#-contents)

---

### `load_parameters_from_inners`

**Parameters:** `class_name` (for diagnostics), `inners` (a tuple of
blueprints).

**Return value:** `dict[str, Any]` — `{name_snake: default}` for every
inner element.

```python
def load_parameters_from_inners(class_name, inners):
    if not isinstance(inners, tuple):
        raise_inners_is_not_tuple(class_name, inners)

    params = {}
    for inner in inners:
        if not issubclass(inner, SimpleConstant):
            raise_inner_is_not_simple_constant_subclass(class_name, inner)
        params[inner.meta.name_snake] = inner.meta.default

    return params
```

A straightforward extraction — for each `inner` (which must be a subclass
of `SimpleConstant`, i.e. an atom or a composition), its `name_snake` and
`default` are taken from the already-existing, computed metadata. The
result serves two purposes: first as the source of parameter names for
`process_logic`, second as the source of values for `calculate_default`.

[▲ Back to Contents](#-contents)

---

### `calculate_default`

**Parameters:** `logic` (already normalized, with a `cls` parameter),
`params` (a tuple of values in `inners` order).

**Return value:** the computed default value.

```python
def calculate_default(logic, params):
    try:
        cls = None
        return logic(cls, *params)
    except Exception as exc:
        raise_calculate_default_failed(logic, params, exc)
```

**`cls = None` is a deliberate trade-off.** At this point, there **isn't
yet** any class whose method `logic` would be — the `namespace` that will
soon be used to create that class is still being built. The `_logic`
function nonetheless expects `cls` as its first parameter (for consistency
with how `_logic` looks on hand-written classes). Since a typical `_logic`
implementation doesn't actually use `cls` anyway (it just reads the
parameter values), passing `None` is safe, and it allows the dry run to
happen before the class even exists.

[▲ Back to Contents](#-contents)
