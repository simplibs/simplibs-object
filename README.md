# 🧬 `simplibs-object`

[![PyPI](https://img.shields.io/pypi/v/simplibs-object)](https://pypi.org/project/simplibs-object/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](https://github.com/simplibs/simplibs-object/blob/main/LICENSE)

**A system for building deterministic, type-safe, and reactive objects.**


`simplibs-object` is a library for **declarative data modeling**.

Instead of writing constructors, setters, validators, and manually recalculating
dependencies, you define a class and tell it what type it has, what its default
value is, what it's composed of, and how the resulting value is built from those
parts. The library takes care of the rest.

```bash
pip install simplibs-object
```

---

The library is built on three simple building blocks:

* **`SimpleConstant`** — an atomic value,
* **`SimpleObject`** — a composition of other objects,
* **`SimpleMixin`** — a capability that can be added to an object.

These blocks can be combined into simple objects as well as larger structures.

For example, you might write:

```python
class Age(SimpleConstant):
    _type = int
    _default = 20
```

or:

```python
class Person(SimpleObject):
    _type = str
    _inners = (FirstName, LastName)

    @classmethod
    def _logic(cls, first_name, last_name):
        return f"{first_name} {last_name}"
```

And that's it — no constructors to write, no validation, no manual checks.

The library knows that the `Age` constant holds an `int`, knows its default
value, and prepares an object with the matching interface.

A composition is then an object made up of constants and other objects, and its
resulting value is derived from theirs.

That's the core principle of the whole library.

---

## 🏛️ Architecture at a glance

The whole system can be understood, in simplified form, as a series of layers:

```text
┌────────────────────────────────┐
│      Definition classes        │ ◄── SimpleBase, SimpleConstant, SimpleObject
└──────────────┬─────────────────┘     (what the user writes)
               ▼
┌────────────────────────────────┐
│      Metadata process          │ ◄── SimpleMeta and *Metadata classes
└──────────────┬─────────────────┘     (validation and compilation at definition time)
               ▼
┌────────────────────────────────┐
│      Instance creation         │ ◄── atom/composite × mutable/immutable, mixin injection
└──────────────┬─────────────────┘     (dynamically creates a new class and instance)
               ▼
┌────────────────────────────────┐
│            Mixins              │ ◄── optional capabilities
└──────────────┬─────────────────┘     (extensibility without touching the core)
               ▼
┌────────────────────────────────┐
│      Tools & testing           │ ◄── automate_creators, randomize, and testing utilities
└────────────────────────────────┘     (makes life easier for developers)
```

Each layer has its own responsibility and can be studied in more detail on its own.

---
## 🧩 Definition classes

`SimpleBase`
is the root of the hierarchy — purely architectural, not used directly.

`SimpleConstant`
defines an atom (`_type`, `_default`, optional `_validate`) and the public API
for validation and normalization.

`SimpleObject`
extends `SimpleConstant` with composition (`_inners`, `_logic`, optional
`_decompose`) — its `_default` is never written by hand; it's always derived
automatically from `_logic(inners' defaults)`.

➡️ [README_SIMPLE_BASE](https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_BASE.md)  
➡️ [README_SIMPLE_CONSTANT](https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_CONSTANT.md)  
➡️ [README_SIMPLE_OBJECT](https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_OBJECT.md)  

---

### Defining constants

When you write, for example:

```python
class Age(SimpleConstant):
    _type = int
    _default = 18
```

you no longer need to write a constructor by hand, store the value, check its
type, or write a setter.

The library derives the necessary behavior from the definition.

```python
age = Age()

age.value = 25
```

If you need to add a custom rule, you can simply do so:

```python
class Age(SimpleConstant):
    _type = int
    _default = 18

    @classmethod
    def _validate(cls, value, *, return_bool=False):
        if value < 0:
            return cls.bool_or_raise_validate_error(
                value,
                "Age cannot be negative.",
                return_bool=return_bool,
            )
        return True
```

This gives you an object that knows its type, its default value, and the rules
for what counts as a valid value.

---

### Composition and reactivity

The library's strength becomes much more apparent once objects start being
composed of other objects.

`SimpleObject` defines:

* `_inners` — what objects it's composed of,
* `_logic` — how the resulting value is built from them,
* `_decompose` — how the resulting value can optionally be decomposed back.

For example:

```python
class FullName(SimpleObject):
    _type = str
    _inners = (FirstName, LastName)

    @classmethod
    def _logic(cls, first_name, last_name):
        return f"{first_name} {last_name}"
```

A change to an inner value is automatically propagated to the composition:

```python
person.first_name = "Peter"

# person.value == "Peter Smith"
```

And if the composition supports `_decompose`, the reverse direction also works:

```text
          ┌───────────────┐
          │   FullName    │
          │ "Peter Smith" │
          └───────┬───────┘
                  │
             _decompose
              ↙       ↘
       ┌──────────┐ ┌─────────┐
       │ FirstName│ │LastName │
       │  "Peter" │ │ "Smith" │
       └──────────┘ └─────────┘
```

This makes the library build a **bidirectionally reactive tree of values**:

* changes inside propagate up toward the root,
* a composition's change can be decomposed down toward its parts.

An important property here is determinism — recalculation isn't based on a
hidden event system or magic dependencies. The relationships between the parts
are determined entirely by the object's own definition.

---

## 🧠 Metadata process

Behind the declarative layer sits the `SimpleMeta` metaclass and the metadata
system.

`SimpleMeta`
is the metaclass that governs a class's entire lifecycle — creation, write-once
protection, instance creation, and representation.

When a class is defined, its metadata is computed and permanently fixed:
`SimpleBaseMetadata` → `SimpleConstantMetadata` → `SimpleObjectMetadata`
A dry run is performed, along with validation of the provided attributes and
methods.


Every element is checked:

* `_type` — whether it matches the default value,
* `_default` — whether it passes validation,
* `_inners` — whether they're composed of `SimpleObject`/`SimpleConstant`
  classes and don't contain conflicting names,
* `_validate` — whether it can correctly validate a value,
* `_logic` — whether it can compute its own default from the inners' default
  values,
* `_decompose` — whether it can compute the inners' default values from its
  own default.

This means definition errors can surface **at class-creation time**, rather
than later when the object is actually used.

The metadata also serves as a fixed description of the blueprint, from which a
concrete runtime instance is later prepared.

➡️ [README_SIMPLE_META](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_META.md)  
➡️ [README_SIMPLE_BASE_METADATA](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_BASE_METADATA.md)  
➡️ [README_SIMPLE_CONSTANT_METADATA](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_CONSTANT_METADATA.md)  
➡️ [README_SIMPLE_OBJECT_METADATA](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_OBJECT_METADATA.md)  
➡️ [README_METHOD_PROCESSING](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_METHOD_PROCESSING.md)  

---

## 🧱 Instance creation

A blueprint is not itself an instance.

The actual runtime instance is created through dynamic compilation —
`make_atom_class` and `make_composite_class` assemble a concrete class with
slots, properties, and (for compositions) reactive hooks, and `create_instance`
safely attaches mixins to it via namespace injection. This avoids `__slots__`
conflicts while keeping a flat MRO regardless of how many mixins are used.

When an object is created, the library assembles a concrete runtime class
based on the definition and prepares everything it needs:

* slots,
* properties,
* validation,
* reactive mechanisms,
* inner objects,
* any mixins.

The instance therefore contains only what it actually needs.

Thanks to the use of `__slots__` and dynamic runtime-class assembly, there's no
need for a generic instance structure full of methods the given object will
never use.

➡️ [README_ATOM_CLASS](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_ATOM_CLASS.md)  
➡️ [README_COMPOSITE_CLASS](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_COMPOSITE_CLASS.md)  
➡️ [README_CREATE_INSTANCE](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_CREATE_INSTANCE.md)  
➡️ [README_INSTANCE_PROTOCOLS](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_INSTANCE_PROTOCOLS.md)  
➡️ [README_VALUE_PROPERTIES](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_VALUE_PROPERTIES.md)  

---

## 🧩 Mixins

Mixins are what give instances their concrete capabilities — serialization,
comparison, arithmetic, change history, an immutable update API, and much more.

The library ships with a rich set of ready-made mixins, and also offers the
`SimpleMixin` base class so you **can write your own logic**.

A mixin never inherits from `SimpleObject` directly — only from `SimpleMixin`.
When an instance is created, only the structural foundation (type, slots,
validation) is taken from the blueprint (`SimpleObject`/`SimpleConstant`), and
the mixin is layered on top of that.

A custom mixin therefore doesn't need to (and must not) know anything about the
specific domain logic of the class it's applied to — it's a purely separate,
reusable capability.

The library deliberately separates an object's structure from its capabilities:

`SimpleObject` says **what an object is**.

`SimpleMixin` says **what an object can do**.

This means the same structure can be used in different ways, depending on which
capabilities you add to it.


➡️ [README_SIMPLE_MIXIN](https://github.com/simplibs/simplibs-object/blob/main/docs/mixins/base_class/README_SIMPLE_MIXIN.md)  

---

### Overview of available mixins

| Category        | What they provide                                                          |
| ---------------- | --------------------------------------------------------------------------- |
| **Core**          | `NodesTuple`, `NodesDicts`, `Snapshot`, `Infrastructure`, `Serialization`   |
| **Collections**   | `CollectionBase`, `Iterable`, `Mapping`, `Collection`                       |
| **Comparison**    | `Equality`, `Ordering`                                                      |
| **Generics**      | `ClassGetItem`                                                              |
| **Interfaces**    | `Call`, `ContextManager`                                                    |
| **Lifecycles**    | `Copyable`, `PickleState`, `PickleReduce`, `Lifecycle`                      |
| **Numeric**       | `Arithmetic`, `Unary`, `Bitwise`, `Inplace`, `Conversion`                   |
| **Representation**| `ValueDisplay`, `ValueFormatting`                                           |
| **Immutable**     | `ImmutableMethods`, `ImmutableWithInners`                                   |
| **Numerical**     | `Volume`, `Equalizer`                                                       |
| **Properties**    | `InnersProperty`, `MetaShortcuts`                                           |
| **State**         | `DefaultState`, `DirtyTracking`, `History`, `Permission`                    |

A full description of each individual mixin (compatibility flags, slots,
methods, what it builds on) is available in a dedicated overview:

➡️ [README_MIXINS_OVERVIEW](https://github.com/simplibs/simplibs-object/blob/main/docs/mixins/README_MIXINS_OVERVIEW.md)  

---

## 🛠️ Tools & testing

The library isn't limited to manually defining classes by hand — the project
also includes tools for:


- `automate_creators` — Programmatically creating blueprints without writing a
  classic `class` definition.  
➡️ [README_AUTOMATE_CREATORS](https://github.com/simplibs/simplibs-object/blob/main/docs/tools/README_AUTOMATE_CREATORS.md)  


- `bulk` — Bulk creation of blueprints and instances from various inputs, such
  as JSON, YAML, CSV, or Python structures.  
➡️ [README_BULK](https://github.com/simplibs/simplibs-object/blob/main/docs/tools/README_BULK.md)  


- `randomize` — Generating random values for objects and entire composition
  trees. Useful for fuzz testing or quickly generating test data.  
➡️ [README_RANDOMIZE](https://github.com/simplibs/simplibs-object/blob/main/docs/tools/README_RANDOMIZE.md)  



- `testing` — Testing utilities that let you verify whole blueprints or mixins
  without having to write dozens of individual tests by hand.  
➡️ [README_TESTING_OVERVIEW](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_TESTING_OVERVIEW.md)  
➡️ [README_BULK_TEST](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_BULK_TEST.md)  
➡️ [README_MIXIN_TESTING](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_MIXIN_TESTING.md)  
➡️ [README_OBJECT_TESTING](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_OBJECT_TESTING.md)  

---

### ⚠️ Exceptions

Every error the library raises inherits from a common root,
`SimpleObjectError` (built on top of [`simplibs-exception`](https://github.com/simplibs/simplibs-exception) —
structured, readable diagnostic cards instead of a bare traceback).
This means you can catch **any** error from the library with a single
`except SimpleObjectError`, or target just one specific category:

| Exception                     | When it happens |
|--------------------------------|------------------|
| `SimpleDefinitionError`        | An error in a **class definition** — a malformed `_inners`, a disallowed `_default` on a composition, an invalid `_logic` signature. Raised at class import/definition time. |
| `SimpleInitializationError`    | An error during **instance creation** — invalid `mixins`/`mutable` parameters, an incompatible mixin, failure to assemble inner elements. |
| `SimpleRuntimeError`           | An error in **data or at runtime** — an invalid value on write, a failed `_validate`, an attempt to write to an immutable instance. This is the exception you'll run into most often during normal use. |

```python
from simplibs.object.exceptions import SimpleObjectError

try:
    age.value = -5
except SimpleObjectError as e:
    print(e)  # a structured diagnostic card: what, why, how to fix it
```

`SimpleObjectError` also filters the library's own internal frames out of the
error's traceback (`_skip_locations`) — the error message points to **your**
code, not the library's internal implementation.

---

### ⚙️ Settings

The library has one configurable point: logging. There's no automatic handler
setup and no interference with the root logger — everything is opt-in and
fully under your control.

```python
import logging
logging.getLogger("simple").setLevel(logging.DEBUG)
```

You can also register a custom callback that runs on every value change
(`value = ...` at the root level):

```python
import simplibs.object.settings.logging as simple_logging

def my_callback(cls, value, event):
    print(f"{cls.__name__}: {event} -> {value}")

simple_logging.on_value_change = my_callback
```


---

## 🧱 Benefits of the library

Every object has its own type and rules for working with its value.

Depending on the definition, it can have:

* a default value,
* validation,
* normalization,
* composition,
* automatic recalculation,
* mutable or immutable behavior,
* custom mixins.

This means the same foundation can be used for very simple values as well as
for more complex data models.

### Declarative data models

An object's structure can be described with a handful of class attributes
instead of a pile of repetitive boilerplate.

### Validation and normalization

Type checking, default values, and custom validation rules are part of the
object's own definition.

### Reactive calculations

When one part of the model affects another, the change automatically
propagates to the corresponding part of the tree.

This can be useful for things like:

* configuration,
* calculations,
* simulations,
* state models,
* forms,
* API data,
* or your own domain models.

### Immutability

An immutable instance has no setter for changing its value.

Instead of modifying an existing instance, you can create a new one via the
immutable API:

```python
new_age = age.with_value(25)
```

The original instance remains untouched.

---

## 🔭 About the library, from the author's point of view

The library grew out of a simple observation — a recurring pattern of
"type + default + validation + logic" — and a wish to give it a deterministic,
reusable foundation once and for all. It's a bit like a small language of its
own for talking to Python: minimal logic, maximum usefulness. Every function
parameter becomes its own object, and together they form a reactive system.

I plan to use it myself as the foundation for the upcoming `simplibs-validate`
— validation logic, where a `SimpleConstant` with its own `_validate` is
exactly the right building block. But I see the potential as broader than
that: since any constant can be turned into a composition by adding `_inners`,
and any composition can conversely be simplified into a constant (by removing
`_inners`, or by creating an instance with `as_atom=True`), the library can
also be used as a general **declarative building system** — extensible and
specifiable in both directions, starting from the smallest units and building
up. One idea I'd like to try out at some point: using constants as elementary
building blocks and composing descriptions of atoms and molecules out of them
— literally, not in the metaphorical programming sense.

This is the **first version** — the result of all the original ideas, but
definitely not a finished work. It's more of a solid foundation and structure
that's a pleasure to keep building on, than a finished product. Real-world use
will show, over time, what still needs tuning, extending, or rethinking
entirely.


---

## ☯️ About simplibs

All libraries in the **simplibs** (Simple Libraries) ecosystem share a common
engineering philosophy:

* **Dyslexia-friendly:** We actively minimize cognitive load. Code is atomized
  into small, self-contained units, files are named directly after the job
  they do, and explanations focus more on *why* something is designed the way
  it is than just *what* it does.
* **Programmer's peace of mind:** Nothing should be missing, and nothing
  should be redundant. We value clean execution paths and understandable
  architecture over a rushed, disorganized pile of features.
* **Defensive style:** We actively anticipate edge cases and error states, so
  that only safe execution paths remain. Code is built to degrade gracefully,
  not to crash unexpectedly.
* **Minimalism:** Find the most direct path to the goal in as few steps as
  possible, without compromising on safety, readability, or completeness.
* **Code as craft:** Code should be pleasant to look at, readable at a glance,
  and evoke structural harmony. We treat software engineering as a precise
  craft.

---

### 🤝 Contributing and community

This is an **open-source project**, made with care. We deeply value
collaboration with the community and welcome any feedback, bug reports, or
ideas for new features!

* **Want to contribute?** Feel free to open an Issue or send a Pull Request.
* **Want to reach out?** If you'd like to discuss the project further,
  collaborate, or just say hi, open a GitHub Issue or start a Discussion.

---

### 📝 License

This library is released under the **MIT** license. Build great things!

---

[▲ Back to top](#-simplibs-object)