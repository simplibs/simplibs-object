# 🧪 Testing mixins — `assert_simple_mixin` and its building blocks

This document describes a testing suite built specifically for verifying
mixins — whether they correctly inherit from `SimpleMixin`, whether they
can be attached to a blueprint via `mixins=(...)` without error, and
whether, once attached, they actually provide the slots, attributes, and
methods they promise. It's a concrete implementation of the principle
mentioned in the library's history: `assert_simple_mixin` is the main
entry point, and `assert_simple_object`/`assert_simple_mixin` use the same
"orchestrator + isolated sub-asserts" pattern.

```
assert_simple_mixin                    (main orchestrator)
├── assert_mixin_inheritance            (does the mixin inherit from SimpleMixin?)
├── assert_mixin_instance_creation      (can it be attached and an instance created?)
├── assert_instance_hasattr             (do the expected slots/attributes/methods exist?)
└── assert_mixins_slots_values          (do the slots have the expected values?)
```

---

## 🧭 Contents

* [`assert_simple_mixin` — the main orchestrator](#assert_simple_mixin--the-main-orchestrator)
* [`assert_mixin_inheritance` — the inheritance check](#assert_mixin_inheritance--the-inheritance-check)
* [`assert_mixin_instance_creation` — creation and injection](#assert_mixin_instance_creation--creation-and-injection)
* [`assert_instance_hasattr` — the generic presence gate](#assert_instance_hasattr--the-generic-presence-gate)
* [`assert_mixins_slots_values` — checking slot values](#assert_mixins_slots_values--checking-slot-values)
* [How it all fits together](#how-it-all-fits-together)

[⬅️ Back to main README](../../README.md)

---

## `assert_simple_mixin` — the main orchestrator

**Parameters:**
* `subtests` (*Any*): the native pytest `subtests` fixture.
* `mixin_class` (*SimpleMixinType*): the mixin under test.
* `test_class` (*SimpleClassType*): the blueprint class the mixin gets
  attached to.
* `mutable` (*bool*, default `True`).
* `slots_names`, `slots_values`, `attribute_names`, `method_names`
  (optional, default `UNSET`): what to verify on the resulting instance.
* `verbose` (*bool*, default `True`).
* `intro` (*str*, default `""`): a prefix for the subtest names.

**Return value:** the created instance with the mixin attached (for any
further, user-specific tests), or `None`, if the instance creation itself
already failed.

**Two phases, in this order:**

```
1. SHALLOW TESTS (the basic contract)
   ├─ assert_mixin_inheritance
   └─ assert_mixin_instance_creation  ──► returns the instance (or None)

   guard: if instance is None → return None, no further processing

2. PARAMETER TESTS (optional, only if the parameter isn't UNSET)
   ├─ slots_names      → assert_instance_hasattr(kind="slot")
   ├─ slots_values     → assert_mixins_slots_values
   ├─ attribute_names  → assert_instance_hasattr(kind="attribute")
   └─ method_names     → assert_instance_hasattr(kind="method")
```

**Why two separate phases.** The first phase ("shallow") verifies the
**basic contract** — without it, there's no point continuing at all (a
mixin that doesn't inherit from `SimpleMixin`, or can't even be attached,
can't have any meaningful slots/attributes to verify). The second phase is
**opt-in** — each of the four parameters is only tested if the caller
actually supplied it (`is not UNSET`), so the test code isn't forced to
list all four categories even if it only cares about one.

**A guard clause after the first phase** (`if instance is None: return
None`) — if the instance couldn't be created, there's no point trying to
reach its slots/attributes in the second phase — that would only produce
misleading "downstream" errors (`AttributeError` on `None`) instead of one
clear, original cause.

[▲ Back to Contents](#-contents)

---

## `assert_mixin_inheritance` — the inheritance check

**Parameters:** `subtests`, `mixin_class`, `verbose`, `intro`.

**Return value:** `None` (failures are reported via `pytest.fail`).

**Two checks, both inside a single `maybe_subtest` block:**

```python
if not isinstance(mixin_class, type):
    pytest.fail("...is not a class...")

if not issubclass(mixin_class, SimpleMixin):
    pytest.fail("...doesn't inherit from SimpleMixin...")
```

The simplest, and also the most fundamental, "fail-fast" boundary in the
whole suite — it only checks what must hold **before** a mixin can even be
considered a valid building block of the system at all: it has to be a
class (not an instance, not a function), and it has to inherit from
`SimpleMixin`, to be compatible with
`_resolve_flat_mixins`/`_verify_mixin_compatibility` (see
[README_CREATE_INSTANCE](../metadata/instance/README_CREATE_INSTANCE.md#_verify_mixin_compatibility--the-compatibility-matrix)).

[▲ Back to Contents](#-contents)

---

## `assert_mixin_instance_creation` — creation and injection

**Parameters:** `subtests`, `mixin_class`, `test_class`, `mutable`
(default `True`), `verbose`, `intro`.

**Return value:** the created instance, or `None` on failure.

**Four steps, each in its own `maybe_subtest`:**

1. **`test_class` must inherit from `SimpleConstant`** (which also covers
   `SimpleObject`, since it itself inherits from `SimpleConstant` — see
   [README_SIMPLE_OBJECT](../core/README_SIMPLE_OBJECT.md)) — checking that
   the caller passed a valid blueprint, not an arbitrary class.
2. **`mixin_class` must inherit from `SimpleMixin`** — duplicates
   `assert_mixin_inheritance`, but here it's a local, standalone check, so
   this function also works on its own, not only as part of
   `assert_simple_mixin`.
3. **The actual instantiation** — `test_class(mixins=(mixin_class,),
   mutable=mutable)`, wrapped in `try/except`. This is the moment the
   entire pipeline from
   [README_CREATE_INSTANCE](../metadata/instance/README_CREATE_INSTANCE.md) actually runs
   (flattening the mixins, compatibility validation, building
   `class_dict`, compilation). Any exception is converted into a readable
   `pytest.fail` with the original error text included — the test code
   therefore never sees a raw traceback from deep inside the instance
   builder, just a clear, understandable message.
4. **Checking member injection** — verifies that the mixin actually
   "showed up" on the resulting instance (see below).

**Step 4 is the most interesting — how it figures out exactly what the
mixin added:**

```python
base_mixin_attrs = set(dir(SimpleMixin))

mixin_members = {
    name for name in dir(mixin_class)
    if not (name.startswith("__") and name.endswith("__"))
    and name not in base_mixin_attrs
}

missing_members = [name for name in mixin_members if not hasattr(instance, name)]
```

**Set subtraction** (`dir(mixin_class)` minus `dir(SimpleMixin)`) is an
elegant trick — instead of the test needing to know in advance exactly
what the mixin defines, it simply compares "what the mixin has on top of
the plain `SimpleMixin` base" and verifies that exactly that set of names
also exists on the resulting instance. The dunder-method filter
(`startswith("__") and endswith("__")`) additionally excludes standard
Python machinery (`__class__`, `__init__`, etc.), which would otherwise
falsely look like a "missing member" due to how dynamic classes work.

**This mechanism is, to some extent, self-testing** — you don't have to
manually list `method_names=(...)` in `assert_simple_mixin` for every
method a mixin defines; step 4 catches this automatically for
**anything** non-trivial the mixin adds. The `slots_names`/
`attribute_names`/`method_names` parameters of `assert_simple_mixin` are
more for **explicit, targeted** checking of specific names (and,
critically, specific values via `slots_values`), not for basic presence
detection.

[▲ Back to Contents](#-contents)

---

## `assert_instance_hasattr` — the generic presence gate

**Parameters:** `subtests`, `instance`, `names` (a tuple of str), `kind`
(str — for labels in the error message), `verbose`, `intro`.

**Return value:** `None`.

**Two-stage validation with a guard clause between the steps:**

```python
# 1. Input validation — names must be a tuple of strings
if not isinstance(names, tuple): pytest.fail(...); is_valid_input = False
for name in names:
    if not isinstance(name, str): pytest.fail(...); is_valid_input = False

if not is_valid_input:
    return  # guard clause

# 2. Presence check — only now
for name in names:
    if not hasattr(instance, name):
        pytest.fail(f"...Available attributes: {dir(instance)}")
```

This function is a **reusable, general-purpose building block** — it
doesn't just check slots, or just attributes, or just methods; the `kind`
parameter is purely cosmetic (it changes the text of the error message:
"slot", "attribute", "method"), but the checking mechanism (`hasattr`) is
identical for all three cases. Thanks to this, `assert_simple_mixin` calls
this **single** function three times (for `slots_names`, `attribute_names`,
`method_names`), instead of having three nearly identical, duplicated
implementations.

**The guard clause between input validation and the presence check** is
the same pattern you know from `assert_simple_mixin` itself — if `names`
isn't a valid tuple of strings, there's no point iterating over it and
calling `hasattr` with invalid names, which would produce misleading
downstream errors.

**`dir(instance)` in the error message** — when the test fails on a
missing attribute, the message directly lists the **complete set of what
the instance actually has** — saving debugging time, since there's no
need to run `dir()` manually in a debugger.

[▲ Back to Contents](#-contents)

---

## `assert_mixins_slots_values` — checking slot values

**Parameters:** `subtests`, `instance`, `slots_values` (a flexible format
— see below), `verbose`, `intro`.

**Return value:** `None`.

**Three steps, each with its own guard clause:**

```python
# 1. Input normalization — two supported shapes
if isinstance(slots_values, tuple) and len(slots_values) == 2 and isinstance(slots_values[0], str):
    normalized = (slots_values,)          # a single pair: ("slot", value)
elif isinstance(slots_values, tuple):
    normalized = slots_values             # a sequence of pairs: (("s1", v1), ("s2", v2))
else:
    pytest.fail(...); normalized = None

if normalized is None:
    return  # guard clause

# 2. Validating the structure of each pair
for pair in normalized:
    if not (isinstance(pair, tuple) and len(pair) == 2): pytest.fail(...); return
    name, _ = pair
    if not isinstance(name, str): pytest.fail(...); return

# 3. The actual check — presence and value
for name, expected_value in normalized:
    if not hasattr(instance, name): pytest.fail(...)
    actual_value = getattr(instance, name)
    if actual_value != expected_value: pytest.fail(...)
```

**A flexible input format solves a common source of test friction.** When
a mixin defines only **one** slot, it's annoying to write
`slots_values=(("my_slot", value),)` — a nested tuple just for consistency
with the multi-element case. Step 1 removes this inconvenience: it
recognizes, based on shape (`len == 2` and the first element is `str`),
whether it's a single pair or a sequence of pairs, and normalizes both to
the same internal representation (a `tuple` of tuples). This "accept both
reasonable input shapes, unify them right at the start" pattern is the
same philosophy as `_class_name_splitter` → `create_names` ("split first,
normalize later"), just applied to a test parameter instead of a class
name.

**Checking the value is the very last step, after two layers of structural
validation** — first it has to be confirmed that `slots_values` even has a
sensible shape (step 1), then that every pair really is a two-element
tuple with a string name (step 2), and only then (step 3) does it check
whether the slot **exists** and **has the correct value**. This gradual
narrowing ensures the error message always points to the **first, most
fundamental** problem, not to a confusing downstream consequence of
badly-structured input.

[▲ Back to Contents](#-contents)

---

## How it all fits together

```
assert_simple_mixin(subtests, MyMixin, test_class=MyConstant, slots_values=(("_counter", 0),))
│
├─ assert_mixin_inheritance(MyMixin)
│     → MyMixin must inherit from SimpleMixin
│
├─ assert_mixin_instance_creation(MyMixin, MyConstant)
│     → MyConstant(mixins=(MyMixin,)) is actually created successfully
│     → all non-dunder, non-SimpleMixin members of MyMixin are present on the instance
│     → returns the finished instance
│
└─ (since slots_values isn't UNSET)
      assert_mixins_slots_values(instance, (("_counter", 0),))
         → instance._counter exists and equals 0
```

The return value of `assert_simple_mixin` (the finished instance with the
mixin) is deliberately useful even **after** all the built-in checks have
run — the test function can keep using it for its own, domain-specific
asserts (calling a mixin method, checking behavior after a mutation, and
so on), without having to manually repeat the whole instantiation
procedure.

Together, the whole suite forms **one, reusable tool** that can test any
of the mixins mentioned in the library's history (`NodesTuple`,
`Snapshot`, `NodesDicts`, `Infrastructure`, `Serialization`, and all the
`others`/`dunders` subcategories) — with the same unified pattern,
regardless of what the specific mixin does internally.

[▲ Back to Contents](#-contents)
