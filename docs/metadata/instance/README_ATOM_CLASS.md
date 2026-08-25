# ⚛️ Atomic instance — `make_atom_class` and its building blocks

This document describes how a blueprint (a `SimpleConstant`/`SimpleObject`
class) turns into an **actual, running atomic instance** — the smallest
structural unit in the whole system. A composite instance (see
[README_COMPOSITE_CLASS](README_COMPOSITE_CLASS.md)) builds directly on top
of it through inheritance.

```
InstanceBase                        (identity, slots, meta property)
└── {Meta.owner_class}AtomBase      ← created by make_atom_class
```

---

## 🧭 Contents

* [InstanceBase — the shared root of every instance](#instancebase--the-shared-root-of-every-instance)
* [make_atom_class — compiling the atomic class](#make_atom_class--compiling-the-atomic-class)
* [create_atom_init — the constructor](#create_atom_init--the-constructor)
* [create_root_value_setter — reactive value writes](#create_root_value_setter--reactive-value-writes)

[⬅️ Back to main README](../../../README.md)

---

## `InstanceBase` — the shared root of every instance

Before looking at `make_atom_class`, it's worth remembering what
`InstanceBase` (see also
[README_SIMPLE_META](../README_SIMPLE_META.md)) gives to **absolutely
every** instance — atomic and composite alike:

```python
class InstanceBase:
    _is_instance_class: bool = True
    __slots__ = ("__weakref__",)

    def init_mixins(self) -> None: ...

    @property
    def meta(self) -> "SimpleMetadataLike":
        return self.__class__.__metadata__

    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
```

* **`_is_instance_class = True`** — a signal to `SimpleMeta.__new__` so it
  doesn't treat the dynamically created class as a new blueprint (see
  [README_SIMPLE_META](../README_SIMPLE_META.md)).
* **`__slots__ = ("__weakref__",)`** — no `__dict__`, just weak-reference
  support. The other slots (`_value`, `_owner`, `_locked`...) are added
  later by the concrete atomic/composite class.
* **`init_mixins`** — an empty default, overridden/extended dynamically
  via `_build_combined_init_mixins` (see
  [README_CREATE_INSTANCE](README_CREATE_INSTANCE.md)) if the instance
  includes mixins with their own initialization.
* **`meta`** — constant-time access to the metadata directly from the
  instance's class (`self.__class__.__metadata__`), with no lookups
  involved.

[▲ Back to Contents](#-contents)

---

## `make_atom_class` — compiling the atomic class

**Parameters:**
* `meta` (*SimpleMetadataLike*): the blueprint's metadata.
* `mutable` (*bool*, default `True`): the mutable or immutable variant.

**Return value:** a dynamically created class (`AtomInstanceProtocol`).

**Under the hood (abridged):**
```python
def make_atom_class(meta, *, mutable=True):
    base_class_name = f"{meta.class_name}Atom{'Mutable' if mutable else 'Immutable'}Base"
    class_parents = (InstanceBase, meta.owner_class)

    class_dict = {
        "_is_mutable": mutable,
        "__metadata__": meta,
        "__slots__": ("_value", "_owner", "_locked"),
        "__init__": create_atom_init(meta, base_class_name),
        "value": create_value_property(meta, mutable=mutable),
        "owner": property(lambda self: self._owner),
    }
    if mutable:
        class_dict["_root_value_setter"] = create_root_value_setter(base_class_name)

    atom_class = type(base_class_name, class_parents, class_dict)

    return atom_class
```

**Dual inheritance is deliberate.** `class_parents = (InstanceBase,
meta.owner_class)` — the instance inherits both structural identity
(`InstanceBase`) and **the domain behavior from the blueprint itself**
(`meta.owner_class`, i.e. the class the user wrote — with its
`_validate` and any other methods). The instance is thus both "the" user
class and a structurally compatible runtime object at the same time.

**The `_value`, `_owner`, `_locked` slots** — three fields, enough for the
complete atomic state: the current value, a reference to the parent in a
composition (for bubbling changes upward), and an immutability flag.

**A note on the blueprint's declarative attributes** (`_type`, `_default`,
`_validate`, `bool_or_raise_validate_error`): `class_dict` never contains
them, so they never end up in `atom_class`'s own `__dict__` — but that
doesn't hide them. `class_parents` includes `meta.owner_class`, so the
instance still reaches them through the MRO, exactly like any other
inherited attribute. `type(...)` only controls the new class's own
namespace; it has no way to remove something a parent already exposes.

[▲ Back to Contents](#-contents)

---

## `create_atom_init` — the constructor

**Parameters:** `meta`, `base_class_name` (for `__qualname__`).

**Return value:** the `__init__` function as a closure.

**Under the hood:**
```python
def create_atom_init(meta, base_class_name):
    def __init__(self):
        self._value = meta.default
        self._owner = UNSET
        self._locked = False
        self.init_mixins()

    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    return __init__
```

**A closure instead of a plain method** — `meta` is captured in the
closure, so the constructor doesn't have to look up the metadata again on
every instance creation (`self.meta` would also work, but a closure is
faster and more direct, since `meta` is already definitively known at
class-compilation time).

**Reflection alignment** (`__name__`, `__qualname__`) — without this step,
the dynamically created function would show up in a traceback as an
anonymous `"<locals>.__init__"`. Overwriting these attributes makes
`__init__` look like a **native member of the generated class** in
diagnostics — important for debugging, since the whole system routinely
creates dozens of dynamic classes.

An instance always starts with **the default value from the metadata**
(`meta.default`), with no owner (`_owner = UNSET`) and unlocked
(`_locked = False`) — ownership is only assigned from the outside, when
the instance becomes an inner element of a composition (see
[README_COMPOSITE_CLASS](README_COMPOSITE_CLASS.md)).

The last step, `self.init_mixins()`, is the hook that the whole
mixin-based extensibility relies on — on the base atomic class it's the
empty method from `InstanceBase`, but once mixins with their own
initialization are added, `create_instance_class` replaces it with a
merged call chain (see
[README_CREATE_INSTANCE](README_CREATE_INSTANCE.md)).

[▲ Back to Contents](#-contents)

---

## `create_root_value_setter` — reactive value writes

**Parameters:** `base_class_name`.

**Return value:** the `_root_value_setter` function as a closure. It only
exists on the **mutable** variant — the immutable instance doesn't have it
at all.

**Under the hood:**
```python
def create_root_value_setter(base_class_name):
    def _root_value_setter(self, value, recalculate_up=True):
        new_value = self.normalize(value, process_none=True)

        if self._value == new_value:
            return

        self._value = new_value

        if self._owner and recalculate_up:
            self._owner._recalculate_self()

    ...
    return _root_value_setter
```

This is the **real heart of upward reactivity** (the "🔼" from the
library's introductory concept). Four steps:

1. **Normalization** — the input always goes through
   `self.normalize(value, process_none=True)`, so `None` is automatically
   replaced with the default instead of raising an error (unlike the
   public `value` setter, where `None` is typically an error — this is
   the internal, more permissive variant for reactive propagation).
2. **Short-circuit on a match** — if the new value equals the old one, the
   function returns immediately. This is a key optimization: without it,
   even a no-op change would trigger a whole cascade of recalculations
   upward.
3. **Write** — `self._value = new_value`.
4. **Bubbling upward** — only if the instance **has** an owner (`self._owner`
   is not `UNSET`) **and** bubbling is allowed (`recalculate_up=True`),
   `self._owner._recalculate_self()` is called.

**The `recalculate_up` parameter is deliberately toggleable**, because
`_root_value_setter` is used in two different directions: a public value
write (`value = ...`, where bubbling makes sense) and internal downward
distribution of values from `_recalculate_inners` (see
[README_COMPOSITE_CLASS](README_COMPOSITE_CLASS.md)), where bubbling back
upward would create an infinite loop — which is why it's called there with
`recalculate_up=False`.

[▲ Back to Contents](#-contents)

➡️ Next: [README_COMPOSITE_CLASS](README_COMPOSITE_CLASS.md)
