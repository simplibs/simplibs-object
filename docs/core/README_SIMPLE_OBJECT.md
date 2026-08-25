# 🧩 `SimpleObject` — Declarative composition

`SimpleObject` extends `SimpleConstant` with the ability to compose a value
from inner elements (`_inners`). It's the flagship class of the whole system —
it lets you model structured data declaratively, in a type-safe and
deterministic way, where the resulting value is always computed from the
elements the composition is built from.

```
SimpleBase
└── SimpleConstant
    └── SimpleObject   ← you are here (inherits EVERYTHING from SimpleConstant)
```

Because `SimpleObject` inherits from `SimpleConstant`, every composition
automatically has everything from
[README_SIMPLE_CONSTANT](README_SIMPLE_CONSTANT.md) too — `validate`,
`normalize`, `is_valid`, and so on. This document only covers what
`SimpleObject` adds on top of that.

---

## 🧭 Contents

* [Declarative interface](#declarative-interface)
  * [`_inners`](#_inners)
  * [`_logic`](#_logic)
  * [`_decompose`](#_decompose)
  * [`_validate`](#_validate)
* [Important: _default must not be defined](#important-_default-must-not-be-defined)
* [Public API](#public-api)
  * [`calculate_value`](#calculate_value)
  * [`decompose_value`](#decompose_value)
* [Architectural role](#architectural-role)

[⬅️ Back to main README](../../README.md)

---

## Declarative interface

```python
class FullName(SimpleObject):
    _type = str
    _inners = (FirstName, LastName)

    @classmethod
    def _logic(cls, first_name, last_name):
        return f"{first_name} {last_name}"

    @classmethod
    def _decompose(cls, value):
        first, _, last = value.partition(" ")
        return (first, last)
```

### `_type`

A type annotation for the composition's **result**. The output of `_logic`
has to pass the same full validation as an atom's value does (see the
[validation pipeline](README_SIMPLE_CONSTANT.md#the-validation-pipeline-as-a-whole)).

### `_inners`

A required tuple of inner elements — each one is either a `SimpleConstant` or
another `SimpleObject` (so compositions can be nested to any depth). The
structure of `_inners` determines:

* what parameters `_logic` expects,
* the composition's default value (computed from the inner elements'
  defaults),
* whether the composition supports decomposing back,
* the metadata layout of the whole composition.

### `_logic`

A required computation hook — it defines how the composition's resulting
value is computed from its inner elements. It receives parameters matching
`_inners` (by name, not just by position), and must return a value that
passes full validation.

**The whole composition's default value** is computed automatically by
calling `_logic` with all inner elements' defaults — which is why a
composition never defines `_default` itself (see
[below](#important-_default-must-not-be-defined)).

### `_decompose`

An optional hook for the reverse direction — it converts a finished
composition value back into values for the individual inner elements. This
enables bidirectional models: upward (inner elements → composition) and
downward (composition → inner elements). If the user doesn't define it, the
composition is treated as non-decomposable.

### `_validate`

The same hook as on `SimpleConstant` — optional extended validation beyond
the type check, with the same three options (return a bool, raise an
exception, or use `bool_or_raise_validate_error`).

[▲ Back to Contents](#-contents)

---

## Important: `_default` must not be defined

Unlike `SimpleConstant`, a composition **never** defines `_default` itself —
the metadata actively enforces this and raises a structured error if you try
(`raise_default_is_defined_in_composition`, see `SimpleObjectMetadata`). The
default value is always derived automatically:

```
composition's _default = _logic(defaults of all _inners)
```

This rule is deliberate and important: it guarantees that a composition's
default is always **consistent** with its own computation rule — it can never
happen that someone manually sets a default that doesn't match what `_logic`
would actually compute.

[▲ Back to Contents](#-contents)

---

## Public API

Just like with `SimpleConstant`, these methods are thin wrappers over
internal logic in `_core/logic/object_methods/`.

### `calculate_value`

Computes the composition's value by calling the user's `_logic`, with full
parameter processing and validation happening before `_logic` even runs.

**Parameters:**
* `*args`, `**kwargs`: values mapped to inner elements (by order in
  `_inners`, or by name).

**Return value:**
* `Any`: the computed composition value.

**Exceptions:**
* `SimpleRuntimeError`, if parameter processing or validation fails.

**Nice detail for IDEs:** the signature uses `ParamSpec`
(`LogicSignature[P, R]`), which means PyCharm (and other IDEs) offer
**autocomplete for exactly the parameters your `_logic` expects** — even
though `calculate_value` itself doesn't declare any specific parameters.

**Under the hood — parameter processing (`_process_calculate_value_params`):**
```python
def _process_calculate_value_params(cls, *args, **kwargs):
    inners_map = cls.meta.inners_map

    if len(args) > len(inners_map):
        raise_too_many_positional_args_error(...)

    clean_kwargs = {}
    args_iter = iter(args)

    for param_name, inner_cls in inners_map.items():
        try:
            value = next(args_iter)
            if param_name in kwargs:
                raise_duplicate_argument_error(cls, param_name)
        except StopIteration:
            value = kwargs.pop(param_name, None)

        if value is None:
            value = inner_cls.meta.default
        else:
            inner_cls.validate(value)

        clean_kwargs[param_name] = value

    if kwargs:
        raise_unknown_parameter_error(cls, list(kwargs.keys()))

    return clean_kwargs
```

This function does four things at once, each guarded with a structured
error:

1. **Checks the number of positional arguments** — there can't be more of
   them than there are inner elements.
2. **Detects duplicates** — if a parameter is given both positionally *and*
   as a keyword argument, that's an error (not a silent overwrite).
3. **Falls back to the default** — a missing parameter is filled in from
   `inner_cls.meta.default`, not from some generic `None` value.
4. **Detects unknown keyword arguments** — anything left over in `kwargs`
   after processing all known `_inners` is an error.

`calculate_value` itself then simply calls `cls.meta.logic(**params_dict)` —
all the complexity of parameter processing is deliberately kept in its own
function, so it stays clear what does what.

[▲ Back to Contents](#-contents)

---

### `decompose_value`

Decomposes a finished composition value back into the values of its inner
elements, using the user's `_decompose`.

**Parameters:**
* `value` (*Any*): the composition value to decompose.

**Return value:**
* `Any`: the decomposed representation (typically a tuple of values for
  `_inners`).

**Exceptions:**
* `SimpleRuntimeError`, if the composition isn't decomposable, or if `value`
  fails validation.

**Under the hood:**
```python
def decompose_value(cls, value):
    if not cls.meta.is_decomposeable:
        raise_class_not_decomposeable(cls.meta)

    cls.validate(value)
    outcome = cls.meta.decompose(value)
    return outcome
```

The order of steps here isn't accidental: first it checks that decomposition
even makes sense (`is_decomposeable`), only then does it validate the input
`value`, and only after that does the actual decomposition run. This order
avoids unnecessary work — there's no point validating a value for an
operation that's going to fail with "not decomposable" anyway.

[▲ Back to Contents](#-contents)

---

## Architectural role

`SimpleObject` is the flagship class of the whole Simple system:

* declarative modeling of composite structures,
* deterministic derivation of the default value from inner elements,
* metadata-driven computation (`calculate_value`) plus optional decomposition
  back (`decompose_value`),
* full inheritance of validation and normalization from `SimpleConstant`,
* a type-safe, readable, declarative API — the user only writes `_type`,
  `_inners`, `_logic` (and optionally `_decompose`/`_validate`); the rest
  (parameter parsing, validation, error messages) is handled by the system.

Actually creating running instances from a class defined this way (both atom
and composite variants, mutable and immutable) is covered in the next
document, about metadata and instance builders.

➡️ Next: [README_SIMPLE_META](../metadata/README_SIMPLE_META.md)

[▲ Back to Contents](#-contents)
