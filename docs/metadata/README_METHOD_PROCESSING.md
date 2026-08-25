# ⚙️ Classmethod processing — `_validate`, `_logic`, `_decompose`

This document describes **one shared pipeline** that all three
user-definable classmethods in the system go through: `_validate` (on both
`SimpleConstant` and `SimpleObject`), and `_logic` and `_decompose` (both
only on `SimpleObject`). Instead of each method type having its own,
duplicated verification logic, both `SimpleConstantMetadata` and
`SimpleObjectMetadata` call the same entry-point function —
`process_classmethod` — just with different parameters.

➡️ Used from: [README_SIMPLE_CONSTANT_METADATA](README_SIMPLE_CONSTANT_METADATA.md),
[README_SIMPLE_OBJECT_METADATA](README_SIMPLE_OBJECT_METADATA.md)

---

## 🧭 Contents

* [Pipeline overview](#pipeline-overview)
* [`process_classmethod` — the entry point](#process_classmethod--the-entry-point)
* [`verify_classmethod` — the gate: validate, clone, or inherit?](#verify_classmethod--the-gate-validate-clone-or-inherit)
* [`_clone_classmethod` — isolating inherited methods](#_clone_classmethod--isolating-inherited-methods)
* [`verify_params` — signature check at the bytecode level](#verify_params--signature-check-at-the-bytecode-level)
* [`verify_annotations_and_defaults` — checking optional annotations](#verify_annotations_and_defaults--checking-optional-annotations)
* [`verify_calculation` — dry run and result check](#verify_calculation--dry-run-and-result-check)
* [`verify_decompose_outcome` — special rules for `_decompose`](#verify_decompose_outcome--special-rules-for-_decompose)

[⬅️ Back to main README](../../README.md)

---

## Pipeline overview

```
process_classmethod
│
├─ 1. verify_classmethod  ──────► decides: validate? clone? skip?
│
├─ 2. (if need_validations)
│     ├─ verify_params
│     └─ verify_annotations_and_defaults  (only if the user declared something)
│
├─ 3. injects normalized defaults/annotations into __func__
│
└─ 4. verify_calculation ──────► dry run + result type check
      └─ (only for _decompose) verify_decompose_outcome
```

The whole pipeline runs **once, at class-definition time** — not on every
call to the method at runtime. The result is either a validated, completed
classmethod (and, for `_logic`, an already-computed default value as well),
or `UNSET`, if the method wasn't defined and is optional.

[▲ Back to Contents](#-contents)

---

## `process_classmethod` — the entry point

**Parameters:**
* `method_name` (*str*): `"_validate"`, `"_logic"`, or `"_decompose"`.
* `expected_params`, `expected_args_params_count`: the expected signature.
* `expected_args_defaults`, `expected_kwargs_defaults`: the expected
  defaults.
* `expected_param_types`, `expected_return_type`: the expected annotations.
* `owner_class`: the class the method is being processed for.
* `test_value` (*tuple*, default `()`): arguments for the dry run.
* `return_calculated_value` (*bool*, default `False`): if `True`, returns a
  `(method, computed_value)` pair instead of just the method — used for
  `_logic`, where the dry run's result also serves as the composition's
  default value.

**Return value:**
* `ClassMethodProtocol` (the validated method), or `(method, value)` if
  `return_calculated_value=True`, or `UNSET`/`(UNSET, UNSET)` if the method
  is optional and missing.

**Under the hood (abridged):**
```python
def process_classmethod(method_name, expected_params, ..., owner_class,
                         test_value=(), return_calculated_value=False):
    need_validations, bound_method = verify_classmethod(...)

    if bound_method is UNSET:
        return (UNSET, UNSET) if return_calculated_value else UNSET

    if need_validations:
        verify_params(...)
        bound_method_annotations = {**expected_param_types, "return": expected_return_type}
        if func.__annotations__ or func.__defaults__ or func.__kwdefaults__:
            verify_annotations_and_defaults(...)
        func.__defaults__ = expected_args_defaults
        func.__kwdefaults__ = expected_kwargs_defaults
        func.__annotations__ = bound_method_annotations

    calculated_value = verify_calculation(bound_method, test_value, expected_return_type, owner_class)

    return (bound_method, calculated_value) if return_calculated_value else bound_method
```

A key detail: **annotations and defaults are force-injected into the
function** (`func.__defaults__ = ...`), even if the user never wrote them at
all. This means the method always looks the same from the outside once
processed — with a complete, consistent signature — no matter how tersely
the user wrote it.

[▲ Back to Contents](#-contents)

---

## `verify_classmethod` — the gate: validate, clone, or inherit?

This is the central decision point of the whole pipeline — it determines
whether a method needs to be re-validated at all, or whether it can (safely)
remain as inherited from the parent.

**Parameters:** `method_name`, `owner_class`, `expected_params`,
`expected_args_params_count`

**Return value:**
* `tuple[bool, classmethod | UNSET]` — `(need_validations, bound_method)`.

**Decision tree (simplified):**

1. **Special shortcut for an undefined `_decompose`.** If the `_decompose`
   method isn't locally overridden (`raw_method is UNSET`) and the inherited
   version points exactly at `SimpleObject._decompose` (an identity check
   via `is` on `__func__` — comparing memory address, not content) →
   `(False, UNSET)` is returned right away. This avoids needlessly running a
   dry run for a method that's still just the default "not decomposable"
   implementation.
2. **Local override (`raw_method is not UNSET`)** → always `(True,
   bound_method)`. Anything the user wrote directly on this class has to be
   verified from scratch.
3. **Inherited `_validate`** → always `(False, bound_method)`. Validation
   rules belong to the class that defined them — an inherited `_validate` is
   never re-verified.
4. **Deep nesting (the class isn't a direct child of `SimpleObject`)** — if
   the subclass changes structural keys (`_inners`, `_type`, `_logic`), the
   inherited method gets **cloned** via `_clone_classmethod`, so that
   injecting new metadata (step 3 in `process_classmethod`) doesn't affect
   the original function object shared with the parent class.
5. **None of the above apply** → the method is structurally broken (not a
   `classmethod`, not defined, etc.) → a set of micro-validators runs
   (`validate_method_is_defined`, `validate_method_is_callable`,
   `validate_method_is_classmethod`), producing a precise error message.

**Why step 4 matters:** in Python, `classmethod` wraps a single shared
function object. If new defaults/annotations were injected directly into an
inherited method (without cloning), that would propagate back into the
parent class as well — a silent, hard-to-spot shared-state bug. Cloning
prevents this by giving deeply nested subclasses their own, independent
copy.

[▲ Back to Contents](#-contents)

---

## `_clone_classmethod` — isolating inherited methods

**Parameters:** `cm` (*classmethod*) — the method to clone.

**Return value:** a new, fully independent `classmethod` object.

**Under the hood:**
```python
def _clone_classmethod(cm):
    func = cm.__func__
    new_func = FunctionType(
        func.__code__, func.__globals__, name=func.__name__,
        argdefs=func.__defaults__, closure=func.__closure__,
    )
    new_func.__annotations__ = dict(func.__annotations__)
    new_func.__kwdefaults__ = dict(func.__kwdefaults__) if func.__kwdefaults__ else None
    if func.__dict__:
        new_func.__dict__.update(func.__dict__)
    return classmethod(new_func)
```

It rebuilds a completely new `FunctionType` from the same bytecode
(`__code__`), the same globals and closure, but with **its own** copies of
the annotations, defaults, and attributes. This new function object is now
safe to mutate (via `func.__defaults__ = ...` in `process_classmethod`)
without affecting the original.

[▲ Back to Contents](#-contents)

---

## `verify_params` — signature check at the bytecode level

**Parameters:** `expected_params`, `expected_args_params_count`,
`bound_method`

**Return value:** `None` (raises an exception on a mismatch).

**Why bytecode, not `inspect`:** the function reads the signature directly
from `__code__` (`co_argcount`, `co_kwonlyargcount`, `co_varnames`,
`co_flags`) instead of going through the `inspect` module. This is faster,
and fully sufficient for this purpose — all that's needed is the parameter
names, their count, and whether `*args`/`**kwargs` are present.

**Happy path (short-circuit):** if the method has neither `*args` nor
`**kwargs`, the positional parameter count matches, and the parameter names
match exactly (`method_params == expected_params`), the function returns
immediately — no further processing. Only when something doesn't match does
it build `exception_info` and `expected_structure` (a readable "blueprint"
of the correct signature) and run three micro-validators that pin down
exactly what's wrong: incorrect parameter names/order, an incorrect
argument count, or the use of `*args`/`**kwargs` (which are forbidden for
`_validate`/`_logic`/`_decompose` — the signature must be fully explicit).

[▲ Back to Contents](#-contents)

---

## `verify_annotations_and_defaults` — checking optional annotations

This only runs when the user **themselves** declared something (type
annotations or default values) — otherwise it's skipped, since
`process_classmethod` injects everything automatically at the end anyway.

**Parameters:** `bound_method`, `expected_params`,
`expected_args_params_count`, `bound_method_annotations`,
`expected_args_defaults`, `expected_kwargs_defaults`

**Return value:** `None` (raises an exception on a mismatch).

**Rule:** *annotations and defaults may be missing, but if they're present,
they must exactly match what the system expects.* That means three
independent checks, each run only if the relevant part is present:

* `func.__annotations__` → `validate_annotations` (annotations must be a
  subset of the expected types),
* `func.__defaults__` → `validate_args_defaults` (positional defaults must
  match the defaults derived from `_inners`),
* `func.__kwdefaults__` → `validate_kwargs_defaults`.

This approach gives the user freedom — they can (but don't have to) write
type annotations for their own readability/IDE support — but if they get
them wrong, the system catches it immediately at class-definition time,
not later at runtime.

[▲ Back to Contents](#-contents)

---

## `verify_calculation` — dry run and result check

The final and most important step: the method is **actually run** (with
test values) already at class-definition time, not just on first use.

**Parameters:** `bound_method`, `test_value`, `expected_return_type`,
`owner_class`

**Return value:** `Any` — the dry run's result (or `UNSET`, if
`bound_method` is `UNSET`).

**Under the hood:**
```python
def verify_calculation(bound_method, test_value, expected_return_type, owner_class):
    if bound_method is UNSET:
        return UNSET

    try:
        calculate_result = bound_method(*test_value)
    except Exception as e:
        raise_method_raised_exceptions(e, bound_method)

    if not isinstance(calculate_result, expected_return_type):
        raise_method_return_unvalide_outcome_type(calculate_result, expected_return_type, bound_method)

    if bound_method.__func__.__name__ == "_decompose":
        verify_decompose_outcome(calculate_result, owner_class, bound_method)

    return calculate_result
```

**Why dry-run at class-definition time already:** this is one of the key
architectural principles of the whole system — errors in user logic
(`_logic` returning the wrong type, `_validate` raising an unexpected
exception, `_decompose` returning a tuple of the wrong length) are caught
**immediately, at module import time**, not later in production on the
first real instance. The test values (`test_value`) are always derived from
the defaults — so the dry run always runs against values the system already
knows are valid.

For `_logic`, this dry run is furthermore directly **the source of the whole
composition's default value** — `process_classmethod`, with
`return_calculated_value=True`, returns the `calculated_value` from
`verify_calculation`, and `SimpleObjectMetadata` uses it directly as
`self.default`. In other words: a composition's `_default` is nothing more
than the result of its own dry run.

[▲ Back to Contents](#-contents)

---

## `verify_decompose_outcome` — special rules for `_decompose`

This only runs when the method being verified is `_decompose` — it checks
that the returned tuple structurally matches `_inners`.

**Parameters:** `calculate_default` (the dry run's result), `owner_class`,
`bound_method`

**Return value:** `None` (raises an exception on a mismatch).

**Two levels of checking:**

1. **Length.** The returned tuple must have exactly as many elements as
   `_inners` — otherwise `raise_decompose_unvalide_outcome_length`.
2. **Individual items.** For each position, it checks whether the value
   either matches the corresponding inner element's type
   (`isinstance(value, expected_type)`), or equals its default (`value ==
   inner.meta.default`) — the second condition is a deliberate concession
   for the dry-run scenario, where decomposing the composition's default
   value naturally returns the individual `_inners`' defaults, which aren't
   necessarily strictly `isinstance`-compatible (e.g. sentinels). If
   neither holds, the micro-validators run for precise diagnostics.

[▲ Back to Contents](#-contents)
