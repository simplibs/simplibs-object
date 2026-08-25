# 🧠 `SimpleMeta` — The metaclass that runs the whole lifecycle

`SimpleMeta` is the brain of the whole Simple system. While `SimpleBase`,
`SimpleConstant`, and `SimpleObject` describe *what* the user is allowed to
declare, `SimpleMeta` controls *what happens with it* — from the moment the
class is defined all the way to the creation of a running instance.

```
SimpleBase(metaclass=SimpleMeta)
└── SimpleConstant
    └── SimpleObject
```

The metaclass takes care of five things, in this order. And it's not a
coincidence — it mirrors a class's natural lifecycle: creation → protection
→ instantiation → representation → metadata access.

---

## 🧭 Contents

* [`__new__` — class creation](#__new__--class-creation)
* [`__setattr__` — write-once protection](#__setattr__--write-once-protection)
* [`__call__` — creating instances](#__call__--creating-instances)
* [`__repr__` and `__str__` — representation](#__repr__-and-__str__--representation)
* [`meta` — metadata access](#meta--metadata-access)
* [Recommended dunder method order](#recommended-dunder-method-order)

[⬅️ Back to main README](../../README.md)

---

## `__new__` — class creation

Runs the moment Python processes the definition of a new class
(`class Age(SimpleConstant): ...`).

```python
def __new__(mcls, name, bases, namespace):
    cls = super().__new__(mcls, name, bases, namespace)

    if hasattr(cls, "_is_instance_class") or name in BASE_CLASS_NAMES:
        return cls

    calculated_metadata = (
        SimpleObjectMetadata(owner_class=cls)
        if hasattr(cls, "_inners")
        else SimpleConstantMetadata(owner_class=cls)
    )
    cls.__metadata__ = calculated_metadata

    return cls
```

Three important details:

**1. Distinguishing constant vs. composition is a single `hasattr`
check.** The system never forces the user to explicitly say "this is a
composition" — it's enough for the class to define `_inners`, and the
metaclass figures out on its own that it needs `SimpleObjectMetadata`
instead of `SimpleConstantMetadata`. A simple, but elegant, decision rule.

**2. A double guard against infinite recursion / needless work.** `name in
BASE_CLASS_NAMES` skips the system classes (`SimpleBase`, `SimpleConstant`,
`SimpleObject` themselves — those don't get any metadata at all).
`hasattr(cls, "_is_instance_class")` skips **dynamically created runtime
classes** (atomic and composite instances created via
`make_atom_class`/`make_composite_class`) — these go through the same
metaclass (they inherit `_type`/`_inners` etc. from the blueprint), but
their metadata is already computed, and recomputing it would be both
wasteful and wrong. This is exactly the point where the declarative world
(blueprints) meets the runtime world (instances).

**3. Metadata is computed once and permanently attached to the class.**
`cls.__metadata__ = calculated_metadata` — from this point on, the metadata
for the given class is complete, computed, and (thanks to the `__setattr__`
below) immutable.

[▲ Back to Contents](#-contents)

---

## `__setattr__` — write-once protection

Runs on **every** attribute assignment at the class level.

```python
def __setattr__(cls, attr_name, new_value):
    if attr_name in cls.__dict__:
        raise_attribut_allready_set(cls, attr_name, new_value)
    super().__setattr__(attr_name, new_value)
```

The check is deliberately `attr_name in cls.__dict__`, not `getattr(cls,
attr_name, UNSET) is not UNSET` (see the commented-out line in the code) —
the difference matters: `cls.__dict__` only guards attributes defined
**directly on this class**, not inherited ones. If the check went through
`getattr`, it would be impossible to set anything at all in a subclass,
because it would always hit the inherited value from the parent.

**Why a blueprint has to be write-once:** once `__new__` has run and the
metadata has been computed, the rest of the system (validation, default
computation, instance builders) relies on the class definition never
changing again. If `_type` or `_default` could be overwritten at runtime,
the metadata would instantly go stale and nobody would know. Write-once
protection eliminates this risk entirely — any attempt to overwrite results
in an immediate, clear error instead of a silent, inconsistent state.

[▲ Back to Contents](#-contents)

---

## `__call__` — creating instances

Runs when a blueprint class is *called like a function*
(`Age()`, `Person(mutable=False)`).

```python
def __call__(cls, *, mixins=(), as_atom=False, mutable=True):
    return create_instance(cls, mixins=mixins, as_atom=as_atom, mutable=mutable)
```

`SimpleMeta` itself contains no logic here — it just delegates to
`create_instance`, a separate, much more complex orchestrator of the whole
instance-creation process. A brief overview of what happens under the hood
(detailed documentation will be in a dedicated README about instance
builders):

1. **Input validation** — `cls` must not be a system base class, `as_atom`
   and `mutable` must be `bool`.
2. **Deciding atom vs. composite** (`is_atom = cls.meta.is_constant or
   as_atom`) — a constant is always an atom; a composition can be forced
   into atomic behavior via `as_atom=True`.
3. **Hashability check for immutable** — an immutable value must be
   hashable, otherwise it wouldn't make sense as immutable.
4. **Selecting the structural base class** (`get_base_class`) — chosen from
   the combination of atom/composite × mutable/immutable.
5. **Compiling the final runtime class** (`create_instance_class`) —
   processing mixins, building the namespace, slots, extension hooks.
6. **Allocating raw memory** via `object.__new__` — without prematurely
   running the parent classes' `__init__`.
7. **Initialization** (`instance.__init__()`).
8. **Returning the finished instance.**

The key idea is **two-phase construction**: first the runtime class is
compiled once (`create_instance_class`), and only then is an instance
allocated from it. This separation means the dynamic class creation (the
expensive part) happens once per given combination of parameters, not
repeatedly for every single instance.

### Where the actual runtime classes come from

Internally, `create_instance` reaches for two "factories" that live in
`_core/metadata/instance_builders/`:

* **`make_atom_class(meta, mutable=...)`** — creates an atomic instance
  class. It inherits from two parents: `InstanceBase` (identity,
  `_is_instance_class`, slots, metadata access) and `meta.owner_class`
  (the domain behavior from the blueprint). It adds the slots `_value`,
  `_owner`, `_locked`, a finished `__init__`, a `value` property, and, for
  the mutable variant, `_root_value_setter` for reactive writes. Finally,
  it **removes the declarative artifacts** (`_type`, `_default`,
  `_validate`, ...) — an instance has no access to the schema, only to the
  result.
* **`make_composite_class(meta, mutable=...)`** — builds a composite
  instance class **on top of the atomic one** (`class_parents =
  (base_class,)`, where `base_class` is precisely
  `atom_class_mutable`/`atom_class_immutable`). It adds a slot for every
  inner element (`inner.meta.name_private`), properties for accessing each
  individual `_inners` element, and, for the mutable variant, the reactive
  hooks `_recalculate_self` and `_recalculate_inners` — this is exactly the
  mechanism that makes a change in one inner element trigger an immediate
  recalculation of the whole composition.

Both functions share the same pattern: **build the name → choose the
parents → build the `class_dict` → `type(name, bases, dict)` → clean up
declarative leftovers.** Using `type(...)` instead of `exec` keeps the whole
compilation safe and explicit — no generated source code, no string
parsing.

And `InstanceBase` is the common root of both — it gives them
`_is_instance_class = True` (so `SimpleMeta.__new__` doesn't treat them as
new blueprints, see above), `__slots__ = ("__weakref__",)` (no `__dict__`,
weak-reference support), fast metadata access (the `meta` property reads
`__metadata__` directly off the class), and diagnostic
`__repr__`/`__str__`.

[▲ Back to Contents](#-contents)

---

## `__repr__` and `__str__` — representation

```python
def __repr__(cls):
    return (
        f"<class {cls.__name__} (System Base)>"
        if cls.meta is UNSET else
        f"<{cls.meta.class_name}Blueprint blueprint='{cls.meta.blueprint_path}' "
        f"type={'Constant' if cls.meta.is_constant else 'Object'}>"
    )

def __str__(cls):
    return cls.__name__
```

`__repr__` is a technical, debugging-oriented representation of the
**blueprint** (not the instance) — it shows the hierarchy path and whether
it's a constant or a composition. `__str__` is deliberately terse — just
the plain class name, suitable for logs and human-readable output.

[▲ Back to Contents](#-contents)

---

## `meta` — metadata access

```python
@property
def meta(cls) -> "SimpleMetadataLike":
    return cls.__metadata__
```

The stable public interface to the metadata — everywhere in the system
(validation, `calculate_value`, `decompose_value`, instance builders)
access goes through `cls.meta`, never directly through `cls.__metadata__`.
This one level of indirection means the internal metadata storage can
change in the future without having to rewrite anything else in the
library.

[▲ Back to Contents](#-contents)

---

## Recommended dunder method order

The order used in `SimpleMeta` (`__new__` → `__setattr__` → `__call__` →
`__repr__` → `__str__` → `meta`) matches a class's natural lifecycle:
**creation → protection → instantiation → representation → metadata
access.** It's also the order CPython itself uses for its own metaclasses,
and the order most established frameworks follow — so it can be taken as a
recommended convention for any other metaclasses in the ecosystem too.

➡️ Deeper documentation on metadata and instance creation
(`SimpleBaseMetadata`, `SimpleConstantMetadata`, `SimpleObjectMetadata`,
`make_atom_class`, `make_composite_class`, `create_instance`) will be in
the follow-up README, once we get to that section per the outline.

[▲ Back to Contents](#-contents)
