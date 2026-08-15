from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .SimpleConstant import SimpleConstant
from ._core.protocols.methods import LogicSignature, P, R
from ._core.logic.object_methods import calculate_value as _calculate_value
from ._core.logic.object_methods import decompose_value as _decompose_value
# Annotations
if TYPE_CHECKING:
    from ._core.protocols.classes import SimpleObjectProtocol
    from ._core.protocols.alias_typings import ValidTypes, InnersTuple


class SimpleObject(SimpleConstant):
    """
    Declarative base class for defining composite objects in the Simple system.

    A composite object represents a structured value computed from inner
    constant or composite nodes. It extends `SimpleConstant` with:

    - a required `_inners` declaration,
    - a required `_logic` method for computing the composite value,
    - an optional `_decompose` method for reverse decomposition,
    - an optional `_validate` method for extended validation.

    Composite objects form the core of the Simple system and enable declarative,
    type-safe, and metadata-driven computation.
    """

    # ----------------------------------------------------------------------
    # 1) Declarative interface (user-defined)
    # ----------------------------------------------------------------------

    # Required type annotation for the composite's computed value.
    _type: "ValidTypes" = UNSET

    # Required tuple of inner elements (constants or composite nodes).
    _inners: "InnersTuple" = UNSET

    @classmethod
    def _logic(
        cls: "SimpleObjectProtocol",
        *args,
        **kwargs
    ) -> Any:
        """
        Required computation hook for composite objects.

        Users must override this method to define how the composite value is
        computed from its inner elements. The method receives parameters
        corresponding to `_inners` and must return a value that passes full
        validation.

        If not overridden, the method returns UNSET and metadata validation
        will raise an error.
        """
        return UNSET

    @classmethod
    def _decompose(
        cls: "SimpleObjectProtocol",
        value: Any
    ) -> Any:
        """
        Optional reverse-decomposition hook.

        Users may override this method to support two-way composite behavior:
        converting a composite value back into values for its inner elements.

        This is useful for bidirectional models, but not required. If not
        overridden, the method returns UNSET and the composite is treated as
        non-decomposable.
        """
        return UNSET

    @classmethod
    def _validate(
        cls: "SimpleObjectProtocol",
        value: Any,
        *,
        return_bool: bool = False
    ) -> bool | Exception:
        """
        Optional extended validation hook.

        Users may override this method to provide additional validation beyond
        basic type checking. The method may:

        - return True/False,
        - raise a custom exception,
        - or use `bool_or_raise_validate_error` for structured error reporting.

        If not overridden, the method defaults to accepting all values that
        pass type validation.
        """
        return True

    # ----------------------------------------------------------------------
    # 2) Public class-level API (metadata-driven)
    # ----------------------------------------------------------------------

    @classmethod
    def calculate_value(
        cls: LogicSignature[P, R],
        *args: P.args,
        **kwargs: P.kwargs
    ) -> R:
        """Compute the composite value using the class's `_logic` method.

        This method:
        - processes parameters according to metadata,
        - validates inner values,
        - invokes the user-defined `_logic`,
        - returns the computed composite value.

        Thanks to ParamSpec, IDEs (including PyCharm) provide autocompletion
        for the parameters of `_logic`.

        Args:
            *args: Positional arguments mapped to inner elements.
            **kwargs: Keyword arguments mapped to inner elements.

        Returns:
            The computed composite value.

        Raises:
            SimpleLogicError: If parameter processing or validation fails.
        """
        return _calculate_value(cls, *args, **kwargs)

    @classmethod
    def decompose_value(
        cls: "SimpleObjectProtocol",
        value: Any
    ) -> Any:
        """Decompose a composite value into its inner components.

        This method:
        - validates the provided value,
        - checks whether the composite supports decomposition,
        - invokes the user-defined `_decompose` method,
        - returns the decomposed representation.

        Args:
            value: The composite value to decompose.

        Returns:
            The decomposed representation of the value.

        Raises:
            SimpleLogicError: If the composite is not decomposable or
                if validation fails.
        """
        return _decompose_value(cls, value)


_DESIGN_NOTES = """
# SimpleObject — Declarative Composite Node

## Purpose
`SimpleObject` is the core declarative class for defining composite structures in
the Simple system. A composite object represents a value computed from multiple
inner elements (`_inners`) using a user-defined `_logic` method. It extends
`SimpleConstant` with structural composition, metadata-driven computation, and
optional bidirectional behavior.

Composite objects form the backbone of the Simple ecosystem, enabling declarative,
type-safe, and deterministic modeling of structured values.

---

## 1. Declarative Interface

### `_type`
Required type annotation describing the composite's computed value. The result of
`_logic` must pass full validation against this type.

### `_inners`
Required tuple of inner elements. Each inner element is a `SimpleConstant` or
another `SimpleObject`. The structure of `_inners` determines:

- the parameters expected by `_logic`,
- the default value of the composite,
- the decomposition behavior (if supported),
- the metadata layout of the composite.

### `_logic`
Required computation hook. This method defines how the composite value is
computed from its inner elements. It receives parameters corresponding to
`_inners` and must return a value that passes full validation.

The default value of the composite is computed by invoking `_logic` with the
default values of all inner elements.

### `_decompose`
Optional reverse-decomposition hook. When implemented, this method converts a
composite value back into values for its inner elements. This enables
bidirectional models where both upward (inner → composite) and downward
(composite → inner) computation is supported.

If not implemented, the composite is treated as non-decomposable.

### `_validate`
Optional extended validation hook. Allows users to enforce additional validation
rules beyond basic type checking. The method may:

- return True/False,
- raise a custom exception,
- or use `bool_or_raise_validate_error` for structured error reporting.

---

## 2. Metadata Behavior

Composite metadata differs from constant metadata in several key ways:

### Default Value
Unlike `SimpleConstant`, composite classes **must not** define `_default`.
If a user attempts to define `_default`, metadata processing raises a structured
error. The default value is always computed automatically using:

```
_logic(defaults_of_inners)
```

This ensures deterministic and consistent default propagation across composite
structures.

### Decomposability
Metadata determines whether the composite supports decomposition:

- If `_decompose` is implemented → `is_decomposeable = True`
- If `_decompose` is not implemented → `is_decomposeable = False`

This flag is used by `decompose_value` to enforce correct behavior.

### Inner Structure
Metadata validates:

- the structure of `_inners`,
- the compatibility of `_logic` parameters,
- the types of inner elements,
- the default propagation rules.

---

## 3. Public API

### `calculate_value`
Computes the composite value using:

1. parameter processing,
2. validation,
3. invocation of `_logic`.

This method is fully metadata-driven and provides IDE autocompletion for
`_logic` parameters via `ParamSpec`.

### `decompose_value`
Decomposes a composite value into its inner components. This method:

1. validates the provided value,
2. checks decomposability,
3. invokes `_decompose` if supported.

If the composite is not decomposable, a structured error is raised.

---

## 4. Architectural Role

`SimpleObject` is the flagship class of the Simple system. It provides:

- declarative composite modeling,
- deterministic default propagation,
- metadata-driven computation,
- optional bidirectional behavior,
- type-safe structured values,
- seamless integration with `SimpleConstant`.

Composite objects allow developers to define complex structures using simple,
readable, declarative Python classes.

---

## Notes
- Composite objects inherit all validation and normalization behavior from
  `SimpleConstant`.
- `_logic` is always required; `_decompose` and `_validate` are optional.
- `_default` must never be defined on composite classes.
- All runtime behavior is delegated to metadata and core logic functions.
```
"""