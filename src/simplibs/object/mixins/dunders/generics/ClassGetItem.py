from typing import Any, Self
# Outers
from ...base_class import SimpleMixin


class ClassGetItem(SimpleMixin):
    """
    Mixin providing support for generic-style subscript syntax:

        MyClass[int]
        MyClass[str]
        MyClass[tuple[int, str]]

    This method is purely a syntactic aid for type hints, IDEs, and
    static analysis. It has no effect on the instance's runtime behavior
    or on the construction of the instance class.

    Logic:
    - If a parent class already implements __class_getitem__, that
      implementation is used.
    - If it doesn't exist (the common case for plain classes), the class
      itself is returned.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Classmethods - CLASS GETITEM
    # ----------------------------------------

    @classmethod
    def __class_getitem__(
        cls: type[Self],
        item: Any
    ) -> type[Self] | Any:
        """
        Enables the MyClass[T] syntax without having to inherit from
        typing.Generic.

        If the parent class implements __class_getitem__, its
        implementation is used. Otherwise the class itself is returned,
        which is the standard fallback Python uses for simple generic
        subscript syntax.
        """

        # 1. Look up the method on the parent class
        super_cls = super(ClassGetItem, cls)
        method = getattr(super_cls, "__class_getitem__", None)

        # 2. Return the method's result, or the class as a fallback
        return (
            method(item)
            if method is not None
            else cls
        )


_DESIGN_NOTES = """
# ClassGetItem

## Purpose
Lets a Simple class be subscripted like `MyClass[int]` without having to
inherit from `typing.Generic`. Purely cosmetic/typing sugar — it doesn't
change what the class does at runtime.

> For newcomers: `__class_getitem__` is what makes `list[int]` or
> `dict[str, int]` work in modern Python type hints. Adding it here means
> a Simple blueprint can be written or annotated the same familiar way,
> even though it isn't a generic class in the `typing.Generic` sense.

## Compatibility
- No compatibility flags — purely additive, has no interaction with
  value, mutability, or composite/atom distinctions.

## Logic
- Looks up `__class_getitem__` on the parent class via `super()`.
- If the parent defines one (e.g. because it *does* inherit from
  `Generic`), that implementation wins — this mixin steps out of the way.
- If not, it falls back to returning the class itself unchanged, which is
  the same fallback CPython uses internally for plain classes.

## Notes
- No `TYPE_CHECKING` import block, unlike most other mixins in this
  package — the method takes no protocol-typed `self` parameter since
  it's a `classmethod` operating on `cls`, not on an instance.
- Has zero effect on instance creation, validation, or the
  `create_instance` pipeline — it only affects what `MyClass[...]`
  returns when read by a type checker or at import time.
"""
