from typing import TYPE_CHECKING, NoReturn
# Outers
from .....exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_init_mixins_contains_super_call(
    cls: "SimpleMixinProtocol",
) -> NoReturn:
    """Raises an error when a mixin overrides 'init_mixins' and contains a call to super(),

    which violates the isolated mixin synthesis architecture.
    """
    func = cls.__dict__["init_mixins"]

    raise SimpleRuntimeError(
        error_name="MIXIN DEFINITION ERROR",
        label="Forbidden super() call in init_mixins",
        expected="The method init_mixins must NOT call super().init_mixins().",
        value=func,
        problem=(
            f"Mixin '{cls.__name__}' overrides 'init_mixins' and calls super().",
            "Mixins are synthesized directly into target classes without MRO inheritance.",
            "Calling super() inside synthesized mixin hooks causes runtime TypeErrors.",
        ),
        context=f"Mixin definition check: {cls.__name__}",
        how_to_fix=(
            "Remove all super() calls from init_mixins().",
            "The instance compilation engine automatically orchestrates and calls all mixin hooks.",
            "Example:",
            "    def init_mixins(self):",
            "        self._my_slot = 'default_value'",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_init_mixins_contains_super_call

## Purpose
Ensures that any mixin overriding the `init_mixins` hook does NOT call `super().init_mixins()`.
This enforces hook isolation and prevents runtime MRO resolution failures.

## Architectural reasoning
Mixins in the Simple system are dynamically merged into runtime-generated instance classes
via dictionary synthesis rather than Python's standard MRO inheritance.

Because mixin classes do not reside in the instance class MRO:
- Calling `super()` inside a synthesized mixin method fails with `TypeError: super(type, obj): obj must be an instance or subtype of type`.
- Hook execution order and chaining are automatically managed by the compiler via `_build_combined_init_mixins`.

Every overriding mixin must isolate its initialization logic solely to its own slots and state.

## Pipeline position
This check occurs during `verify_mixin_definition` after validating:
1. `__slots__`,
2. slot types,
3. forbidden slot names,
4. mixin flags,
5. `_only_types`.

## Diagnostic value
The error message includes:
- the offending method object,
- a clear explanation of why `super()` is prohibited in flat mixin synthesis,
- a description of the expected isolated hook structure,
- a concrete example of the correct implementation.

## Notes
- This is a pure `raise_...` function.
- It is triggered at class creation time via `SimpleMixinMeta`.
"""