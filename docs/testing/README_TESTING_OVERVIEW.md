# 🧪 `testing` — Overview of the testing toolkit

The `simplibs.object.testing` package is a set of tools for writing
**your own** tests — whether you're testing the library itself, or (much
more commonly) testing **your own** `SimpleConstant`/`SimpleObject`
classes and mixins in your project. The goal is simple: write one readable
declaration instead of dozens of hand-written `assert` statements, while
still covering every important aspect of behavior — inheritance, instance
creation, validation, reactivity, mutability.

---

## 🧭 Contents

* [Three entry points](#three-entry-points)
* [The shared design pattern](#the-shared-design-pattern)
* [Quick start](#quick-start)
* [Where to find what](#where-to-find-what)
* [Supplementary tools outside `testing`](#supplementary-tools-outside-testing)

[⬅️ Back to main README](../../README.md)

---

## Three entry points

The package offers three functions, each for a different level of
granularity:

| Function                   | Tests                                                                                                                           | Document                                             |
|:---------------------------|:--------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------|
| **`assert_simple_mixin`**  | one specific mixin — inheritance, injection, slots/attributes/methods                                                           | [README_MIXIN_TESTING](README_MIXIN_TESTING.md)      |
| **`assert_simple_object`** | one blueprint (`SimpleConstant`/`SimpleObject`) — inheritance, instantiation, values, reactivity, mutability, lifecycle methods | [README_OBJECT_TESTING](README_OBJECT_TESTING.md)    |
| **`bulk_test`**            | any batch of both at once, with a single call                                                                                   | [README_BULK_TEST](README_BULK_TEST.md)              |

The typical workflow: start with `assert_simple_object`/`assert_simple_mixin`
for the individual classes you're currently developing, and once you have
several, move to `bulk_test` with a batch of `ObjectCase`/`MixinCase`
(or even just plain tuples), so the whole test suite stays readable in a
single file.

[▲ Back to Contents](#-contents)

---

## The shared design pattern

All three entry points (and their internal sub-asserts) share the same
architectural philosophy, which is worth knowing up front:

* **Orchestrator + isolated sub-asserts.** Every high-level function
  (`assert_simple_mixin`, `assert_simple_object`) is just a sequence of
  calls to small, single-purpose functions (`assert_class_inheritance`,
  `assert_value_change`, ...). The sub-asserts can also be used on their
  own, if you only need to test one specific aspect.
* **Phases: shallow → parameter (opt-in) → deep.** The basic structural
  checks always run; parameter tests (reactivity, mutability, specific
  values) only run if you pass the matching argument (the `UNSET` sentinel
  means "I don't want to test this"); deep tests (`deep_check=True`, on by
  default) also verify internal mechanisms like mixin injection or
  `_validate`/`_logic`/`_decompose`.
* **Guard clauses wherever continuing would be misleading.** If instance
  creation fails, there's no point continuing to tests that build on that
  instance — every function, after a key step, asks "did that work?" and,
  if not, stops with a clear error instead of a downstream
  `AttributeError`.
* **`maybe_subtest` for isolated reporting.** Every logical step runs in
  its own pytest subtest (from `simplibs.exception.testing`) — so one
  failure in the middle of a long test doesn't hide errors that would
  otherwise have come after it; the report shows exactly which specific
  step failed.
* **The `UNSET` sentinel as "I don't care about this".** Used
  consistently throughout the whole suite for opt-in parameters — the
  same sentinel the library uses everywhere else (see
  [`simplibs.sentinels`](../../../simplibs-sentinels/README.md)), not
  some one-off, testing-specific convention.

[▲ Back to Contents](#-contents)

---

## Quick start

Testing a single constant, including mutability and validation:

```python
def test_age(subtests):
    assert_simple_object(
        subtests,
        Age,
        test_value_change=25,
        test_mutability=30,
        test_immutability=40,
    )
```

Testing a composition, including bidirectional reactivity:

```python
def test_full_name(subtests):
    assert_simple_object(
        subtests,
        FullName,
        test_reactivity_up=InnerValue("first_name", "Jane"),
        test_reactivity_down="John Smith",
    )
```

Testing a mixin:

```python
def test_snapshot_mixin(subtests):
    assert_simple_mixin(
        subtests,
        Snapshot,
        test_class=Age,
        method_names=("take_snapshot", "restore_snapshot"),
    )
```

Testing a whole batch at once:

```python
def test_all(subtests):
    bulk_test(subtests, [
        Age,
        (FullName, ()),
        (Snapshot, Age),
        ObjectCase(test_class=Weight, test_mutability=80.5),
    ])
```

[▲ Back to Contents](#-contents)

---

## Where to find what

```
testing/
├── assert_simple_mixin.py          ──► README_MIXIN_TESTING.md
├── assert_simple_object.py         ──► README_OBJECT_TESTING.md
├── bulk_test.py                    ──► README_BULK_TEST.md
├── asserts/
│   ├── mixins/          (4 functions)  ──► README_MIXIN_TESTING.md
│   ├── base/             (4 functions) ──► README_OBJECT_TESTING.md
│   ├── methods/          (3 functions) ──► README_OBJECT_TESTING.md
│   ├── mutability/       (2 functions) ──► README_OBJECT_TESTING.md
│   └── reactivity/       (2 functions) ──► README_OBJECT_TESTING.md
└── containers/
    ├── TestMixin.py                ──► README_BULK_TEST.md
    ├── InnerValue.py               ──► README_BULK_TEST.md
    ├── ObjectCase.py               ──► README_BULK_TEST.md
    └── MixinCase.py                ──► README_BULK_TEST.md
```

[▲ Back to Contents](#-contents)

---

## Supplementary tools outside `testing`

Two sets of tools from the `tools/` folder pair well with the testing
toolkit, even though they're not formally part of it:

* **[README_AUTOMATE_CREATORS](../tools/README_AUTOMATE_CREATORS.md)** —
  `create_simple_object`/`create_constant_class`/`create_object_class`
  let you create a blueprint **programmatically**, at runtime. This is
  handy for quickly assembling test blueprints right inside a test
  (without having to write a `class` definition in production code just
  for the test), or for parametrized tests generated from data.
* **[README_RANDOMIZE](../tools/README_RANDOMIZE.md)** —
  `randomize_value`/`random_data_filler` can fill an instance (or an
  entire composition tree) with random, but valid, values. This is a
  handy complement to `assert_simple_object` for **fuzz testing** —
  instead of manually chosen test values, try out behavior across many
  random inputs, including stress-testing the reactive mechanism (see the
  [note on the reactive stress test](../tools/README_RANDOMIZE.md#random_data_filler--the-whole-tree)).

[▲ Back to Contents](#-contents)
