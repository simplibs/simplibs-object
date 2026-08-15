from typing import TYPE_CHECKING, NoReturn
# Outers
from .....exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_init_mixins_missing_super_call(
    cls: "SimpleMixinProtocol",
) -> NoReturn:
    """
    Raises an error when a mixin overrides 'init_mixins' but does not call
    super().init_mixins(), breaking the initialization chain.
    """

    func = cls.__dict__["init_mixins"]
    called_names = func.__code__.co_names

    raise SimpleMixinError(
        error_name="MIXIN DEFINITION ERROR",
        label="Missing super() call in init_mixins",
        expected="The method init_mixins must call super().init_mixins().",
        value=func,
        problem=(
            f"Mixin '{cls.__name__}' overrides 'init_mixins', but does not call super().init_mixins().",
            "This breaks the mixin initialization chain.",
            "Parent mixins are not initialized correctly.",
        ),
    context=f"Mixin definition check: {cls.__name__}",
        how_to_fix=(
            "Add a call to super().init_mixins() inside the method.",
            "Example:",
            "    def init_mixins(self):",
            "        super().init_mixins()",
            "        # your mixin initialization logic here",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_init_mixins_missing_super_call

## Purpose
Ensures that any mixin overriding the `init_mixins` method correctly calls
`super().init_mixins()`. This preserves the initialization chain required for
multiple mixins to cooperate safely.

## Architectural reasoning
Mixins in the Simple system are applied dynamically during instance creation.
Each mixin may define its own initialization logic inside `init_mixins`.

To ensure that:

- parent mixins are initialized,
- sibling mixins are initialized,
- the base class initialization runs,

every overriding mixin **must** call:

```python
super().init_mixins()
```

If this call is missing, the initialization chain is broken, causing:

- missing state initialization,
- inconsistent runtime behavior,
- subtle bugs that are difficult to diagnose.

## Pipeline position
This check occurs at the end of `verify_mixin_definition`, after validating:

1. `__slots__`,
2. slot types,
3. forbidden slot names,
4. mixin flags,
5. `_only_types`.

It is the final structural validation step for mixin definitions.

## Diagnostic value
The error message includes:

- the offending method object,
- a clear explanation of the problem,
- a description of the expected behavior,
- a concrete example of the correct implementation.

This makes debugging straightforward and prevents silent initialization failures.

## Notes
- This is a pure `raise_...` function.
- It is used exclusively by the mixin definition validator.
- All mixins overriding `init_mixins` must pass this check.
"""