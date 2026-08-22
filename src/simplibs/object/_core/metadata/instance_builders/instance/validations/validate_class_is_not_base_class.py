from typing import TYPE_CHECKING
# Outers
from ......exceptions import SimpleInitializationError
from ....constants import BASE_CLASS_NAMES
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_class_is_not_base_class(
    cls: "SimpleClassLike",
) -> None:
    """Validates that the user did not pass a raw Simple base class."""

    # 1. Check base-class misuse
    if cls.__name__ not in BASE_CLASS_NAMES:
        return

    # 2. Raise error
    raise SimpleInitializationError(
        error_name="INVALID CLASS",
        label="base_class_not_allowed",
        expected="Declarative subclass of SimpleBase",
        value=cls,
        problem=f"Class '{cls.__name__}' is a core Simple framework base class and cannot be instantiated.",
        context=f"create_instance(cls={cls.__name__})",
        how_to_fix=(
            "Use a declarative class derived from SimpleObject or SimpleConstant.",
            "Example:",
            "    class MyNumber(SimpleObject):",
            "        _type = int\n",
            "Base classes (SimpleObject, SimpleAtom, SimpleComposite, …) serve only as framework primitives.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_class_is_not_base_class

## Purpose
Prevents users from creating runtime instances directly from Simple’s internal
framework base classes. Only declarative subclasses may be instantiated.

## Behavior
1. Checks whether the class name appears in `BASE_CLASS_NAMES`.
2. If yes, raises `SimpleInitializationError` with a clear remediation message.

## Notes
- Base classes define structural behavior and metadata mechanics; they are not
  valid runtime entities.
- This validator is the first guard in the instance‑builder pipeline and ensures
  that all subsequent logic operates on valid declarative classes.
"""