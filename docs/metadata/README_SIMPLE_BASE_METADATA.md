# 🧱 `SimpleBaseMetadata` — Foundation for all metadata

`SimpleBaseMetadata` is the common ancestor of `SimpleConstantMetadata` and
`SimpleObjectMetadata`. It doesn't compute any domain-specific data itself
(type, default, `_inners`...) — it's responsible exclusively for the things
**every single** metadata instance needs: name identity, namespace
bookkeeping, a readable hierarchy path, and immutability.

```
SimpleBaseMetadata           ← you are here
├── SimpleConstantMetadata
│   └── SimpleObjectMetadata
```

---

## 🧭 Contents

* [Initialization pipeline](#initialization-pipeline)
* [Name identity (`create_names`)](#name-identity-create_names)
* [Hierarchy path (`calculate_blueprint_path`)](#hierarchy-path-calculate_blueprint_path)
* [The write-once rule](#the-write-once-rule)
* [Subclass architecture](#subclass-architecture)

[⬅️ Back to main README](../../README.md)

---

## Initialization pipeline

```python
def __init__(self, owner_class):
    self.owner_class = owner_class
    self.class_name = owner_class.__name__
    (self.name_tuple, self.name_snake, self.name_private) = create_names(owner_class)
    self.node_names_set = {self.name_snake}
    self.blueprint_path = calculate_blueprint_path(owner_class)
    self._process_user_data()
```

Five deterministic steps, always in the same order:

1. **Owner reference** — `owner_class`, i.e. the class the metadata is
   being computed for.
2. **Name identity** — four derived variants of the class name (see below).
3. **Namespace bookkeeping** (`node_names_set`) — starts as a one-element
   set containing the class's own `name_snake`. Subclasses
   (`SimpleObjectMetadata`) extend it, while processing `_inners`, with the
   names of all nested elements — this is the mechanism the system uses to
   enforce **globally unique names across the whole composition tree**
   (see
   [README_SIMPLE_OBJECT_METADATA](README_SIMPLE_OBJECT_METADATA.md#name-collisions)).
4. **Blueprint path** — a readable representation of the position within
   the inheritance hierarchy.
5. **Subclass hook** (`_process_user_data`) — an empty method that
   `SimpleConstantMetadata`/`SimpleObjectMetadata` override with their own
   domain logic.

[▲ Back to Contents](#-contents)

---

## Name identity (`create_names`)

`create_names` generates three derived variants from the class name, each
for a different purpose:

| Variant        | Format                     | Purpose                                      |
|:---------------|:---------------------------|:---------------------------------------------|
| `name_tuple`   | `("My", "HTTP", "Client")` | semantic units with capitalization preserved |
| `name_snake`   | `"my_http_client"`         | parameter names, internal keys               |
| `name_private` | `"_my_http_client"`        | private slots and internal attributes        |

The principle is **"split first, then normalize"**: `_class_name_splitter`
breaks the PascalCase name into semantic units (validating along the way
that the name is a valid identifier, purely ASCII, and free of
underscores), while `create_names` only joins those units afterward and
normalizes them to `snake_case`. The separation of responsibilities is
strict — the splitter knows nothing about the concept of "snake_case", and
`create_names` knows nothing about PascalCase splitting rules.

**Word-boundary detection** in the splitter also handles acronyms:

```text
MyClass       → ("My", "Class")
HTTPServer    → ("HTTP", "Server")
User123       → ("User", "123")
MyHTTPClient  → ("My", "HTTP", "Client")
```

The key trick is in the behavior at the acronym → word boundary
(`HTTPServer`): when a lowercase letter follows a run of uppercase letters,
the last uppercase letter is "given back" and becomes the start of a new
word (`Server`), while the rest (`HTTP`) is closed off as its own unit.
Without this step, `HTTPServer` would end up as a single word instead of
two.

All three variants are **derived from one another, not built
independently** — `name_snake` always comes from `name_tuple`,
`name_private` always comes from `name_snake`. This guarantees they can
never end up inconsistent with each other.

[▲ Back to Contents](#-contents)

---

## Hierarchy path (`calculate_blueprint_path`)

Builds a readable representation of inheritance for `__repr__` purposes
(see
[README_SIMPLE_META](README_SIMPLE_META.md#__repr__-and-__str__--representation))
— showing which **domain** (not system) parents the class inherits from.

```python
def calculate_blueprint_path(cls):
    from .....SimpleBase import SimpleBase
    parents = [
        base.__name__ for base in cls.__mro__
        if issubclass(base, SimpleBase)
        and base.__name__ not in BASE_CLASS_NAMES
        and base is not cls
    ]
    return cls.__name__ if not parents else f"{cls.__name__}({', '.join(parents)})"
```

It filters the MRO (`__mro__`) on three conditions at once: the parent
must be part of the Simple ecosystem (`issubclass(base, SimpleBase)`), it
must not be the framework's own root
(`SimpleBase`/`SimpleConstant`/`SimpleObject` from `BASE_CLASS_NAMES`), and
it must not be the class itself.

| Hierarchy                               | Output                      |
|:----------------------------------------|:----------------------------|
| `MyConstant(SimpleConstant)`            | `"MyConstant"`              |
| `MyObject(BaseObject, SimpleObject)`    | `"MyObject(BaseObject)"`    |
| `Child(ParentA, ParentB, SimpleObject)` | `"Child(ParentA, ParentB)"` |

The `SimpleBase` import is deliberately local (inside the function) — this
avoids a circular dependency during the early import of the metadata
module, when `SimpleBase` itself might still be in the process of being
defined.

[▲ Back to Contents](#-contents)

---

## The write-once rule

```python
def __setattr__(self, attr_name, new_value):
    current_value = getattr(self, attr_name, UNSET)
    if current_value is not UNSET:
        raise_metadata_is_immutable(attr_name, current_value, new_value, self.owner_class)
    super().__setattr__(attr_name, new_value)
```

The same principle as `SimpleMeta.__setattr__` at the class level (see
[README_SIMPLE_META](README_SIMPLE_META.md#__setattr__--write-once-protection)),
applied here at the **metadata instance** level: a field may be set exactly
once. As long as its value is `UNSET`, assignment goes through; once it's
been set, any further write attempt raises `raise_metadata_is_immutable`.

This is why `__slots__` in `SimpleBaseMetadata` only lists field names
(`owner_class`, `class_name`, ...) without default values — the fields
"don't exist" until `__init__` (or, more precisely, `_process_user_data`)
actually sets them, and `getattr(self, attr_name, UNSET)` returns `UNSET`
for anything not yet assigned.

[▲ Back to Contents](#-contents)

---

## Subclass architecture

The key rule for anyone wanting to extend the metadata system: **subclasses
must not override `__init__`.** All custom initialization belongs in
`_process_user_data()`.

This guarantees that:

* name identity is always computed the same way,
* `node_names_set` is always initialized consistently,
* `blueprint_path` is always generated,
* the metadata structure is predictable across the whole system.

`SimpleBaseMetadata` itself is deliberately lightweight — all the heavy
logic is delegated to specialized processors (`create_names`,
`calculate_blueprint_path`, and, in subclasses, `process_type`,
`process_default_for_constant`, `process_inners`, `process_classmethod`).
The metadata object is created once per class and is never mutated.

➡️ Next: [README_SIMPLE_CONSTANT_METADATA](README_SIMPLE_CONSTANT_METADATA.md)

[▲ Back to Contents](#-contents)
