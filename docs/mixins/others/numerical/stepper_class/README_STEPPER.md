# 🧱 `Stepper` — Controlled Numeric Manipulation

`Stepper` is an internal service class that provides an encapsulated interface for safe numeric value manipulation. It handles incrementing, decrementing, and directly assigning values with automatic type normalization, validation, bound limits enforcement, and optional callbacks.

```python
from simplibs.object.mixins.others.numerical._stepper_class import Stepper

stepper = Stepper(instance)

```

`Stepper` is used internally by numerical mixins (such as `Volume` for single values and `Equalizer` for composite inner nodes) and is typically not instantiated directly by the user.

---

## 🧭 Table of Contents

* [`__init__`](#__init__)
* [`step`](#step)
* [`up_limit`](#up_limit)
* [`down_limit`](#down_limit)
* [`up_limit_action`](#up_limit_action)
* [`down_limit_action`](#down_limit_action)
* [`step_up``](#step_up)
* [`step_down`](#step_down)
* [`set_value`](#set_value)
* [`__repr__`](#__repr__)

[⬅️ Back to main Mixins Overview](../../../README_MIXINS_OVERVIEW.md)

---

### `__init__`

Initializes a new `Stepper` controller bound to a numeric instance, setting default values for step, limits, and limit callbacks.

**Parameters:**

* `instance` (*SimpleInstanceLike*): The target instance implementing `InstanceBase` with a numeric value.

**Returns:**

* `None`

**Under the hood:**

```python
def __init__(self, instance):

    # 1. Validate instance
    validate_instance(instance)

    # 2. Bind instance
    self._instance = instance

    # 3. Determine numeric type
    self._value_type = type(instance.value)

    # 4. Default step value
    self._step = self._value_type(1)

    # 5. Default limits and actions
    self._up_limit = UNSET
    self._down_limit = UNSET
    self._up_limit_action = UNSET
    self._down_limit_action = UNSET

```

[▲ Back to top](#-table-of-contents)

---

### `step`

Gets or sets the default step amount used for increment and decrement operations. Setting a new step automatically normalizes and validates the value against the bound instance.

**Parameters (setter):**

* `value` (*Any*): The step increment/decrement size.

**Returns:**

* `Any` (getter): The current step value.

**Example usage:**

```python
stepper.step = 5

```

**Under the hood:**

```python
@property
def step(self):
    return self._step

@step.setter
def step(self, value):
    self._step = process_value(self, value)

```

[▲ Back to top](#-table-of-contents)

---

### `up_limit`

Gets or sets the upper boundary for the numeric value. Verifies boundary consistency against `down_limit`.

**Parameters (setter):**

* `value` (*Any*): The upper limit value (or `UNSET`).

**Returns:**

* `Any`: The configured upper limit or `UNSET`.

**Example usage:**

```python
stepper.up_limit = 100

```

**Under the hood:**

```python
@property
def up_limit(self):
    return self._up_limit

@up_limit.setter
def up_limit(self, value):
    # Normalizes value and ensures up_limit >= down_limit
    self._up_limit = process_up_limit_value(self, value)

```

[▲ Back to top](#-table-of-contents)

---

### `down_limit`

Gets or sets the lower boundary for the numeric value. Verifies boundary consistency against `up_limit`.

**Parameters (setter):**

* `value` (*Any*): The lower limit value (or `UNSET`).

**Returns:**

* `Any`: The configured lower limit or `UNSET`.

**Example usage:**

```python
stepper.down_limit = 0

```

**Under the hood:**

```python
@property
def down_limit(self):
    return self._down_limit

@down_limit.setter
def down_limit(self, value):
    # Normalizes value and ensures down_limit <= up_limit
    self._down_limit = process_down_limit_value(self, value)

```

[▲ Back to top](#-table-of-contents)

---

### `up_limit_action`

Gets or sets a callable action executed whenever an operation attempts to exceed `up_limit`.

**Parameters (setter):**

* `value` (*Callable*): Callback without arguments.

**Returns:**

* `LimitAction`: The callable action or `UNSET`.

**Example usage:**

```python
stepper.up_limit_action = lambda: print("Max reached!")

```

**Under the hood:**

```python
@property
def up_limit_action(self):
    return self._up_limit_action

@up_limit_action.setter
def up_limit_action(self, value):
    if not callable(value):
        raise_stepper_invalid_action(self, value)
    self._up_limit_action = value

```

[▲ Back to top](#-table-of-contents)

---

### `down_limit_action`

Gets or sets a callable action executed whenever an operation attempts to fall below `down_limit`.

**Parameters (setter):**

* `value` (*Callable*): Callback without arguments.

**Returns:**

* `LimitAction`: The callable action or `UNSET`.

**Example usage:**

```python
stepper.down_limit_action = lambda: print("Min reached!")

```

**Under the hood:**

```python
@property
def down_limit_action(self):
    return self._down_limit_action

@down_limit_action.setter
def down_limit_action(self, value):
    if not callable(value):
        raise_stepper_invalid_action(self, value)
    self._down_limit_action = value

```

[▲ Back to top](#-table-of-contents)

---

### `step_up`

Increases the instance value by the configured `step` (or by an optionally provided custom amount). Enforces `up_limit` and triggers `up_limit_action` if limit is breached.

**Parameters:**

* `value` (*StepValue*, optional, default `UNSET`): Custom step increment. If `UNSET`, the default `step` is used.
* `validate` (*bool*, keyword-only, default `True`): Whether to run instance validation on the step amount.
* `raise_exception` (*bool*, keyword-only, default `False`): Whether to raise an exception if the upper limit is reached/exceeded.

**Returns:**

* `bool`: `True` if the increment succeeded, `False` if blocked by upper limit.

**Example usage:**

```python
stepper.step_up()
stepper.step_up(10, raise_exception=True)

```

**Under the hood:**

```python
def step_up(self, value=UNSET, *, validate=True, raise_exception=False):

    # 1. Normalize and validate the step value
    _value = process_step_value(self, value, validate=validate)

    # 2. Compute the new value
    new_value = self._instance._value + _value

    # 3. Check upper limit and trigger action/error if violated
    if not verify_up_limit(self, new_value, raise_exception=raise_exception):
        return False

    # 4. Write the new value
    self._instance._value = new_value
    return True

```

[▲ Back to top](#-table-of-contents)

---

### `step_down`

Decreases the instance value by the configured `step` (or by an optionally provided custom amount). Enforces `down_limit` and triggers `down_limit_action` if limit is breached.

**Parameters:**

* `value` (*StepValue*, optional, default `UNSET`): Custom step decrement. If `UNSET`, the default `step` is used.
* `validate` (*bool*, keyword-only, default `True`): Whether to run instance validation on the step amount.
* `raise_exception` (*bool*, keyword-only, default `False`): Whether to raise an exception if the lower limit is reached/exceeded.

**Returns:**

* `bool`: `True` if the decrement succeeded, `False` if blocked by lower limit.

**Example usage:**

```python
stepper.step_down()
stepper.step_down(5)

```

**Under the hood:**

```python
def step_down(self, value=UNSET, *, validate=True, raise_exception=False):

    # 1. Normalize and validate the step value
    _value = process_step_value(self, value, validate=validate)

    # 2. Compute the new value
    new_value = self._instance._value - _value

    # 3. Check lower limit and trigger action/error if violated
    if not verify_down_limit(self, new_value, raise_exception=raise_exception):
        return False

    # 4. Write the new value
    self._instance._value = new_value
    return True

```

[▲ Back to top](#-table-of-contents)

---

### `set_value`

Safely sets a specific value with full limit checking and validation based on the direction of change.

**Parameters:**

* `value` (*Any*): The target numeric value.
* `validate` (*bool*, keyword-only, default `True`): Whether to validate the new value via the bound instance.
* `raise_exception` (*bool*, keyword-only, default `False`): Whether to raise an exception if limits are exceeded.

**Returns:**

* `bool`: `True` if assigned successfully, `False` if blocked by limits.

**Example usage:**

```python
stepper.set_value(50)

```

**Under the hood:**

```python
def set_value(self, value, *, validate=True, raise_exception=False):

    # 1. Normalize and validate the value
    _value = process_value(self, value, validate=validate)

    # 2. Handle identical value (no-op)
    if _value == self._instance._value:
        return True

    # 3. Limit checks
    if _value > self._instance._value:
        if not verify_up_limit(self, _value, raise_exception=raise_exception):
            return False
    else:
        if not verify_down_limit(self, _value, raise_exception=raise_exception):
            return False

    # 4. Write the value
    self._instance._value = _value
    return True

```

[▲ Back to top](#-table-of-contents)

---

### `__repr__`

Returns an informative string representation of the `Stepper` instance with its current value and step.

**Parameters:**

* *(none)*

**Returns:**

* `str`

**Under the hood:**

```python
def __repr__(self):
    return f"<Stepper value={self._instance.value!r} step={self._step}>"

```

[▲ Back to top](#-table-of-contents)

---
