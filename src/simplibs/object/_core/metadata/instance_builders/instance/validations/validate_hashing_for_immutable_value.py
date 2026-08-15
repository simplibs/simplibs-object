from typing import TYPE_CHECKING
# Outers
from ......exceptions import SimpleInitializationError
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_hashing_for_immutable_value(
    cls: "SimpleClassLike",
) -> None:
    """
    Validates that the default value is hashable for immutable instances.

    Immutable instances rely on value-based identity and must therefore wrap
    a hashable default value. If hashing fails, a structured `SimpleInitializationError`
    is raised with a clear diagnostic message.
    """

    try:
        hash(cls.meta.default)
    except Exception as error:
        raise SimpleInitializationError(
            error_name="UNHASHABLE DEFAULT",
            label="immutable_requires_hashable_default",
            expected="Hashable default value",
            value=cls.meta.default,
            problem=(
                f"Immutable instance '{cls.meta.class_name}' cannot wrap a "
                f"non-hashable default value."
            ),
            context=f"create_instance(cls={cls.meta.class_name}, mutable=False)",
            how_to_fix=(
                "Ensure that the default value is hashable.",
                "Examples of hashable values: int, float, str, tuple, frozenset.",
                "Examples of non-hashable values: list, dict, set, custom mutable objects.",
            ),
            exception=TypeError,
        ) from error


_DESING_NOTES = """
# validate_hashing_for_immutable_value

## Purpose
Ensures that immutable instances wrap a hashable default value. Immutable objects
in the Simple system rely on value-based identity and must therefore participate
safely in hashing operations (e.g., dictionary keys, sets, structural equality).

## Behavior
1. Attempts to hash `cls.meta.default`.
2. If hashing succeeds, the instance is safe to construct.
3. If hashing fails, raises a structured `SimpleInitializationError` describing:
   - the nature of the problem,
   - the expected contract,
   - the offending value,
   - how to fix the issue.

## Notes
- Hashability is determined using Python’s built-in `hash()` function, which is
  the only reliable and universal test.
- This validator is invoked early in the instance-builder pipeline, before any
  mixin logic or class compilation.
- Immutable instances must remain stable and deterministic; non-hashable values
  violate this contract.
"""