# 🧪 Testing objects and constants — `assert_simple_object`

While [README_MIXIN_TESTING](README_MIXIN_TESTING.md) tests mixins
themselves, this document tests **blueprints** — the `SimpleConstant` and
`SimpleObject` classes you wrote. It verifies inheritance, instance
creation, value changes, bidirectional reactivity, mutability, and the
internal lifecycle methods (`_validate`, `_logic`, `_decompose`) — all
through one unified entry point.

```
assert_simple_object                    (main orchestrator, 3 phases)
├── SHALLOW
│   ├── assert_class_inheritance
│   └── assert_user_instance_creation
├── PARAMETER (opt-in)
│   ├── assert_value_change
│   ├── assert_reactivity_upward
│   ├── assert_reactivity_downward
│   ├── assert_mutable_behavior
│   └── assert_immutable_behavior
└── DEEP (deep_check=True)
    ├── assert_instance_creation        (with TestMixin)
    ├── assert_validate_method
    ├── assert_calculate_value_method
    └── assert_decompose_value_method
```

---

## 🧭 Contents

* [`assert_simple_object` — the main orchestrator](#assert_simple_object--the-main-orchestrator)
* [Shallow: `assert_class_inheritance`](#shallow-assert_class_inheritance)
* [Shallow: `assert_user_instance_creation`](#shallow-assert_user_instance_creation)
* [Parameter: `assert_value_change` — the universal core](#parameter-assert_value_change--the-universal-core)
* [Parameter: `ssert_reactivity_upward`](#parameter-assert_reactivity_upward)
* [Parameter: `assert_reactivity_downward`](#parameter-assert_reactivity_downward)
* [Parameter: `assert_mutable_behavior` and `ssert_immutable_behavior`](#parameter-assert_mutable_behavior-and-assert_immutable_behavior)
* [Deep: `assert_instance_creation` — synthetically, with `TestMixin`](#deep-assert_instance_creation--synthetically-with-testmixin)
* [Deep: `assert_validate_method`](#deep-assert_validate_method)
* [Deep: `assert_calculate_value_method` and `assert_decompose_value_method`](#deep-assert_calculate_value_method-and-assert_decompose_value_method)

[⬅️ Back to main README](../../README.md)

---

## `assert_simple_object` — the main orchestrator

**Parameters:**
* `subtests`, `test_class` (required).
* `mixins` (default `UNSET`): mixins for the user instance.
* `test_value_change`, `test_reactivity_up`, `test_reactivity_down`,
  `test_mutability`, `test_immutability` (all default `UNSET`) — opt-in
  parameter tests.
* `verbose` (default `True`), `intro` (default `""`).
* `deep_check` (default `True`): turns on the third, "deep" phase.

**Return value:** the created user instance (with any mixins).

**Three phases, the same pattern as `assert_simple_mixin`** (see
[README_MIXIN_TESTING](README_MIXIN_TESTING.md)) — shallow → parameter
(opt-in) → here with an extra, third **deep** phase:

```python
# SHALLOW
assert_class_inheritance(subtests, test_class, ...)
instance = assert_user_instance_creation(subtests, test_class, mixins=mixins, ...)

# PARAMETER (only when the parameter isn't UNSET)
if test_value_change is not UNSET: assert_value_change(...)
if test_reactivity_up is not UNSET: assert_reactivity_upward(...)
if test_reactivity_down is not UNSET: assert_reactivity_downward(...)
if test_mutability is not UNSET: assert_mutable_behavior(...)
if test_immutability is not UNSET: assert_immutable_behavior(...)

# DEEP (only when deep_check=True)
if deep_check:
    assert_instance_creation(subtests, test_class, ...)
    if "_validate" in test_class.__dict__: assert_validate_method(...)
    if "_logic" in test_class.__dict__: assert_calculate_value_method(...)
    if "_decompose" in test_class.__dict__ and test_class.meta.is_decomposeable:
        assert_decompose_value_method(...)
```

**The deep phase only tests what the user actually overrode.** Notice the
conditions `"_validate" in test_class.__dict__` — exactly the same local
presence pattern used by `verify_classmethod` (see
[README_METHOD_PROCESSING](../metadata/README_METHOD_PROCESSING.md#verify_classmethod--the-gate-validate-clone-or-inherit)).
There's no point unit-testing `_decompose` if the class doesn't define it
at all (the inherited default implementation returns `UNSET`, and testing
that would be pointless) — and `test_class.meta.is_decomposeable`
additionally guards against the case where `_decompose` is defined, but
the composition still isn't fully decomposable anyway (because some inner
element isn't decomposable, see
[README_SIMPLE_OBJECT_METADATA](../metadata/README_SIMPLE_OBJECT_METADATA.md)).

**The `verbose_value_change` cascade** — a subtle but well-thought-out
detail:

```python
verbose_value_change = test_value_change is UNSET
# ... after assert_reactivity_upward:
verbose_value_change = verbose_value_change or test_reactivity_up is UNSET
# ... after assert_reactivity_downward:
verbose_value_change = verbose_value_change or test_reactivity_down is UNSET
```

Several parameter tests (`assert_reactivity_upward`,
`assert_reactivity_downward`, `assert_mutable_behavior`) internally call
the shared `assert_value_change` (see below). If the user has **already**
explicitly requested the standalone `test_value_change` test, there's no
point reporting the exact same sub-tests **again**, just nested inside
another, higher-level check — that would lead to duplicated, confusing
output. The cascade progressively "turns on" verbose reporting for
`assert_value_change` only if **none** of the preceding tests that would
also use it were requested — as soon as one of them was (`is UNSET` is
`False`), `verbose_value_change` stays off for all the following ones too.

[▲ Back to Contents](#-contents)

---

## Shallow: `assert_class_inheritance`

**Parameters:** `subtests`, `test_class`, `verbose`, `intro`.

**Return value:** `None`.

```python
if not hasattr(test_class, "_inners"):
    assert issubclass(test_class, SimpleConstant)
else:
    assert issubclass(test_class, SimpleObject)
```

The same routing rule as `SimpleMeta.__new__` (see
[README_SIMPLE_META](../metadata/README_SIMPLE_META.md#__new__--class-creation)) — the presence
of `_inners` decides whether the class should behave like an atom or a
composition, and this assert just verifies that the actual inheritance
matches that expectation.

[▲ Back to Contents](#-contents)

---

## Shallow: `assert_user_instance_creation`

**Parameters:** `subtests`, `test_class`, `mixins` (default `UNSET`),
`verbose`, `intro`.

**Return value:** the created instance.

```python
mixins_tuple = () if mixins is UNSET else mixins  # (with type validation)
instance = test_class(mixins=mixins_tuple)
assert instance is not None
```

**Different from `assert_instance_creation`** (the deep phase, see below)
in that it's a **lightweight, user-facing** check — it only verifies that
an instance with the user-specified (or no) combination of mixins can be
created at all, without a deeper structural check of mixin-member
propagation. The returned instance is then the one the rest of
`assert_simple_object` works with during the PARAMETER phase.

[▲ Back to Contents](#-contents)

---

## Parameter: `assert_value_change` — the universal core

**Parameters:** `subtests`, `instance`, `value` (a raw value, or an
`InnerValue`), `verbose`, `intro`.

**Return value:** the applied value (for further chaining).

**Five steps, with a guard clause after each risky one:**

```
1. Determine the target — the root instance, or InnerValue.as_instance_tuple(instance)
   guard: if the path can't be resolved → return None

2. Validate the candidate value (target.validate(value, return_bool=True))
   guard: if invalid → return None (don't attempt the setter with an invalid value)

3. Confirm the value differs from the current one (otherwise the test would prove nothing)
   guard: if the same → return None

4. Write it (target.value = candidate_value), wrapped in try/except

5. Confirm the value actually changed (target.value == candidate_value)
```

**This is the single most important shared function in the whole object
testing suite** — `assert_reactivity_upward`, `assert_reactivity_downward`,
and `assert_mutable_behavior` all delegate the actual mutation to it. The
three guard clauses **before** steps 4–5 aren't there for show: without
them, a test could silently "pass" even though it wasn't actually testing
anything meaningful (e.g. writing the same value the instance already had,
so step 5 would pass trivially, regardless of whether the setter even
works).

**`InnerValue` as polymorphic input** — the `value` parameter accepts
either a plain value (the test applies to `instance` itself), or an
`InnerValue` (the test applies to a nested element, see
[README_BULK_TEST](README_BULK_TEST.md)). This unified signature is what
lets `assert_reactivity_upward` use the **same** function that a simple
root-value test uses — only **where** the value gets written changes, not
the writing mechanism itself.

[▲ Back to Contents](#-contents)

---

## Parameter: `assert_reactivity_upward`

**Parameters:** `subtests`, `instance`, `new_value` (must be `InnerValue`),
`verbose`, `verbose_value_change`, `intro`.

**Return value:** `None`.

```
1. Remember the root's original value (instance.value)
2. new_value MUST be an InnerValue (otherwise fail — a plain value makes
   no sense for a "bottom-up reactivity" test, since there's nothing to bubble)
3. assert_value_change(instance, value=new_value)  ── applies to the INNER element
4. Confirm the root value CHANGED compared to step 1
```

**The test is deliberately simple and independent of the specific
`_logic`.** It doesn't check whether the new root value is "correct" in
any precise sense — only that it changed **at all**. That's enough to
verify that the bubbling mechanism (`_root_value_setter` →
`_recalculate_self`, see
[README_COMPOSITE_CLASS](../metadata/instance/README_COMPOSITE_CLASS.md))
actually works, without having to duplicate the user's `_logic` inside the
test.

[▲ Back to Contents](#-contents)

---

## Parameter: `assert_reactivity_downward`

**Parameters:** `subtests`, `instance`, `new_value` (a raw value for the
root), `verbose`, `verbose_value_change`, `intro`.

**Return value:** `None`.

```
1. instance MUST be a composition (not meta.is_constant)
   guard: an atom → fail (it has no inner elements to test)

2. meta MUST support decomposition (is_decomposeable)
   guard: no → fail

3. assert_value_change(instance, value=new_value)  ── writes to the ROOT
4. expected_values = instance.decompose_value(new_value)
   guard: if decomposition fails → return

5. For every inner: getattr(instance, inner.meta.name_snake) must match
   the corresponding value from expected_values (zipped in order)
```

**Unlike `assert_reactivity_upward`, this test is exact, not just "did it
change".** Because decomposition is a deterministic function
(`decompose_value`), the test can compute **exactly** what value each
inner element should have, and compare 1:1. This is possible precisely
because `_recalculate_inners` (see
[README_COMPOSITE_CLASS](../metadata/instance/README_COMPOSITE_CLASS.md#create_recalculate_inners--value-flow-downward))
uses the very same `decompose_value` method the test calls to compute the
expected value — so the test essentially verifies that the runtime
behavior matches what someone would compute "by hand" from the outside.

[▲ Back to Contents](#-contents)

---

## Parameter: `assert_mutable_behavior` and `assert_immutable_behavior`

Two symmetrical tests, each covering one half of the mutability contract.

### `assert_mutable_behavior`

**Parameters:** `subtests`, `test_class`, `new_value`, `verbose`,
`verbose_value_change`, `intro`.

```
1. instance = test_class(mutable=True)
2. original_id = id(instance)
3. assert_value_change(instance, value=new_value)   ← the actual mutation
4. id(instance) MUST remain the same as original_id
```

### `assert_immutable_behavior`

**Parameters:** `subtests`, `test_class`, `new_value`, `verbose`, `intro`.

```
1. instance = test_class(mutable=False)
2. original_id, original_value = id(instance), instance.value
3. instance.value = new_value  MUST raise an exception
4. id(instance) MUST remain the same
5. instance.value MUST remain the same as original_value
```

**Both tests share the same identity check** (`id(instance)` unchanged),
but with **opposite** expectations for the mutation itself: mutable
**must** succeed and preserve identity, immutable **must** fail and
preserve both identity and value. This symmetry matches exactly how
immutability is implemented at the level of
`create_value_property`/`create_value_setter` — for the immutable variant,
the setter **doesn't exist at all** (see
[README_VALUE_PROPERTIES](../metadata/instance/README_VALUE_PROPERTIES.md)),
so a write attempt never succeeds at the level of Python itself, let alone
at some business validation.

**The identity check matters for both variants** — it confirms the system
implements **real** mutability (an in-place change of state), not an
"immutable-style" object pattern where every "change" would actually
create a new instance. `assert_mutable_behavior` proves that mutation
doesn't create a new instance; `assert_immutable_behavior` proves that a
rejected mutation leaves behind no side effect at all.

[▲ Back to Contents](#-contents)

---

## Deep: `assert_instance_creation` — synthetically, with `TestMixin`

**Parameters:** `subtests`, `test_class`, `verbose`, `intro`.

**Return value:** the created instance, with `TestMixin` attached.

```python
instance = test_class(mixins=(TestMixin,))

assert instance._test_slot == "test_value"                              # slot
assert instance.test_property == "test_value"                           # property
assert instance.test_method() == "[TestMixin] property=test_value"      # method
assert instance.__class__.test_class_attribute == "class_level_ok"      # class attribute
assert instance.test_class_method() == "class_method_ok"                # class method
```

**Unlike `assert_user_instance_creation`, this test doesn't use the
user's mixins — it always uses `TestMixin`.** The purpose is different:
it doesn't verify whether a **specific** user mixin works (that's what
[`assert_simple_mixin`](README_MIXIN_TESTING.md) does), but whether the
**mixin-attachment mechanism in general** works for the given
`test_class` — i.e. whether
`_resolve_flat_mixins`/`_build_instance_class_dict`/`_extend_instance_class`
(see [README_CREATE_INSTANCE](../metadata/instance/README_CREATE_INSTANCE.md))
work correctly on exactly this specific blueprint class. `TestMixin` (see
[README_BULK_TEST](README_BULK_TEST.md#testmixin--a-synthetic-test-double)) is designed to cover **every**
injection path at once — a slot, a property, an instance method, a class
attribute, and a class method (via `__extend_instance_class__`) — in a
single call.

[▲ Back to Contents](#-contents)

---

## Deep: `assert_validate_method`

**Parameters:** `subtests`, `test_class`, `verbose`, `intro`.

**Return value:** `None`.

**Five checks, systematically covering the "happy path" plus two invalid
inputs × two modes:**

```
1. test_class.validate(meta.default, return_bool=True)  MUST be True
2. test_class.validate(UNSET, return_bool=True)          MUST be False
3. test_class.validate(UNSET, return_bool=False)          MUST raise an exception
4. test_class.validate(None, return_bool=True)            MUST be False
5. test_class.validate(None, return_bool=False)           MUST raise an exception
```

**A 2×2 matrix (`UNSET`/`None` × boolean/exception mode) systematically
verifies both halves of the `validate` contract** described in
[README_SIMPLE_CONSTANT](../core/README_SIMPLE_CONSTANT.md) — that
`return_bool=True` always returns a bool without raising, and
`return_bool=False` always either returns success (implicitly), or raises
a structured error, never a mix of the two. `UNSET` and `None` are chosen
as two "universally invalid" inputs, since no meaningful `_type` should
accept either of them — they're reliable negative test cases, independent
of the specific domain of the class under test.

[▲ Back to Contents](#-contents)

---

## Deep: `assert_calculate_value_method` and `assert_decompose_value_method`

Two symmetrical tests for compositions — one for the upward direction
(computation), one for the downward direction (decomposition).

### `assert_calculate_value_method`

```python
params = {inner.meta.name_snake: inner.meta.default for inner in test_class.meta.inners}
calculated = test_class.calculate_value(**params)
assert calculated == test_class.meta.default
```

### `assert_decompose_value_method`

```python
expected = tuple(inner.meta.default for inner in test_class.meta.inners)
decomposed = test_class.decompose_value(test_class.meta.default)
assert decomposed == expected
```

**Both tests work on the same principle — they test against the
defaults, because defaults are the only values the system already knows
for certain are valid and mutually consistent.** Recall that a
composition's `self.default` **is** the result of `_logic`'s dry run over
`_inners`' defaults (see
[README_SIMPLE_OBJECT_METADATA](../metadata/README_SIMPLE_OBJECT_METADATA.md))
— so `assert_calculate_value_method` essentially **repeats** the exact
same computation that already ran once when the class was defined, and
verifies it gives the same result (deterministically, with no side effect
having occurred in between).

**`assert_decompose_value_method` additionally verifies bidirectional
consistency** between `_logic` and `_decompose` — if `_logic(defaults) ==
default` and `_decompose(default) == defaults`, that means the two
functions are genuinely inverses of each other, at least at this one
(default) value. That's exactly the property
`verify_decompose_outcome` (see
[README_METHOD_PROCESSING](../metadata/README_METHOD_PROCESSING.md#verify_decompose_outcome--special-rules-for-_decompose))
checks structurally already at class-definition time — this test just
reconfirms it at the level of behavior, not just type matching.

[▲ Back to Contents](#-contents)

➡️ Next: [README_BULK_TEST](README_BULK_TEST.md)
