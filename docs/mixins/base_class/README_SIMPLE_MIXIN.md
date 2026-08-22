# 🧱 `SimpleMixin` — Structural Foundation for All Mixins

`SimpleMixin` is the base class every mixin in the Simple system must inherit from. It
does not add behavior on its own — instead it provides the structural contract that
makes mixins safe to combine: declarative compatibility flags, a slot-based memory
layout requirement, participation in a shared initialization chain, and automatic
structural validation whenever a new mixin subclass is defined.

```python
from simplibs.sentinels import UNSET

class SimpleMixin:
    ...
```

Any custom mixin a user writes must inherit from `SimpleMixin`, directly or indirectly
— this is what the validator (`verify_mixin_definition`) checks for, and a mixin that
doesn't satisfy this contract will fail validation and cannot be attached to a Simple
instance class.

---

## 🧭 Table of Contents

* [Compatibility Flags](#compatibility-flags)
* [`init_mixins`](#init_mixins)
* [`__init_subclass__`](#__init_subclass__)

---

### Compatibility Flags

Class-level declarative attributes that restrict which instance types a mixin may be
applied to. They carry no logic themselves — the instance-building pipeline reads them
to decide whether a given mixin is allowed on a given class.

**Attributes:**
* `_constant_only` (*bool*, default `False`): restricts the mixin to atomic instances.
* `_composite_only` (*bool*, default `False`): restricts the mixin to composite instances.
* `_mutable_only` (*bool*, default `False`): restricts the mixin to mutable instances.
* `_immutable_only` (*bool*, default `False`): restricts the mixin to immutable instances.
* `_only_types` (*ValidTypes*, default `UNSET`): restricts the mixin to instances whose
  value type matches (e.g. `Number`, `Integral`).

**Example usage:**
```python
class Bitwise(SimpleMixin):
    _constant_only = True
    _only_types = Integral
    ...
```

**Under the hood:**
```python
class SimpleMixin:
    _constant_only = False
    _composite_only = False
    _mutable_only = False
    _immutable_only = False
    _only_types = UNSET
```

[▲ Back to top](#-table-of-contents)

---

### `init_mixins`

The default initialization hook every mixin participates in. Mixins that override it
must call `super().init_mixins()` first, so every mixin in the MRO gets a chance to run
its own setup before the instance is considered ready.

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `None`

**Example usage:**
```python
class MyMixin(SimpleMixin):
    def init_mixins(self) -> None:
        super().init_mixins()
        self._my_field = compute_something()
```

**Under the hood:**
```python
def init_mixins(self) -> None:
    super().init_mixins()
```

[▲ Back to top](#-table-of-contents)

---

### `__init_subclass__`

Runs automatically whenever a new mixin subclass is created (i.e. at class-definition
time, not instance-creation time). Validates the mixin's structural correctness before
it can ever be used.

**Parameters:**
* `**kwargs`: forwarded to `super().__init_subclass__()`.

**Returns:**
* `None`

**Example usage:**
```python
# Triggered implicitly just by defining a mixin:
class MyMixin(SimpleMixin):
    __slots__ = ("_my_field",)
    # __init_subclass__ runs here, validating the definition
```

**Under the hood:**
```python
def __init_subclass__(cls, **kwargs) -> None:
    super().__init_subclass__(**kwargs)
    verify_mixin_definition(cls)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../README_MIXINS_OVERVIEW.md)
