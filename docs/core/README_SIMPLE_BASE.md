# 🧱 `SimpleBase` — Root of the whole hierarchy

`SimpleBase` is the lowest layer of the whole Simple system. It doesn't do
anything on its own — its only job is to give all declarative classes
(`SimpleConstant`, `SimpleObject`) a shared identity and hook them up to the
`SimpleMeta` metaclass, which is what actually brings real behavior to life.

```
SimpleBase             (metaclass=SimpleMeta, no declarative logic)
└── SimpleConstant     (atom: _type, _default, _validate)
    └── SimpleObject   (composition: _inners, _logic, _decompose)
```

---

## 🧭 Contents

* [Why this class exists at all](#why-this-class-exists-at-all)
* [`__slots__`](#__slots__)
* [`__metadata__`](#__metadata__)
* [Architectural role](#architectural-role)

[⬅️ Back to main README](../../README.md)

---

## Why this class exists at all

Without `SimpleBase`, both `SimpleConstant` and `SimpleObject` would have to
separately hook themselves up to `SimpleMeta`, and each would need its own
placeholder for metadata. By pulling this out into a shared root, the whole
system has a single place where it's historically decided "from now on, every
class in this hierarchy is a Simple class" — and that place never needs to
change.

```python
class SimpleBase(metaclass=SimpleMeta):
    __slots__ = ()
    __metadata__: "SimpleMetadataLike" = UNSET
```

The class is **never used directly** — there's no scenario where you'd
inherit straight from `SimpleBase`. It's a purely architectural "anchor
point," not a functional building block.

[▲ Back to Contents](#-contents)

---

## `__slots__`

```python
__slots__ = ()
```

An empty slot tuple doesn't mean "no data" — it means "no *own* data".
`SimpleBase` simply guarantees that `__dict__` (and, with it, unlimited,
uncontrolled runtime attribute additions) never enters the hierarchy from the
start. Every subclass has to define its own `__slots__` to keep this benefit
— `SimpleBase` itself just sets it as the default standard.

The benefit here is purely about performance and memory: smaller instances,
faster attribute access, a predictable memory layout.

[▲ Back to Contents](#-contents)

---

## `__metadata__`

```python
__metadata__: "SimpleMetadataLike" = UNSET
```

This is a placeholder, not a real value. `SimpleBase` (and system classes in
general) doesn't have — and doesn't need — any metadata; `UNSET` here simply
guarantees that the `__metadata__` attribute **exists** on every class in the
hierarchy, even before `SimpleMeta.__new__` fills it in with real, computed
metadata for a specific user-defined declarative class.

Thanks to this, the rest of the system can safely assume "`__metadata__`
exists on this class" without having to handle an `AttributeError` at the
edges of the hierarchy.

[▲ Back to Contents](#-contents)

---

## Architectural role

`SimpleBase`, in short:

* unifies inheritance — a single common ancestor for both atoms and
  compositions,
* provides a stable anchor for the metaclass's behavior,
* guarantees that every Simple class shares the same structural foundation
  (slots, presence of `__metadata__`).

It's the "root node" of the whole Simple ecosystem — deliberately minimal, so
it doesn't clutter the public API with anything unnecessary. All actual
behavior is defined later, in `SimpleConstant`, `SimpleObject`, and in
`SimpleMeta` itself.

➡️ Next: [README_SIMPLE_CONSTANT](README_SIMPLE_CONSTANT.md)

[▲ Back to Contents](#-contents)
