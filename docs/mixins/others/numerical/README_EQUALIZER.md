# 🧱 `Equalizer` — Per-Inner Steppers

`Equalizer` gives every inner of a composite its own `Stepper`, exposed as a dynamic
property named `<inner_name>_stepper` — one fader per channel.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from src.simplibs.object.mixins.core_mixins import NodesTuple

class Equalizer(NodesTuple, SimpleMixin):
    ...
```

`_composite_only = True`, `_mutable_only = True`, `_only_types = Number`.

---

## 🧭 Table of Contents

* [`__extend_instance_class__`](#__extend_instance_class__)
* [`init_mixins`](#init_mixins)

[⬅️ Back to main Mixins Overview](../../README_MIXINS_OVERVIEW.md)

---

### `__extend_instance_class__`

Class-creation-time hook. For every node name, dynamically defines and attaches a
read-only property `<name>_stepper` that reads from the instance's `_steppers` dict.

**Parameters:**
* `instance_cls` (*SimpleInstanceLike*): the instance class being built.

**Returns:**
* `SimpleInstanceLike`: the modified class.

**Example usage:**
```python
class Mixer(Equalizer, SimpleObject):
    volume: int
    treble: int

mixer.volume_stepper.up(5)
```

**Under the hood:**
```python
@staticmethod
def __extend_instance_class__(instance_cls):
    for name in instance_cls.meta.node_names_set:

        def getter(self, _name=name):
            return self._steppers[_name]

        prop_name = f"{name}{"_stepper"}"
        setattr(instance_cls, prop_name, property(getter))

    return instance_cls
```

[▲ Back to top](#-table-of-contents)

---

### `init_mixins`

Builds one `Stepper` per node, stored in `_steppers`, keyed by name.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Example usage:**
```python
mixer = Mixer(volume=50, treble=10)
```

**Under the hood:**
```python
def init_mixins(self):
    self._steppers = {
        instance.meta.name_snake: Stepper(instance)
        for instance, _ in self._nodes_tuple
    }
```

A closer look at the Stepper class:  
➡️ [README_STEPPER](stepper_class/README_STEPPER.md)    

[▲ Back to top](#-table-of-contents)

---

