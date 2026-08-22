from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .validations.mixins_validations import (
    validate_mixin_is_class,
    validate_mixin_is_simple_base_subclass,
    raise_mixin_not_allowed_for_mutable,
    raise_mixin_not_allowed_for_immutable,
    raise_mixin_not_allowed_for_constant,
    raise_mixin_not_support_default_value_type,
    raise_mixin_not_allowed_for_composite,
)
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike
    from .....protocols.mixins.base_class import SimpleMixinProtocol


# noinspection PyProtectedMember
def _verify_mixin_compatibility(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
    is_atom: bool,
    mutable: bool = True,
) -> None:
    """Validates mixin identity and compatibility constraints."""

    # 1. Local import to avoid circular dependencies
    from ......mixins.base_class import SimpleMixin

    # 2. Identity validation
    # noinspection PyTypeChecker
    if (
        not isinstance(mixin, type)
        or not issubclass(mixin, SimpleMixin)
    ):
        validate_mixin_is_class(cls, mixin)
        validate_mixin_is_simple_base_subclass(cls, mixin)


    # 3. Compatibility matrix
    mixin: "SimpleMixinProtocol"
    if mixin._constant_only and not is_atom:
        raise_mixin_not_allowed_for_composite(cls, mixin)

    if mixin._composite_only and is_atom:
        raise_mixin_not_allowed_for_constant(cls, mixin)

    if mixin._mutable_only and not mutable:
        raise_mixin_not_allowed_for_immutable(cls, mixin)

    if mixin._immutable_only and mutable:
        raise_mixin_not_allowed_for_mutable(cls, mixin)

    if mixin._only_types is not UNSET and not isinstance(cls.meta.default, mixin._only_types):
        raise_mixin_not_support_default_value_type(cls, mixin)


_DESIGN_NOTES = """
# _verify_mixin_compatibility

## Purpose
Validates mixin identity and enforces compatibility constraints defined on
`SimpleMixin`. Ensures that only structurally valid mixins are applied to
instances with matching topology and mutability.

## Behavior
1. Identity validation:
   - mixin must be a class
   - mixin must inherit from `SimpleMixin`
2. Compatibility matrix:
   - `_constant_only`      → atomic only
   - `_composite_only`     → composite only
   - `_mutable_only`       → mutable only
   - `_immutable_only`     → immutable only
   - `_only_types`         → default value type constraint

## Notes
- Uses lazy import of `SimpleMixin` to avoid circular dependencies.
- Keeps the validator minimal and deterministic.
- Ensures that mixins cannot be misapplied to incompatible instance types.

"""