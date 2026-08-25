# 🏗️ `create_instance` — Orchestration and the mixin pipeline

This document describes the top level of instance creation — what actually
runs when you call `MyClass(mixins=(...), mutable=False)`, i.e. exactly
what `SimpleMeta.__call__` delegates to (see
[README_SIMPLE_META](../README_SIMPLE_META.md)). While
[README_ATOM_CLASS](README_ATOM_CLASS.md) and
[README_COMPOSITE_CLASS](README_COMPOSITE_CLASS.md) describe the
structural foundation (atom/composition), this document describes how
mixins get **safely attached** on top of that foundation.

---

## 🧭 Contents

* [`create_instance` — the main orchestrator](#create_instance--the-main-orchestrator)
* [`get_base_class` — selecting the structural foundation](#get_base_class--selecting-the-structural-foundation)
* [`create_instance_class` — compiling the final class](#create_instance_class--compiling-the-final-class)
* [`_resolve_flat_mixins` — flattening the mixin hierarchy](#_resolve_flat_mixins--flattening-the-mixin-hierarchy)
* [`_verify_mixin_compatibility` — the compatibility matrix](#_verify_mixin_compatibility--the-compatibility-matrix)
* [`_build_instance_class_dict` — namespace injection](#_build_instance_class_dict--namespace-injection)
* [`_build_combined_init_mixins` — chaining initialization](#_build_combined_init_mixins--chaining-initialization)
* [`_extend_instance_class`— post-compilation hooks](#_extend_instance_class--post-compilation-hooks)

[⬅️ Back to main README](../../../README.md)

---

## `create_instance` — the main orchestrator

**Parameters:** `cls`, `mixins` (tuple), `as_atom` (bool), `mutable` (bool,
default `True`).

**Return value:** a finished, initialized instance.

**The eight-step pipeline:**

```
1. Input validation (cls is not a base class, as_atom/mutable are bool)
2. is_atom = cls.meta.is_constant or as_atom
3. Hashability check (only for immutable)
4. get_base_class  ──► selects the structural foundation
5. create_instance_class  ──► compiles the final class with mixins
6. object.__new__  ──► raw memory allocation
7. instance.__init__()  ──► initialization
8. return instance
```

**Step 2 is a one-liner, but an important rule:** `is_atom =
cls.meta.is_constant or as_atom` — a constant is **always** an atom,
regardless of `as_atom`; a composition, on the other hand, can be forced
into atomic behavior (`as_atom=True`) if it makes sense for some purpose
to treat it as a single chunk of value instead of a structured tree.

**Step 3 — an immutable value must be hashable.** This makes sense: if the
value is immutable, it should work as a `dict` key / `set` element, which
requires hashability. This check runs before any compilation even starts.

**Two-phase construction (steps 5 vs. 6–7)** is a key architectural
principle: first the runtime class is compiled **once** (an expensive
operation — building `class_dict`, validating mixins...), and only then is
an instance allocated from it (a cheap operation — `object.__new__` +
`__init__`). If the same combination of `mixins`/`mutable` were used to
create instances repeatedly, the class compilation could, in the future,
be cached at the level of the calling code.

[▲ Back to Contents](#-contents)

---

## `get_base_class` — selecting the structural foundation

**Parameters:** `cls`, `is_atom`, `mutable`.

**Return value:** one of the four already-compiled classes from the
metadata.

```python
def get_base_class(cls, is_atom, mutable):
    if is_atom:
        return cls.meta.atom_class_mutable if mutable else cls.meta.atom_class_immutable
    return cls.meta.composite_class_mutable if mutable else cls.meta.composite_class_immutable
```

A pure routing gate across two independent axes — **topology** (atom vs.
composition) and **mutability** (mutable vs. immutable). All the
complexity (lazy creation, caching) is delegated to the metadata — this
function itself doesn't compile anything, it just selects.

[▲ Back to Contents](#-contents)

---

## `create_instance_class` — compiling the final class

**Parameters:** `cls`, `mixins`, `base_class`, `is_atom`, `mutable`.

**Return value:** a compiled runtime class, ready for instance allocation.

**Under the hood:**
```python
def create_instance_class(cls, mixins, base_class, is_atom, mutable):
    class_name = f"{cls.meta.class_name}Instance"
    class_dict = _build_instance_class_dict(cls, mixins, is_atom, mutable)

    _instance_cls = type(class_name, (base_class,), class_dict)
    _instance_cls.__qualname__ = class_name

    _extend_instance_class(class_dict["__mixins__"], _instance_cls)

    return _instance_cls
```

**A key architectural decision: `(base_class,)` — a single parent.**
Mixins are **not** placed into `class_parents`, as you might expect from a
classic multiple-inheritance pattern. Instead, they're flattened,
validated, and mixed directly into `class_dict` (see
`_build_instance_class_dict` below) — the so-called **Namespace Injection
Pattern**.

**Why not standard multiple inheritance?** Three reasons, straight from
`_DESIGN_NOTES`:

1. **Slot layout conflicts.** Python doesn't allow combining multiple
   classes with non-empty `__slots__` in regular multiple inheritance
   (`TypeError`). Injecting mixin slots directly into `class_dict`
   sidesteps this limit entirely.
2. **Explicit membership tracking.** Which mixins an instance has isn't
   tested via the MRO, but via the explicit `class_dict["__mixins__"]` (a
   tuple of flattened mixin classes) — `isinstance(obj, Mixin)` then works
   reliably via a custom `__instancecheck__` on `SimpleMixinMeta`,
   regardless of any MRO complications.
3. **Predictable conflict resolution.** Attribute collisions are resolved
   deterministically already while `class_dict` is being built (see
   below), rather than relying on a complex MRO order.

[▲ Back to Contents](#-contents)

---

## `_resolve_flat_mixins` — flattening the mixin hierarchy

**Parameters:** `cls`, `mixins`, `is_atom`, `mutable`.

**Return value:** a `tuple` — a flattened, deduplicated list of every mixin
(including their full MRO ancestry), in insertion-preserving order.

**Under the hood (the principle):**
```python
def _resolve_flat_mixins(cls, mixins, is_atom, mutable):
    flat_mixins = {}  # a dict used as an O(1) insertion-ordered set

    for mixin in mixins:
        for mro_mixin in mixin.__mro__:
            if mro_mixin not in (object, SimpleMixin):
                if mro_mixin not in flat_mixins:
                    _verify_mixin_compatibility(cls, mro_mixin, is_atom, mutable)
                    flat_mixins[mro_mixin] = True

    return tuple(flat_mixins.keys())
```

**Why walk each mixin's whole `__mro__`, not just the mixin itself?**
Because the user might pass in a mixin that itself inherits from other
mixins — the function "unpacks" its whole inheritance tree, so the final
instance gets absolutely everything the mixin (and its ancestors) define.

**A `dict` used as an insertion-ordered set** — `mro_mixin not in
flat_mixins` is an O(1) check, but unlike a `set`, a `dict` (since Python
3.7) remembers the order its keys were inserted in. This order matters —
`_build_instance_class_dict` later walks it **in reverse**, so that the
natural rule "the first one in the user-supplied tuple wins" holds true
(see below).

**Validation happens "on the fly"** (`_verify_mixin_compatibility` is
called right when a new mixin is discovered, not only after the whole list
has been flattened) — so even an incompatible mixin hidden deep in a
foreign MRO ancestry is caught immediately, before the final class even
starts being assembled.

[▲ Back to Contents](#-contents)

---

## `_verify_mixin_compatibility` — the compatibility matrix

**Parameters:** `cls`, `mixin`, `is_atom`, `mutable` (default `True`).

**Return value:** `None` (raises an exception on incompatibility).

**Under the hood:**
```python
def _verify_mixin_compatibility(cls, mixin, is_atom, mutable=True):
    if not isinstance(mixin, type) or not issubclass(mixin, SimpleMixin):
        validate_mixin_is_class(cls, mixin)
        validate_mixin_is_simple_base_subclass(cls, mixin)

    if mixin._constant_only and not is_atom:
        raise_mixin_not_allowed_for_composite(cls, mixin)
    if mixin._composite_only and is_atom:
        raise_mixin_not_allowed_for_constant(cls, mixin)
    if mixin._mutable_only and not mutable:
        raise_mixin_not_allowed_for_immutable(cls, mixin)
    if mixin._immutable_only and mutable:
        raise_mixin_not_allowed_for_mutable(cls, mixin)
    if mixin._only_types is not UNSET and not isinstance(cls.meta.default, mixin._only_types):
        raise_mixin_not_support_default_value_type(cls, mixin)
```

Five independent checks — every mixin declares its constraints through
flags (`_constant_only`, `_composite_only`, `_mutable_only`,
`_immutable_only`, `_only_types`) — exactly the ones mentioned earlier in
the library's history as "mixin compatibility flags." This function is
where those flags are **actually enforced**, on every instance creation
involving that mixin.

The last check (`_only_types`) is type-based — if a mixin only makes sense
for certain data types (e.g. numeric mixins like `Stepper`/`Volume` from
the library's history), it verifies that `cls.meta.default` is an instance
of the expected type before the mixin is even attached.

[▲ Back to Contents](#-contents)

---

## `_build_instance_class_dict` — namespace injection

**Parameters:** `cls`, `mixins`, `is_atom`, `mutable`.

**Return value:** the complete `class_dict`, ready for `type(...)`.

**Seven steps:**

1. **Flattening the mixins** via `_resolve_flat_mixins`.
2. **Base namespace** — `__is_constant__`, `__is_mutable__`, `__mixins__`.
3. **Preparing accumulators** — `init_mixins` (a list of hooks),
   `mixin_slots` (a dict), and `class_slots` — the set of every slot
   inherited from `cls.__mro__` (i.e. from the structural foundation, the
   atom/composition).
4. **Iterating the mixins in reverse order** (`reversed(all_unique_mixins)`)
   — this is the core of the attribute-override mechanism.
5. For each mixin: checking for slot collisions (against both the base
   class and previously processed mixins) and extracting its namespace
   (methods, attributes).
6. Merging the collected `init_mixins` hooks into one (see below).
7. Finalizing `__slots__` from `mixin_slots`.

**Why `reversed(...)`?** This is the key detail for understanding mixin
priority. The user writes `mixins=(MixinA, MixinB)` expecting `MixinA`
(written **first**) to take precedence if both define the same attribute.
But `class_dict[key] = value` in a loop **overwrites** the previous
value — so for `MixinA` to "win", it has to be processed **last**.
Iterating in reverse order is exactly what makes that happen.

**Slot collisions are fatal, not silently overwritten.** Unlike ordinary
attributes/methods (where an override is intentional and fine), a
**slot-name** collision is always an error — either against the base
structural class (`raise_mixin_slot_collision_with_base_class`), or
between two mixins (`raise_mixin_slot_collision`). Two mixins sharing the
same slot would overwrite each other's memory location — a hard-to-spot,
silent bug — which is why it's treated as a hard error right at
compilation time.

**`IGNORED_DICT_KEYS`** — a set of keys that are never copied from a
mixin's namespace (`__dict__`, `__weakref__`, `__slots__` itself,
`__doc__`, `__module__`, `__init_subclass__`, `__extend_instance_class__`).
Either it's framework "boilerplate" that would clutter the target class,
or (in the case of `__extend_instance_class__`) it's a hook that's
processed separately, **after** the class is compiled (see
`_extend_instance_class` below).

**`init_mixins` isn't copied like a plain attribute** — if the key is
exactly `"init_mixins"`, instead of being written directly into
`class_dict`, the function is added to the `init_mixins` list (step 3), so
`_build_combined_init_mixins` can chain it together with all the others.

[▲ Back to Contents](#-contents)

---

## `_build_combined_init_mixins` — chaining initialization

**Parameters:** `init_mixins_hooks` (a list of functions).

**Return value:** a single merged function, `combined_init_mixins`.

**Under the hood:**
```python
def _build_combined_init_mixins(init_mixins_hooks):
    def combined_init_mixins(self):
        for init_mixin in init_mixins_hooks:
            init_mixin(self)
    return combined_init_mixins
```

Trivial at a glance, but architecturally important: instead of a chain of
`super().init_mixins()` calls (which, in a dynamically assembled
hierarchy, would mean relying on the MRO), all the collected `init_mixins`
hooks are called **explicitly and sequentially** in a single closed-over
function. The same principle as "no `super()`" in `create_composite_init`
(see [README_COMPOSITE_CLASS](README_COMPOSITE_CLASS.md#create_composite_init--the-constructor)) — a consistent
preference for explicit, deterministic ordering over an implicit MRO-based
resolution.

[▲ Back to Contents](#-contents)

---

## `_extend_instance_class` — post-compilation hooks

**Parameters:** `mixins` (the flattened tuple), `instance_class` (the
already-compiled class).

**Return value:** `None` — mutates `instance_class` **in place**.

**Under the hood:**
```python
def _extend_instance_class(mixins, instance_class):
    for mixin in mixins:
        if "__extend_instance_class__" in mixin.__dict__:
            raw_attr = mixin.__dict__["__extend_instance_class__"]
            if not isinstance(raw_attr, (staticmethod, classmethod)):
                raise_invalide_extend_instance_class_definition(instance_class, mixin)
            mixin.__extend_instance_class__(instance_class)
```

This hook is an **escape hatch** for mixins that need more than just a
static `class_dict` merge — typically mixins like `InnersProperty` or
`Equalizer`, which need to dynamically generate properties/setters **only
after** the final class is done (because, for example, they need to know
the complete `__mixins__` set, or other information that's only available
on the compiled class).

**Reading `mixin.__dict__` directly, not `getattr`** — this is
deliberately read straight from the class dictionary, to avoid triggering
premature descriptor evaluation (`getattr` could invoke `__get__` and
accidentally call the method).

**`@staticmethod`/`@classmethod` is enforced.** A plain instance method
wouldn't make sense here — the hook is called at the **class** level, not
the instance level (the instance doesn't even exist yet, only the
compiled class).

**Returns `None`, mutates in place** — the same convention as
`list.sort()` in Python: it signals that `instance_class` was changed
directly in memory, not that a new class is returned.

[▲ Back to Contents](#-contents)
