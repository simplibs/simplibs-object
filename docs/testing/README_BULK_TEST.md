# 📦 Batch testing — `bulk_test` and its containers

`bulk_test` is the last layer of the testing suite — it lets you run an
**entire batch** of tests (objects and mixins, in any combination) with a
single call inside one pytest test function, instead of writing dozens of
separate `def test_...` functions. It supports two writing styles: quick
(plain classes and tuples) and declarative (`ObjectCase`/`MixinCase`
containers).

```
bulk_test                          (polymorphic dispatcher)
├── ObjectCase.run_test()  ──► assert_simple_object(README_OBJECT_TESTING.md)
├── MixinCase.run_test()   ──► assert_simple_mixin(README_MIXIN_TESTING.md)
├── a plain SimpleConstant/SimpleObject class  ──► assert_simple_object (no mixins)
├── (class, mixins)  ──► assert_simple_object (with mixins)
└── (mixin, class)   ──► assert_simple_mixin
```

---

## 🧭 Contents

* [`bulk_test` — the polymorphic dispatcher](#bulk_test--the-polymorphic-dispatcher)
* [`TestMixin` — a synthetic test double](#testmixin--a-synthetic-test-double)
* [`InnerValue` — an address inside the tree](#innervalue--an-address-inside-the-tree)
* [`ObjectCase` and `MixinCase` — declarative specifications](#objectcase-and-mixincase--declarative-specifications)

[⬅️ Back to main README](../../README.md)

---

## `bulk_test` — the polymorphic dispatcher

**Parameters:** `subtests`, `items` (a list/tuple of arbitrarily mixed
items), `verbose` (default `True`), `deep_check` (default `True`).

**Return value:** `None` (runs the asserts directly).

**Five recognized item shapes, tested in this order:**

```python
for item in items:
    if isinstance(item, ObjectCase):
        item.run_test(subtests, ...)
        continue

    if isinstance(item, MixinCase):
        item.run_test(subtests, ...)
        continue

    if isinstance(item, type) and issubclass(item, SimpleConstant):
        assert_simple_object(subtests, item, mixins=UNSET, ...)
        continue

    if isinstance(item, tuple) and len(item) == 2:
        # (SimpleConstant class, tuple of mixins) → assert_simple_object with mixins
        # (mixin, SimpleConstant class) → assert_simple_mixin
        ...
        continue

    raise AssertionError(f"Unsupported bulk test item: {item!r}")
```

**Distinguishing the two variants of a two-element tuple is type
detection, not positional convention.** `(cls, mixins)` vs. `(mixin_class,
test_class)` — both are syntactically a `tuple` of length 2, so the
dispatcher has to inspect the **types** of both elements to know which
variant it's looking at:

```python
cls, mixins = item
if (isinstance(cls, type) and issubclass(cls, SimpleConstant)
    and isinstance(mixins, tuple) and all(issubclass(m, SimpleMixin) for m in mixins)):
    # → object + mixins

mixin_class, test_class = item
if (isinstance(mixin_class, type) and issubclass(mixin_class, SimpleMixin)
    and isinstance(test_class, type) and issubclass(test_class, SimpleConstant)):
    # → mixin + test class
```

Both conditions are tried in order (first "object + mixins", then "mixin +
class") — and because they're mutually exclusive by type (a
`SimpleConstant` subclass can't also be a `SimpleMixin` subclass), there's
no possibility of a collision. Anything that doesn't match any of the five
recognized shapes ends up raising an explicit `AssertionError` —
a **fail-fast** principle: better to immediately report an invalid batch
item than to silently skip it and let the user think the test ran.

**`intro` is auto-generated from the class name**
(`f"object_{cls.__name__}::"`, `f"mixin_{mixin_class.__name__}::"`) —
thanks to this, even a batch of dozens of items run all at once produces
**readable, mutually distinguishable** subtest names in pytest's output,
without the user having to write it out manually for every item.

[▲ Back to Contents](#-contents)

---

## `TestMixin` — a synthetic test double

A special mixin that **doesn't exist for production use** — its sole
purpose is to serve as a "universal X-ray" for verifying that the mixin
injection mechanism (see
[README_CREATE_INSTANCE](../metadata/instance/README_CREATE_INSTANCE.md)) works correctly
on any target class.

```python
class TestMixin(SimpleMixin):
    __test__ = False  # pytest shouldn't treat it as a test class

    _constant_only = False
    _composite_only = False
    _mutable_only = False
    _immutable_only = False
    _only_types = UNSET

    __slots__ = ("_test_slot",)

    def init_mixins(self) -> None:
        self._test_slot = "test_value"

    @property
    def test_property(self) -> str: ...

    def test_method(self) -> str: ...

    @staticmethod
    def __extend_instance_class__(instance_cls: type) -> type:
        setattr(instance_cls, "test_class_attribute", "class_level_ok")
        def test_class_method(self) -> str: return "class_method_ok"
        setattr(instance_cls, "test_class_method", test_class_method)
        return instance_cls
```

**Every compatibility flag is turned off (`False`/`UNSET`)** — this is
deliberate and important. `TestMixin` has to be attachable to **absolutely
any** combination of atom/composition × mutable/immutable, because its job
is to test the injection mechanism independently of whatever specific
`test_class` you happen to be testing against (see
[`_verify_mixin_compatibility`](../metadata/instance/README_CREATE_INSTANCE.md#_verify_mixin_compatibility--the-compatibility-matrix)
— if `TestMixin` had, say, `_constant_only = True`, it would fail on
compositions).

**Covers all five injection paths at once, with a single mixin:**

| Mechanism                     | What it verifies                                                                                                                                                                                                    |
|:------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `__slots__ = ("_test_slot",)` | slot allocation on the dynamic class                                                                                                                                                                                |
| `init_mixins`                 | the initialization hook runs (see [`_build_combined_init_mixins`](../metadata/instance/README_CREATE_INSTANCE.md#_build_combined_init_mixins--chaining-initialization))                                             |
| `test_property`               | a property (getter and setter) was copied into the namespace correctly                                                                                                                                              |
| `test_method`                 | an instance method works and sees the state set in `init_mixins`                                                                                                                                                    |
| `__extend_instance_class__`   | the post-compilation hook (see [`_extend_instance_class`](../metadata/instance/README_CREATE_INSTANCE.md#_extend_instance_class--post-compilation-hooks)) works and can add both class-level attributes and methods |

`__test__ = False` is a purely technical detail for pytest — without it,
pytest might try to "discover" `TestMixin` as a test class itself (since
its name starts with `Test...`), which would generate a false warning.

[▲ Back to Contents](#-contents)

---

## `InnerValue` — an address inside the tree

A **dataclass** (`frozen=True`) representing a "path + value" pair for
testing nested composition elements — used by
`assert_value_change`/`assert_reactivity_upward` (see
[README_OBJECT_TESTING](README_OBJECT_TESTING.md#parameter-assert_value_change--the-universal-core)).

**Fields:** `path` (a dot-notation `str`, or `Iterable[str]`), `value`
(`Any`).

**Path normalization in `__post_init__`:**
```python
if isinstance(self.path, str):
    parts = self.path.split(".")
else:
    parts = tuple(self.path)

if not parts:
    raise_inner_value_empty_path()
for part in parts:
    if not isinstance(part, str):
        raise_inner_value_invalid_path_type(self.path, part)

object.__setattr__(self, "path", tuple(parts))
```

**Two ways to write the path, one normalized result** —
`InnerValue("engine.pistons", 4)` and `InnerValue(("engine", "pistons"),
4)` end up exactly the same after `__post_init__`. This is the same
"accept a convenient input, normalize it to a unified internal
representation" pattern you know from
[`assert_mixins_slots_values`](README_MIXIN_TESTING.md#assert_mixins_slots_values--checking-slot-values)
— just applied to a tree path instead of a name/value pair.

**`object.__setattr__` on a frozen dataclass** — `InnerValue` is
`frozen=True` (an immutable, hashable value), so plain `self.path =
tuple(parts)` would fail with `FrozenInstanceError`. `object.__setattr__(self,
"path", ...)` bypasses this lock exactly once, inside `__post_init__` — a
legitimate, common pattern for frozen dataclasses, when you need to
compute/normalize a field during initialization.

**Navigating the tree — `as_instance_tuple`:**
```python
def as_instance_tuple(self, instance):
    current = instance
    for part in self.path:
        inner_prop = f"{part}_instance"
        if not hasattr(current, inner_prop):
            return UNSET
        current = getattr(current, inner_prop)
        if current is None:
            return UNSET
    return current, self.value
```

**Uses the `<name>_instance` convention**, i.e. exactly the property
generated by `create_properties_for_inner` (see
[README_VALUE_PROPERTIES](../metadata/instance/README_VALUE_PROPERTIES.md#create_properties_for_inner--both-together-for-one-element))
— so `InnerValue("engine", 4)` internally reaches for
`instance.engine_instance`, not `instance.engine` (which would return the
value, not the instance you could keep navigating deeper into the tree
from). Returns `UNSET` (not an exception) on any navigation failure — the
caller (`assert_value_change`) then handles that as a `pytest.fail` with
context, instead of the test crashing on an unattributed `AttributeError`
from deep inside the helper function.

[▲ Back to Contents](#-contents)

---

## `ObjectCase` and `MixinCase` — declarative specifications

Two `dataclass`es (`slots=True, kw_only=True`) that do exactly one thing:
**wrap the parameters** of `assert_simple_object`/`assert_simple_mixin`
into a named, reusable object.

```python
@dataclass(slots=True, kw_only=True)
class ObjectCase:
    test_class: "SimpleClassLike"
    mixins: tuple[...] | UnsetType = UNSET
    test_value_change: Any | InnerValue | UnsetType = UNSET
    test_reactivity_up: InnerValue | UnsetType = UNSET
    test_reactivity_down: Any | UnsetType = UNSET
    test_mutability: Any | InnerValue | UnsetType = UNSET
    test_immutability: Any | InnerValue | UnsetType = UNSET

    def run_test(self, subtests, *, verbose=True, intro="", deep_check=True):
        from ..assert_simple_object import assert_simple_object
        return assert_simple_object(subtests, self.test_class, mixins=self.mixins, ...)
```

`MixinCase` is structurally the same idea, just mirroring
`assert_simple_mixin`'s parameters (`mixin_class`, `test_class`,
`slots_names`, `slots_values`, `attribute_names`, `method_names`).

**Why does this wrapper even exist, when `bulk_test` already handles plain
tuples?** Tuples (`(cls, mixins)`, `(mixin, cls)`) only cover the **most
common** parameters — they don't leave room for `test_reactivity_up`,
`slots_values`, and similar finer-grained settings. `ObjectCase`/
`MixinCase`, on the other hand, expose the **entire** range of parameters
the orchestrators support, and they're **named** as well — more readable
than a positionally-packed tuple, especially in a large test suite where
test cases get shared/imported across files in the repository.

**The local import inside `run_test`** (`from ..assert_simple_object import
assert_simple_object`) — not at the top of the module — is a deliberate
resolution of a circular dependency: `assert_simple_object` internally
imports `ObjectCase` (for type annotations), so an import at the top of
`ObjectCase.py` would create a cycle. An import inside the method is only
evaluated when `run_test()` is actually called, by which point both
modules are already fully loaded.

[▲ Back to Contents](#-contents)

➡️ Next: [README_TESTING_OVERVIEW](README_TESTING_OVERVIEW.md)
