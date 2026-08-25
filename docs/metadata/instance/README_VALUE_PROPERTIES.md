# 🔗 The `value` property — Unified access to the value

The `value` property is the **single public interface** through which the
user both reads and writes the value — whether it's the root instance, or
any arbitrarily nested inner element inside a composition. This document
describes the mechanics behind building that unified interface.

---

## 🧭 Contents

* [`create_value_property` — assembling the property](#create_value_property--assembling-the-property)
* [`create_value_getter` — reading](#create_value_getter--reading)
* [`create_value_setter` — writing](#create_value_setter--writing)
* [`create_instance_property` — accessing the instance, not the value](#create_instance_property--accessing-the-instance-not-the-value)
* [`create_properties_for_inner` — both together, for one element](#create_properties_for_inner--both-together-for-one-element)

[⬅️ Back to main README](../../../README.md)

---

## `create_value_property` — assembling the property

**Parameters:**
* `meta`: the metadata of the element the property belongs to.
* `is_constant` (*bool*, default `True`): atomic or composite setter
  behavior.
* `mutable` (*bool*, default `True`): whether a setter should be created
  at all.
* `path` (*tuple | None*): `None` for the root value, otherwise the path
  to an inner element.

**Return value:** a `property` object with a generated docstring.

```python
def create_value_property(meta, *, is_constant=True, mutable=True, path=None):
    getter = create_value_getter(meta, path)

    if not mutable:
        return property(fget=getter, doc=...)

    setter = create_value_setter(meta, is_constant, path)
    return property(fget=getter, fset=setter, doc=...)
```

**Immutable → getter only.** If the instance is immutable, the `property`
is never even assembled with a setter — attempting to write
(`instance.value = ...`) fails at the level of Python itself
(`AttributeError: can't set attribute`), not through any custom
validation. The strongest possible guarantee of immutability — the write
path simply doesn't exist.

**The automatically generated docstring** differs based on
`is_constant` — for an atom it describes normalization and bubbling
upward, for a composition it describes decomposition and distribution to
the inner elements. Thanks to this, `help(MyClass.value)` gives the user a
directly meaningful, contextually correct description, even though the
whole property is generated dynamically.

**This function creates `value` for two different things at once** — the
root value of an instance (`path=None`, called from
`make_atom_class`/`make_composite_class`) and the value of any arbitrary
inner element (`path=(...)`, called from `create_properties_for_inner`
below). It's one unified mechanism, not two separate implementations.

[▲ Back to Contents](#-contents)

---

## `create_value_getter` — reading

**Parameters:** `meta`, `path` (`None`, or a tuple).

**Return value:** the getter function.

```python
def create_value_getter(meta, path):
    if path is None:
        def getter(self):
            return self._value
    else:
        get_inner_instance = attrgetter(*path)
        def getter(self):
            return get_inner_instance(self).value

    getter.__annotations__ = {"return": meta.value_type}
    return getter
```

**The getter is deliberately identical for atoms and compositions alike**
— it always just returns the current normalized value. All the difference
between atomic and composite behavior is concentrated in the **setter**
(see below); the getter stays uniform and stateless.

**`operator.attrgetter(*path)` instead of a chain of `getattr` calls** —
for nested access (`path = ("_engine", "_pistons")`), `attrgetter` is
faster than manually chaining `getattr` calls and doesn't allocate extra
intermediate steps.

[▲ Back to Contents](#-contents)

---

## `create_value_setter` — writing

**Parameters:** `meta`, `is_constant` (default `False`), `path` (default
`None`).

**Return value:** the setter function.

**Under the hood (abridged):**
```python
def create_value_setter(meta, is_constant=False, path=None):
    get_inner = attrgetter(*path) if path is not None else None

    def setter(self, value):
        if self._locked:
            raise_locked_value_error(value, self.__class__.__name__)

        if not is_constant and not meta.is_decomposeable:
            raise_class_not_decomposeable(meta)

        instance = get_inner(self) if get_inner is not None else self

        instance._root_value_setter(value, recalculate_up=True)

        if not is_constant:
            instance._recalculate_inners()

        if path is None:
            log_value_event(self.__class__, value, event="set")

    return setter
```

Five steps, in exactly this order:

1. **The lock always comes first.** `self._locked` is checked as the very
   first thing — no other logic is even evaluated if the instance is
   locked.
2. **A composite setter requires decomposability.** If it's a composition
   (`not is_constant`) and `meta.is_decomposeable` is `False`, the write
   is rejected outright — there's no point accepting a value that
   couldn't be decomposed into the inner elements anyway.
3. **Distinguish root vs. inner element**
   (`instance = get_inner(self) if ... else self`) — from this point on,
   the code works with the **target** instance, not necessarily `self`.
4. **Write plus optional decomposition.** The value is always written
   first via `_root_value_setter(value, recalculate_up=True)` (bubbling
   upward allowed — this is a public, user-initiated write). If it's a
   composition, `_recalculate_inners()` is then called right after, to
   distribute the new value down into the inner elements.
5. **Logging only at the root level.** `if path is None` — a change to an
   inner element is only logged once, at the level where the user
   actually triggered it, not repeatedly at every intermediate step of
   the cascade.

**This setter is the bridge between the two reactive directions**
described in [README_COMPOSITE_CLASS](README_COMPOSITE_CLASS.md) — step 4
triggers both `_recalculate_self` (via `_root_value_setter` → bubbling)
and `_recalculate_inners` (directly), depending on whether the target is
an atom or a composition.

[▲ Back to Contents](#-contents)

---

## `create_instance_property` — accessing the instance, not the value

**Parameters:** `inner_meta`, `path`.

**Return value:** a read-only `property`.

```python
def create_instance_property(inner_meta, path):
    get_inner_instance = attrgetter(*path)

    def getter(self):
        return get_inner_instance(self)

    return property(fget=getter, doc=...)
```

The structural counterpart to the `value` property — instead of the inner
element's **value**, it returns its **instance** directly (an object with
its own `.value`, `.owner`, and possibly mixin methods). Always a getter
only — replacing the entire inner instance from the outside is never
allowed, only setting its value (via the `value` property).

This property is mainly useful for introspection and advanced use cases,
where the user needs to reach the inner element as a full-fledged object
(e.g. to call a mixin method on it), not just read its value.

[▲ Back to Contents](#-contents)

---

## `create_properties_for_inner` — both together, for one element

**Parameters:** `inner_meta`, `path` (default `()`), `mutable` (default
`True`).

**Return value:** a `dict` with two keys.

```python
def create_properties_for_inner(inner_meta, path=(), *, mutable=True):
    name_snake = inner_meta.name_snake
    instance_path = path + (inner_meta.name_private,)

    return {
        name_snake: create_value_property(inner_meta, is_constant=inner_meta.is_constant,
                                            mutable=mutable, path=instance_path),
        f"{name_snake}_instance": create_instance_property(inner_meta, instance_path),
    }
```

For a single inner element (say, `engine`), this generates **two**
properties at once:

* **`engine`** — the value (always readable, writable depending on
  mutability and decomposability).
* **`engine_instance`** — the instance itself (always read-only).

**`instance_path = path + (inner_meta.name_private,)`** — this is where
the path for nested access is built up. The function receives `path` from
the outside (the caller, typically `create_properties_for_inners`, passes
`()` for direct elements) and extends it with its own private slot. For
multiply nested structures (if the caller were to pass a non-empty
`path`), the resulting path would grow by another level — so the
mechanism is prepared for deeper nesting too, even though in the base
case (`create_properties_for_inners` always calls it with `path=()`) only
one level is actually used.

The resulting `dict` is then merged directly (`|=`) into `class_dict` when
the composite class is compiled (see
[README_COMPOSITE_CLASS](README_COMPOSITE_CLASS.md)).

[▲ Back to Contents](#-contents)

➡️ Next: [README_INSTANCE_PROTOCOLS](README_INSTANCE_PROTOCOLS.md)
