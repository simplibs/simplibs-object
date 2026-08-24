# 🧱 `Bitwise` — Bitwise Operators for Atoms

`Bitwise` gives a SimpleObject atom the standard bitwise operators (`&`, `|`, `^`,
`<<`, `>>`, `~`), including reflected forms, so integer-valued constants behave like
plain `int` in bit-manipulation code.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from src.simplibs.object.mixins.core_mixins import NodesDicts, NodesTuple, Snapshot

class Bitwise(Snapshot, NodesDicts, NodesTuple, SimpleMixin):
    ...
```

`_constant_only = True`, `_only_types = Integral` — restricted to atoms holding
integral values.

---

## 🧭 Table of Contents

* [`__and__` / `__rand__`](#__and__--__rand__)
* [`__or__` / `__ror__`](#__or__--__ror__)
* [`__xor__` / `__rxor__`](#__xor__--__rxor__)
* [`__lshift__` / `__rlshift__`](#__lshift__--__rlshift__)
* [`__rshift__` / `__rrshift__`](#__rshift__--__rrshift__)
* [`__invert__`](#__invert__)

---

### `__and__` / `__rand__`

Returns a new instance with the value `self.value & other` (or reversed).

**Parameters:**
* `other` (*Any*)

**Returns:**
* a new instance.

**Example usage:**
```python
flags & 0b0011
```

**Under the hood:**
```python
def __and__(self, other):
    return execute_bitwise_op(self, operator.and_, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__or__` / `__ror__`

Same shape, using `operator.or_`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* a new instance holding `self.value | other` (or reversed).

**Example usage:**
```python
flags | 0b0100
```

**Under the hood:**
```python
def __or__(self, other):
    return execute_bitwise_op(self, operator.or_, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__xor__` / `__rxor__`

Same shape, using `operator.xor`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* a new instance holding `self.value ^ other` (or reversed).

**Example usage:**
```python
flags ^ 0b0001
```

**Under the hood:**
```python
def __xor__(self, other):
    return execute_bitwise_op(self, operator.xor, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__lshift__` / `__rlshift__`

Same shape, using `operator.lshift`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* a new instance holding `self.value << other` (or reversed).

**Example usage:**
```python
flags << 1
```

**Under the hood:**
```python
def __lshift__(self, other):
    return execute_bitwise_op(self, operator.lshift, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__rshift__` / `__rrshift__`

Same shape, using `operator.rshift`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* a new instance holding `self.value >> other` (or reversed).

**Example usage:**
```python
flags >> 1
```

**Under the hood:**
```python
def __rshift__(self, other):
    return execute_bitwise_op(self, operator.rshift, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__invert__`

Returns a new instance with the value `~self.value`. Unary — no reflected form.

**Parameters:**
* *(none)*

**Returns:**
* a new instance, or `NotImplemented` if the value doesn't support inversion.

**Example usage:**
```python
~flags
```

**Under the hood:**
```python
def __invert__(self):
    try:
        value = ~self.value
        return with_constant(self, self.meta.name_snake, value)
    except TypeError:
        return NotImplemented
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
