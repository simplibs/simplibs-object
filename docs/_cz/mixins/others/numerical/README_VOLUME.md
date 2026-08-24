# 🧱 `Volume` — Stepper for the Main Value

`Volume` attaches a `Stepper` — a numeric controller supporting safe stepping and
limit enforcement — directly to an instance's own value.

```python
from numbers import Number
from src.simplibs.object.mixins.base_class import SimpleMixin
from ._stepper_class import Stepper

class Volume(SimpleMixin):
    ...
```

`_mutable_only = True`, `_only_types = Number`.

---

## 🧭 Table of Contents

* [`init_mixins`](#init_mixins)
* [`value_stepper`](#value_stepper)

---

### `init_mixins`

Builds a `Stepper` bound to this instance.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Example usage:**
```python
volume = VolumeControl(default=50)
volume.value_stepper.up(10)
```

**Under the hood:**
```python
def init_mixins(self):
    super().init_mixins()
    self._value_stepper = Stepper(self)
```

[▲ Back to top](#-table-of-contents)

---

### `value_stepper`

Returns the numeric controller (stepper) for safely manipulating this instance's main
value.

**Parameters:**
* *(none — property getter)*

**Returns:**
* `StepperProtocol`

**Example usage:**
```python
volume.value_stepper.down(5)
```

**Under the hood:**
```python
@property
def value_stepper(self):
    return self._value_stepper
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
