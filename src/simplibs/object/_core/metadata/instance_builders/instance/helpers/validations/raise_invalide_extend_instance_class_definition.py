from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleInitializationError
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.mixins.base_class import SimpleMixinProtocol


def raise_invalide_extend_instance_class_definition(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
) -> None:
    """Raises an error when __extend_instance_class__ hook on a mixin is not a classmethod or staticmethod."""

    raw_attr = mixin.__dict__["__extend_instance_class__"]

    raise SimpleInitializationError(
        error_name="INVALID EXTEND INSTANCE CLASS DEFINITION",
        label="mixin_invalid_extend_instance_class_definition",
        expected="@classmethod or @staticmethod decorator on __extend_instance_class__",
        value=type(raw_attr).__name__,
        problem=(
            f"Mixin '{mixin.__name__}' defines '__extend_instance_class__' as an "
            f"un-decorated method or invalid descriptor ({type(raw_attr).__name__}) "
            f"when compiling instance class for '{cls.__name__}'."
        ),
        context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
        how_to_fix=(
            "Decorate '__extend_instance_class__' on the mixin with @classmethod or @staticmethod.",
            "Example:",
            "    class MyMixin(SimpleMixin):",
            "        @classmethod",
            "        def __extend_instance_class__(cls, instance_cls):",
            "            # In-place class modification logic",
            "            ...",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_invalide_extend_instance_class_definition

## Purpose
Signals that a mixin defines the `__extend_instance_class__` metaprogramming hook without 
properly wrapping it in `@classmethod` or `@staticmethod`.

## Behavior
- Triggered when:
  - `"__extend_instance_class__" in mixin.__dict__`
  - AND `not isinstance(raw_attr, (staticmethod, classmethod))`
- Raises `SimpleInitializationError` with a detailed diagnostic message and clear resolution steps.

## Notes
- Direct dictionary inspection (`mixin.__dict__`) retrieves raw attributes before descriptor 
  binding occurs.
- Raw instance methods are not callable at class-compilation time because no instance of 
  the mixin exists yet.
- Requiring `@classmethod` or `@staticmethod` guarantees that the extension hook can be 
  safely executed against the newly created runtime instance class (`_instance_cls`).
"""