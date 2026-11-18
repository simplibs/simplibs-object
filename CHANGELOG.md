# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.2] - 2026-11-18

### 🐛 Fixed

* **`assert_immutable_behavior` could pass while proving nothing.** Any exception counted as
  "assignment rejected", so a `new_value` that the class would reject anyway (invalid) or that equals
  the current value made the check green. A new subtest `new_value_is_acceptable` first requires the
  value to be valid for the class and different from the current one, as `assert_value_change` does for
  the mutable case. **Behavior change** of the testing helper: a test passing such a value now fails.
* **`assert_reactivity_downward` compared with `zip`**, which stops at the shorter side: a
  `decompose_value` returning too few (or too many) values left the remaining inner components unchecked
  and the test green. The two lengths are compared first.
* **`verbose_value_change` cascade in `assert_simple_object`** used `or`, which turned detailed reporting
  back on after an earlier stage had already reported the value change. It now uses `and`, as the
  documentation always described: detailed only while no earlier stage reported it.
* **`assert_value_change`**: `InnerValue.as_instance_tuple` returns the bare `UNSET` (not a pair) when
  the path cannot be resolved; unpacking it failed with a confusing `TypeError`. The result is checked
  first, so a wrong path is reported as "could not be resolved".
* **`assert_user_instance_creation`** could end on an unbound name when the creation failed in verbose
  mode. It now returns `None` in that case, and `assert_simple_object` stops there instead of going on
  with `None`.
* **`assert_class_inheritance`**: passing something that is not a class raised `TypeError` from
  `issubclass`; it is now a failed check with a message.

### 🔄 Changed

* **Failure messages**: the plain `assert` statements of the testing package now say what was expected
  (pytest does not rewrite the asserts of an installed package, so they failed with an empty text).

### 📋 Improved

* **Tests**: new tests for the acceptable-value check and the non-class guard.
* **Documentation**: corrected design notes (`TestMixin` is not used by the method-level assertions;
  "directly or indirectly" for the inheritance contract).

---

## [0.1.1] - 2026-09-07

### 🐛 Fixed

* **Root Exception `skip_locations` Field**:
Renamed `_skip_locations` to `skip_locations` in `SimpleObjectError` to align with the constructor contract of `simplibs-exception`. This ensures internal library stack frames are correctly filtered out from tracebacks, pointing diagnostics directly to user code.

### 📋 Improved

* **IDE Autocompletion DX**:
Removed explicit `cls: "Simple...Protocol"` type annotations from user-facing declarative hook signatures (`_validate` on `SimpleConstant`; `_logic`, `_decompose`, and `_validate` on `SimpleObject`). This prevents IDEs like PyCharm from injecting protocol imports into subclasses when auto-generating method stubs.
* **Core Dependency Update**:
Upgraded `simplibs-exception` to `1.0.2` to resolve type checker warnings (`PyTypeChecker`) when using context-managed test helpers.

---

## [0.1.0] - 2026-08-24

### ✨ Added

#### Core

* `SimpleBase` — common architectural foundation for the `simplibs-object` hierarchy
* `SimpleConstant` — declarative definition of atomic, typed values with defaults, validation, and normalization
* `SimpleObject` — declarative composition of multiple inner objects into a derived value
* Support for `_type`, `_default`, `_inners`, `_logic`, `_decompose`, and `_validate` declarations
* Automatic default-value derivation for composite objects from their inner defaults and `_logic`

#### Declarative Object System

* Declarative class definitions serving as stable blueprints for runtime instances
* Automatic generation of the object interface from the class definition
* Standardized validation and normalization API
* Value creation and decomposition through `_logic` and `_decompose`
* Value update support for existing instances
* Write-once protection for processed class definitions

#### Metadata & Metaclass

* `SimpleMeta` — metaclass responsible for processing and validating `SimpleBase`, `SimpleConstant`, and `SimpleObject` definitions
* `SimpleBaseMetadata` — metadata layer for common class information
* `SimpleConstantMetadata` — metadata processing for atomic definitions
* `SimpleObjectMetadata` — metadata processing for composite definitions
* Method processing and signature verification for `_validate`, `_logic`, and `_decompose`
* Definition-time validation of types, defaults, inners, methods, and their relationships
* Early detection of invalid class definitions during class creation

#### Runtime Instances

* Dynamic creation of specialized atomic and composite runtime classes
* `make_atom_class` — runtime class creation for atomic objects
* `make_composite_class` — runtime class creation for composite objects
* `create_instance` — centralized runtime instance construction
* Support for mutable and immutable instance variants
* `__slots__`-based lightweight instance storage
* Runtime properties for accessing inner objects
* Instance protocols for common runtime behavior
* Value-property infrastructure for controlled value access and updates

#### Reactive Composition

* Automatic recalculation of composite values when inner values change
* Upward propagation of changes from inner objects toward the composition root
* Downward propagation through `_decompose` when a composite value is changed
* Recursive propagation through nested composite structures
* Owner relationships between inner objects and their containing objects
* Deterministic dependency flow based directly on the declared composition

#### Immutability

* Immutable instance support through `mutable=False`
* Immutable instances without value setters
* Immutable update methods returning new, consistent instances
* `ImmutableMethods` mixin for immutable value updates
* `ImmutableWithInners` mixin for convenient immutable updates of inner objects

#### Mixins

* `SimpleMixin` — base contract for reusable instance capabilities
* Dynamic mixin injection without requiring traditional multiple inheritance
* Core mixins for shared instance infrastructure
* Collection mixins for iterable, mapping, and collection behavior
* Comparison mixins for equality, ordering, and hashing
* Generic and interface mixins
* Lifecycle, copying, and pickle support
* Numeric and operator mixins
* Representation and formatting mixins
* Immutable update mixins
* State management mixins including defaults, dirty tracking, history, and permissions
* Property and metadata convenience mixins
* Support for creating custom mixins independently of domain-specific object definitions

#### Built-in Mixins

* `NodesTuple`
* `NodesDicts`
* `Snapshot`
* `Infrastructure`
* `Serialization`
* `CollectionBase`
* `Iterable`
* `Mapping`
* `Collection`
* `Equality`
* `Ordering`
* `ClassGetItem`
* `Call`
* `ContextManager`
* `Copyable`
* `PickleState`
* `PicleReduce`
* `Lifecycle`
* `Arithmetic`
* `Unary`
* `Bitwise`
* `Inplace`
* `Conversion`
* `ValueDisplay`
* `ValueFormatting`
* `ImmutableMethods`
* `ImmutableWithInners`
* `Volume`
* `Equalizer`
* `InnersProperty`
* `MetaShortcuts`
* `DefaultState`
* `DirtyTracking`
* `History`
* `Permission`

#### Tools

* `automate_creators` — programmatic creation of constant and object blueprints
* `bulk` — bulk creation of blueprints and instances from structured input
* `randomize` — integration with [`simplibs-randomize`](https://github.com/simplibs/simplibs-randomize) for generating valid random values
* `testing` — reusable assertions and test helpers for `SimpleObject` and `SimpleMixin` definitions
* Support for testing complete object structures and mixin configurations

#### Exceptions

* `SimpleObjectError` — common base exception for all library errors
* `SimpleDefinitionError` — errors in class and blueprint definitions
* `SimpleInitializationError` — errors during instance creation
* `SimpleRuntimeError` — errors occurring during runtime value manipulation
* Integration with [`simplibs-exception`](https://github.com/simplibs/simplibs-exception) for structured exception output
* Internal traceback filtering so diagnostics focus on the relevant user code
* Support for catching all library errors through `SimpleObjectError` or individual error categories

#### Settings

* Configurable library logging without automatic root logger configuration
* Optional value-change callback through the logging settings module
* Explicit opt-in behavior for logging configuration

#### Documentation

* Complete documentation for core classes
* Dedicated documentation for metadata processing
* Documentation for runtime instance creation
* Documentation for instance protocols and value properties
* Complete mixin overview and individual mixin documentation
* Documentation for `automate_creators`, `bulk`, and `randomize`
* Dedicated testing documentation
* Quick-start examples for basic objects, validation, mutability, composition, and mixins
* Main project README introducing the architecture and intended usage

#### Quality Assurance

* Test suite covering core object definitions and runtime behavior
* Tests for metadata processing and class validation
* Tests for atomic and composite instance creation
* Tests for mutable and immutable behavior
* Tests for reactive value propagation
* Tests for mixin compatibility and behavior
* Tests for exception handling and error propagation
* Testing utilities for validating user-defined objects and mixins

#### Dependencies

* `simplibs-exception` — structured exception framework underlying `SimpleObjectError`
* `simplibs-randomize` — optional random value generation and test-data support

---

## Legend

* 🔄 **Changed** — modifications to existing functionality
* ✨ **Added** — new features and components
* 🐛 **Fixed** — bug fixes
* 📋 **Improved** — enhancements to existing features
* ⚠️ **Deprecated** — deprecated functionality
* 🗑️ **Removed** — removed functionality
