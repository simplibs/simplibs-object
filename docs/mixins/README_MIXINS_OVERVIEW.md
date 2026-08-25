# 🧱 Simple Object — Mixins Overview

Mixins are the building blocks of the Simple object system. A user defines a
blueprint class, then combines mixins to assemble a fully-featured runtime instance —
each mixin contributing one property or capability. This document introduces every
mixin available in the ecosystem, grouped by category, with a link to its full
documentation.

**Writing your own mixin?** Any custom mixin must inherit from `SimpleMixin`
(directly or indirectly) to pass structural validation — see
[`SimpleMixin`](base_class/README_SIMPLE_MIXIN.md) for the required contract.

---

## 🧭 Table of Contents

* [Base Class](#base-class)
* [Core Mixins](#core-mixins)
* [Dunders](#dunders)
  * [Collections](#collections)
  * [Comparison](#comparison)
  * [Generics](#generics)
  * [Interfaces](#interfaces)
  * [Lifecycles](#lifecycles)
  * [Numeric](#numeric)
  * [Representation](#representation)
* [Others](#others)
  * [Immutable](#immutable)
  * [Numerical](#numerical)
  * [Properties](#properties)
  * [State](#state)

[⬅️ Back to main README](../../README.md)

---

## Base Class

| Mixin         | Description                                                                                                               |
|:--------------|:--------------------------------------------------------------------------------------------------------------------------|
| `SimpleMixin` | The structural foundation every mixin must inherit from — compatibility flags, `init_mixins` chain, automatic validation. |

➡️ [README_SIMPLE_MIXIN](base_class/README_SIMPLE_MIXIN.md)  

[▲ Back to Contents](#-table-of-contents)

---

## Core Mixins

Shared infrastructure used throughout the ecosystem — not a "feature" category on its
own, but the foundation both `dunders` and `others` build on.

| Mixin            | Description                                                                   |
|:-----------------|:------------------------------------------------------------------------------|
| `NodesTuple`     | Builds `_nodes_tuple`, the flat ordered source of every node in the instance. |
| `NodesDicts`     | Turns `_nodes_tuple` into fast, name-keyed lookup dicts.                      |
| `Snapshot`       | Build, restore, and compare full-state value snapshots.                       |
| `Infrastructure` | Bundles `NodesDicts` + `Snapshot` into one shared base.                       |
| `Serialization`  | Full `to_dict` / `to_json` / `from_dict` / `from_json` API.                   |

➡️ [README_NODES_TUPLE](core_mixins/README_NODES_TUPLE.md)  
➡️ [README_NODES_DICTS](core_mixins/README_NODES_DICTS.md)  
➡️ [README_SNAPSHOT](core_mixins/README_SNAPSHOT.md)  
➡️ [README_INFRASTRUCTURE](core_mixins/README_INFRASTRUCTURE.md)  
➡️ [README_SERIALIZATION](core_mixins/README_SERIALIZATION.md)   

[▲ Back to Contents](#-table-of-contents)

---

## Dunders

Mixins implementing standard Python "dunder" (double-underscore) protocols — the
hooks Python itself looks for to make an object iterable, comparable, callable,
picklable, printable, and so on.

### Collections

Dict-like and iterable behavior over a composite's direct inners.

| Mixin            | Description                                                       |
|:-----------------|:------------------------------------------------------------------|
| `CollectionBase` | Base mapping foundation — `keys()`, `values()`, `items()`.        |
| `Iterable`       | `__iter__`, `__reversed__`, `__dir__` over inner keys.            |
| `Mapping`        | `__getitem__`, `__setitem__`, `__contains__`, `__len__`, `get()`. |
| `Collection`     | Combines `Iterable` + `Mapping` into full dict-like API.          |

➡️ [README_COLLECTION_BASE](dunders/collections/README_COLLECTION_BASE.md)  
➡️ [README_ITERABLE](dunders/collections/README_ITERABLE.md)  
➡️ [README_MAPPING](dunders/collections/README_MAPPING.md)   
➡️ [README_COLLECTION](dunders/collections/main/README_COLLECTION.md)  

[▲ Back to Contents](#-table-of-contents)

---

### Comparison

Value-based equality, hashing, and magnitude ordering.

| Mixin      | Description                                                 |
|:-----------|:------------------------------------------------------------|
| `Equality` | `__eq__` and `__hash__`, mutability-aware hashing strategy. |
| `Ordering` | `__lt__`, `__le__`, `__gt__`, `__ge__` via `self.value`.    |

➡️ [README_EQUALITY](dunders/comparison/README_EQUALITY.md)  
➡️ [README_ORDERING](dunders/comparison/README_ORDERING.md)  

[▲ Back to Contents](#-table-of-contents)

---

### Generics

Generic-style subscript syntax for typing/IDE purposes.

| Mixin          | Description                                                              |
|:---------------|:-------------------------------------------------------------------------|
| `ClassGetItem` | `__class_getitem__` fallback for subscriptable classes (`MyClass[int]`). |

➡️ [README_CLASS_GETITEM](dunders/generics/README_CLASS_GETITEM.md)  


[▲ Back to Contents](#-table-of-contents)

---

### Interfaces

General-purpose Python object protocols.

| Mixin            | Description                                                  |
|:-----------------|:-------------------------------------------------------------|
| `Call`           | `__call__` — syntactic sugar over the `with_any` change API. |
| `ContextManager` | `__enter__` / `__exit__` — inert, no-op context support.     |

➡️ [README_CALL](dunders/interfaces/README_CALL.md)  
➡️ [README_CONTEXT](dunders/interfaces/README_CONTEXT.md)  


[▲ Back to Contents](#-table-of-contents)

---

### Lifecycles

Object lifecycle protocols built on a shared snapshot foundation.

| Mixin         | Description                                                       |
|:--------------|:------------------------------------------------------------------|
| `Copyable`    | `__copy__` / `__deepcopy__` via snapshot.                         |
| `PickleState` | `__getstate__` / `__setstate__` via `to_dict()` / `from_dict()`.  |
| `PicleReduce` | `__reduce__` — top-level pickle protocol hook.                    |
| `Lifecycle`   | Combines `Copyable` + `PicleReduce` for full copy/pickle support. |

➡️ [README_COPYABLE](dunders/lifecycles/README_COPYABLE.md)  
➡️ [README_PICKLE_STATE](dunders/lifecycles/README_PICKLE_STATE.md)  
➡️ [README_PICKLE_REDUCE](dunders/lifecycles/README_PICKLE_REDUCE.md)  
➡️ [README_LIFECYCLE](dunders/lifecycles/main/README_LIFECYCLE.md)  

[▲ Back to Contents](#-table-of-contents)

---

### Numeric

The full range of Python numeric protocols.

| Mixin        | Description                                                   |
|:-------------|:--------------------------------------------------------------|
| `Arithmetic` | `+ - * / // % **` and reflected forms, returns new instances. |
| `Unary`      | `-x`, `+x`, `abs(x)`, returns new instances.                  |
| `Bitwise`    | `& \| ^ << >> ~` for integral atoms only.                     |
| `Inplace`    | `+= -= *= /= //= %= **=`, mutates in place.                   |
| `Conversion` | `int()`, `float()`, `complex()`, `round()`, floor/ceil/trunc. |

➡️ [README_ARITHMETIC](dunders/numeric/README_ARITHMETIC.md)  
➡️ [README_UNARY](dunders/numeric/README_UNARY.md)  
➡️ [README_BITWISE](dunders/numeric/README_BITWISE.md)  
➡️ [README_INPLACE](dunders/numeric/README_INPLACE.md)   
➡️ [README_CONVERSION](dunders/numeric/README_CONVERSION.md)  

[▲ Back to Contents](#-table-of-contents)

---

### Representation

How an instance presents itself as text, bytes, and boolean.

| Mixin             | Description                                                 |
|:------------------|:------------------------------------------------------------|
| `ValueDisplay`    | `__repr__` / `__str__` — value-like display, constant-only. |
| `ValueFormatting` | `format()` / `__format__` / `__bytes__` / `__bool__`.       |

➡️ [README_VALUE_DISPLAY](dunders/representation/README_VALUE_DISPLAY.md)  
➡️ [README_VALUE_FORMATTING](dunders/representation/README_VALUE_FORMATTING.md)  

[▲ Back to Contents](#-table-of-contents)

---

## Others

Mixins that add Simple-ecosystem-specific behavior rather than implementing a
standard Python protocol.

### Immutable

The "change without mutating" API for immutable instances.

| Mixin                 | Description                                                     |
|:----------------------|:----------------------------------------------------------------|
| `ImmutableMethods`    | `with_constant`, `with_composite`, `with_changes`, `duplicate`. |
| `ImmutableWithInners` | Generates a dedicated `with_<name>(value)` per inner.           |

➡️ [README_IMMUTABLE_METHODS](others/immutable/README_IMMUTABLE_METHODS.md)  
➡️ [README_IMMUTABLE_METHODS_WITHINNERS](others/immutable/README_IMMUTABLE_METHODS_WITHINNERS.md)  

[▲ Back to Contents](#-table-of-contents)

---

### Numerical

Safe, bounded numeric stepping via `Stepper` controllers.

| Mixin                 | Description                                           |
|:----------------------|:------------------------------------------------------|
| `Volume`              | One stepper for the instance's own main value.        |
| `Equalizer`           | One stepper per inner, exposed as dynamic properties. |

➡️ [README_VOLUME](others/numerical/README_VOLUME.md)   
➡️ [README_EQUALIZER](others/numerical/README_EQUALIZER.md)  

[▲ Back to Contents](#-table-of-contents)

---

### Properties

Ergonomic property-based access.

| Mixin            | Description                                               |
|:-----------------|:----------------------------------------------------------|
| `InnersProperty` | Direct attribute access to a composite's inners.          |
| `MetaShortcuts`  | Shortcut properties over frequently used metadata fields. |

➡️ [README_INNERS_PROPERTY](others/properties/README_INNERS_PROPERTY.md)  
➡️ [README_META_SHORTCUTS](others/properties/README_META_SHORTCUTS.md)  

[▲ Back to Contents](#-table-of-contents)

---

### State

State management for mutable instances.

| Mixin           | Description                                                     |
|:----------------|:----------------------------------------------------------------|
| `DefaultState`  | Remembers construction-time state; reset / clone / new-default. |
| `DirtyTracking` | `is_dirty`, `dirty_paths`, `mark_clean()`, `reset_to_clean()`.  |
| `History`       | Full undo/redo history — record, navigate, diff, export/import. |
| `Permission`    | Runtime `lock()` / `unlock()` read-only toggle.                 |

➡️ [README_DEFAULT_STATE](others/state/README_DEFAULT_STATE.md)  
➡️ [README_DIRTY_TRACKING](others/state/README_DIRTY_TRACKING.md)  
➡️ [README_HISTORY](others/state/README_HISTORY.md)  
➡️ [README_PERMISSION](others/state/README_PERMISSION.md)  

[▲ Back to Contents](#-table-of-contents)

---


