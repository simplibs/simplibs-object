# 🧱 `SimpleMixin` — The foundation for building your own mixins

`SimpleMixin` is the root class that **absolutely every** mixin in the
Simple system has to inherit from. It doesn't do anything functional on
its own — its job is to give mixins a shared identity, declarative
compatibility flags, and, above all, **strict structural validation at
definition time**, because mixins (unlike regular Python inheritance) get
injected directly into the `class_dict` of dynamically created instance
classes (see
[README_CREATE_INSTANCE](../../metadata/instance/README_CREATE_INSTANCE.md#_build_instance_class_dict--namespace-injection))
— any structural error there would propagate dangerously and illegibly.

```
SimpleMixin (metaclass=SimpleMixinMeta)
├── NodesTuple, NodesDicts, Snapshot, ...   (core_mixins)
└── your own mixin
```

---

## 🧭 Contents

* [Declarative compatibility flags](#declarative-compatibility-flags)
* [`__slots__` and `init_mixins`](#__slots__-and-init_mixins)
* [`SimpleMixinMeta` — validation at definition time, identity at runtime](#simplemixinmeta--validation-at-definition-time-identity-at-runtime)
* [`_verify_mixin_definition` — everything that's checked](#_verify_mixin_definition--everything-thats-checked)

[⬅️ Back to main README](../../../README.md)

---

## Declarative compatibility flags

```python
class SimpleMixin(metaclass=SimpleMixinMeta):
    _constant_only: bool = False
    _composite_only: bool = False
    _mutable_only: bool = False
    _immutable_only: bool = False
    _only_types: "ValidTypes" = UNSET

    __slots__ = ()

    def init_mixins(self) -> None:
        pass
```

Five flags a custom mixin can override to declare which instances it's
allowed to attach to — exactly the ones `_verify_mixin_compatibility`
actually enforces on every instance creation (see
[README_CREATE_INSTANCE](../../metadata/instance/README_CREATE_INSTANCE.md#_verify_mixin_compatibility--the-compatibility-matrix)):

| Flag              | Restricts to                                                     |
|:------------------|:-----------------------------------------------------------------|
| `_constant_only`  | atomic instances only                                            |
| `_composite_only` | composite instances only                                         |
| `_mutable_only`   | mutable instances only                                           |
| `_immutable_only` | immutable instances only                                         |
| `_only_types`     | only instances whose `meta.default` matches the given type/union |

**The default values are always "no restriction"** (`False`/`UNSET`) — a
mixin that doesn't override any flag can be attached anywhere. That's
exactly why `TestMixin` (see
[README_BULK_TEST](../../testing/README_BULK_TEST.md#testmixin--a-synthetic-test-double))
leaves every flag at its default — it needs to work universally.

[▲ Back to Contents](#-contents)

---

## `__slots__` and `init_mixins`

**`__slots__ = ()`** on `SimpleMixin` itself is just the default value —
in reality, **every specific mixin** has to define its own `__slots__`
explicitly, even if it's empty. This isn't just a convention, it's
**enforced** by validation (see
[`_verify_mixin_definition`](#_verify_mixin_definition--everything-thats-checked)
below) — without an explicit `__slots__`, a mixin doesn't even pass
definition.

**`init_mixins` is an isolated hook, not a chain through `super()`.** The
method's docstring says this directly: a mixin that overrides
`init_mixins` **must not** call `super().init_mixins()`. The reason is
architectural — mixins aren't composed via the MRO, so `super()` chaining
wouldn't make sense here (and couldn't work reliably either). Instead, the
instance builder collects `init_mixins` from every mixin separately and
chains them together itself into a single function
(`_build_combined_init_mixins`, see
[README_CREATE_INSTANCE](../../metadata/instance/README_CREATE_INSTANCE.md#_build_combined_init_mixins--chaining-initialization)).
So your mixin should write `init_mixins` as if it were the **only** mixin
in the world — set only its own slots, nothing more.

[▲ Back to Contents](#-contents)

---

## `SimpleMixinMeta` — validation at definition time, identity at runtime

The `SimpleMixin` metaclass handles two independent things.

### 1. Validation at definition time (`__init__`)

```python
def __init__(cls, name, bases, dct, **kwargs):
    super().__init__(name, bases, dct, **kwargs)
    if bases:
        _verify_mixin_definition(cls)
```

**`if bases:`** — a one-line but important condition. `SimpleMixin`
itself has an empty `bases` tuple (it doesn't inherit from anything except
`object`), so validation couldn't be run on it (and it wouldn't make sense
anyway — it's the root, not a concrete mixin). Every **derived** class
(where `bases` isn't empty) is validated immediately at definition time —
a **fail-fast** principle: an incorrectly defined mixin never gets a
chance to slip deeper into the system and fail later, illegibly, in the
middle of compiling some specific instance.

### 2. Identity at runtime (`__instancecheck__`)

```python
def __instancecheck__(cls, instance):
    if super().__instancecheck__(instance):
        return True
    mixins = getattr(instance, "__mixins__", ())
    return any(issubclass(m, cls) for m in mixins)
```

This solves a specific problem: because mixins are **not** in the MRO of
the resulting instance class (they're flattened into `class_dict`, see
[README_CREATE_INSTANCE](../../metadata/instance/README_CREATE_INSTANCE.md#create_instance_class--compiling-the-final-class)),
a plain `isinstance(obj, MyMixin)` would **always return `False`** without
this override — Python would look for `MyMixin` in the MRO and wouldn't
find it there.

The solution is two-step: first try the standard MRO check (`super()...`,
just in case a mixin ever does end up directly in the MRO), and if that
doesn't succeed, reach for `instance.__mixins__` — the flat tuple of every
mixin that `_build_instance_class_dict` stored on the class (see
[README_CREATE_INSTANCE](../../metadata/instance/README_CREATE_INSTANCE.md#_build_instance_class_dict--namespace-injection))
— and check whether `cls` itself, or one of its subclasses, is in there
(`issubclass(m, cls)`). Thanks to this, `isinstance(instance, Snapshot)`
works exactly the way a user would intuitively expect, even though it's
technically a "trick" compared to the standard Python mechanism.

[▲ Back to Contents](#-contents)

---

## `_verify_mixin_definition` — everything that's checked

Nine steps, run once when each specific mixin is defined:

```
1. __slots__ MUST be in cls.__dict__ (explicitly defined, not inherited)
2. slots MUST be a tuple or str
3. every item in slots MUST be a str
4. slots MUST NOT contain forbidden names (FORBIDDEN_NAMES)
5. the class-level namespace MUST NOT contain forbidden names
6. the compatibility flags (RESTRICTION_FLAGS) MUST be bool, if defined
7. _only_types MUST have one of the supported forms (UNSET / type / tuple[type] / Union)
8. init_mixins MUST NOT call super() (checked via co_names bytecode inspection)
```

**Step 1 is the strictest and most important** — without an explicit
`__slots__`, a mixin doesn't pass at all. This enforces what was mentioned
above: every mixin has to declare its own memory layout, otherwise there'd
be a risk of a mixin accidentally getting a `__dict__` (and, with it,
unlimited, uncontrolled attribute additions that would break the rest of
the system's guarantees about a predictable instance layout).

**Steps 4–5 (forbidden names) protect the system's internal API.**
`FORBIDDEN_NAMES` contains names that already have their own, fixed
meaning in the system (e.g. `_value`, `_owner`, `value`, `meta` —
overriding `init_mixins` would be the exception to this exception: note
that `init_mixins` is a legitimate, overridable hook, whereas
`FORBIDDEN_NAMES` guards more against internal structural attributes like
`_value`/`_owner`/`_locked`). If a mixin defined a slot or attribute with
the same name, a **silent collision** would occur — the mixin's attribute
would either overwrite, or be overwritten by, the system's own, with no
warning at runtime at all. Validation catches this immediately and
clearly, at definition time.

**Step 8 is the only check that reads bytecode directly**
(`func.__code__.co_names`) instead of using AST or string searching — a
fast, reliable way to detect whether the `init_mixins` function references
the name `super` **anywhere** inside itself. This check is a direct
enforcement of the rule described above ("no `super()` chaining") —
without it, an incorrect call to `super().init_mixins()` could lead to a
confusing `AttributeError` only at runtime, deep inside the instance
builder, instead of a clear error right at the mixin's definition.

[▲ Back to Contents](#-contents)

