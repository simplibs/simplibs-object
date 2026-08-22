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

---

## Base Class

| Mixin | Description |
| :---- | :---------- |
| [`SimpleMixin`](base_class/README_SIMPLE_MIXIN.md) | The structural foundation every mixin must inherit from — compatibility flags, `init_mixins` chain, automatic validation. |

---

## Core Mixins

Shared infrastructure used throughout the ecosystem — not a "feature" category on its
own, but the foundation both `dunders` and `others` build on.

| Mixin | Description |
| :---- | :---------- |
| [`NodesTuple`](core_mixins/README_NODES_TUPLE.md) | Builds `_nodes_tuple`, the flat ordered source of every node in the instance. |
| [`NodesDicts`](core_mixins/README_NODES_DICTS.md) | Turns `_nodes_tuple` into fast, name-keyed lookup dicts. |
| [`Snapshot`](core_mixins/README_SNAPSHOT.md) | Build, restore, and compare full-state value snapshots. |
| [`Infrastructure`](core_mixins/README_INFRASTRUCTURE.md) | Bundles `NodesDicts` + `Snapshot` into one shared base. |
| [`Serialization`](core_mixins/README_SERIALIZATION.md) | Full `to_dict` / `to_json` / `from_dict` / `from_json` API. |

---

## Dunders

Mixins implementing standard Python "dunder" (double-underscore) protocols — the
hooks Python itself looks for to make an object iterable, comparable, callable,
picklable, printable, and so on.

### Collections

Dict-like and iterable behavior over a composite's direct inners.

| Mixin | Description |
| :---- | :---------- |
| [`CollectionBase`](dunders/collections/README_COLLECTION_BASE.md) | Base mapping foundation — `keys()`, `values()`, `items()`. |
| [`Iterable`](dunders/collections/README_ITERABLE.md) | `__iter__`, `__reversed__`, `__dir__` over inner keys. |
| [`Mapping`](dunders/collections/README_MAPPING.md) | `__getitem__`, `__setitem__`, `__contains__`, `__len__`, `get()`. |
| [`Collection`](dunders/collections/main/README_COLLECTION.md) | Combines `Iterable` + `Mapping` into full dict-like API. |

### Comparison

Value-based equality, hashing, and magnitude ordering.

| Mixin | Description |
| :---- | :---------- |
| [`Equality`](dunders/comparison/README_EQUALITY.md) | `__eq__` and `__hash__`, mutability-aware hashing strategy. |
| [`Ordering`](dunders/comparison/README_ORDERING.md) | `__lt__`, `__le__`, `__gt__`, `__ge__` via `self.value`. |

### Generics

Generic-style subscript syntax for typing/IDE purposes.

| Mixin | Description |
| :---- | :---------- |
| [`ClassGetItem`](dunders/generics/README_CLASS_GETITEM.md) | `__class_getitem__` fallback for subscriptable classes (`MyClass[int]`). |

### Interfaces

General-purpose Python object protocols.

| Mixin | Description |
| :---- | :---------- |
| [`Call`](dunders/interfaces/README_CALL.md) | `__call__` — syntactic sugar over the `with_any` change API. |
| [`ContextManager`](dunders/interfaces/README_CONTEXT.md) | `__enter__` / `__exit__` — inert, no-op context support. |

### Lifecycles

Object lifecycle protocols built on a shared snapshot foundation.

| Mixin | Description |
| :---- | :---------- |
| [`Copyable`](dunders/lifecycles/README_COPYABLE.md) | `__copy__` / `__deepcopy__` via snapshot. |
| [`PickleState`](dunders/lifecycles/README_PICKLE_STATE.md) | `__getstate__` / `__setstate__` via `to_dict()` / `from_dict()`. |
| [`PicleReduce`](dunders/lifecycles/README_PICKLE_REDUCE.md) | `__reduce__` — top-level pickle protocol hook. |
| [`Lifecycle`](dunders/lifecycles/main/README_LIFECYCLE.md) | Combines `Copyable` + `PicleReduce` for full copy/pickle support. |

### Numeric

The full range of Python numeric protocols.

| Mixin | Description |
| :---- | :---------- |
| [`Arithmetic`](dunders/numeric/README_ARITHMETIC.md) | `+ - * / // % **` and reflected forms, returns new instances. |
| [`Unary`](dunders/numeric/README_UNARY.md) | `-x`, `+x`, `abs(x)`, returns new instances. |
| [`Bitwise`](dunders/numeric/README_BITWISE.md) | `& \| ^ << >> ~` for integral atoms only. |
| [`Inplace`](dunders/numeric/README_INPLACE.md) | `+= -= *= /= //= %= **=`, mutates in place. |
| [`Conversion`](dunders/numeric/README_CONVERSION.md) | `int()`, `float()`, `complex()`, `round()`, floor/ceil/trunc. |

### Representation

How an instance presents itself as text, bytes, and boolean.

| Mixin | Description |
| :---- | :---------- |
| [`ValueDisplay`](dunders/representation/README_VALUE_DISPLAY.md) | `__repr__` / `__str__` — value-like display, constant-only. |
| [`ValueFormatting`](dunders/representation/README_VALUE_FORMATTING.md) | `format()` / `__format__` / `__bytes__` / `__bool__`. |

---

## Others

Mixins that add Simple-ecosystem-specific behavior rather than implementing a
standard Python protocol.

### Immutable

The "change without mutating" API for immutable instances.

| Mixin | Description |
| :---- | :---------- |
| [`ImmutableMethods`](others/immutable/README_IMMUTABLE_METHODS.md) | `with_constant`, `with_composite`, `with_changes`, `duplicate`. |
| [`ImmutableWithInners`](others/immutable/README_IMMUTABLE_METHODS_WITHINNERS.md) | Generates a dedicated `with_<name>(value)` per inner. |

### Numerical

Safe, bounded numeric stepping via `Stepper` controllers.

| Mixin | Description |
| :---- | :---------- |
| [`Volume`](others/numerical/README_VOLUME.md) | One stepper for the instance's own main value. |
| [`Equalizer`](others/numerical/README_EQUALIZER.md) | One stepper per inner, exposed as dynamic properties. |

### Properties

Ergonomic property-based access.

| Mixin | Description |
| :---- | :---------- |
| [`InnersProperty`](others/properties/README_INNERS_PROPERTY.md) | Direct attribute access to a composite's inners. |
| [`MetaShortcuts`](others/properties/README_META_SHORTCUTS.md) | Shortcut properties over frequently used metadata fields. |

### State

State management for mutable instances.

| Mixin | Description |
| :---- | :---------- |
| [`DefaultState`](others/state/README_DEFAULT_STATE.md) | Remembers construction-time state; reset / clone / new-default. |
| [`DirtyTracking`](others/state/README_DIRTY_TRACKING.md) | `is_dirty`, `dirty_paths`, `mark_clean()`, `reset_to_clean()`. |
| [`History`](others/state/README_HISTORY.md) | Full undo/redo history — record, navigate, diff, export/import. |
| [`Permission`](others/state/README_PERMISSION.md) | Runtime `lock()` / `unlock()` read-only toggle. |

---

[⬅️ Back to main README](../README.md)
