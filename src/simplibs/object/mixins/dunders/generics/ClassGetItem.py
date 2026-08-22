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
    - If it doesn't exist (the common case for plain classes), or if
      the MRO traversal raises TypeError on dynamically generated classes,
      the class itself is returned.
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
        try:
            # Look up method on the parent via standard super() inside classmethod
            super_method = getattr(super(), "__class_getitem__", None)
            if super_method is not None:
                return super_method(item)
        except (TypeError, AttributeError):
            # Fallback for dynamic class hierarchies or missing parent implementations
            pass

        return cls


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

## Architecture & Logic
- **`super()` resolution in `@classmethod`:** 
  The implementation relies on zero-argument `super().__class_getitem__` inside 
  a defensive `try...except (TypeError, AttributeError)` block.
- **Why avoid explicit `super(ClassGetItem, cls)`:**
  In dynamic metaclass architectures, `cls` is an instance class created 
  at runtime whose Method Resolution Order (MRO) may not explicitly expose 
  `ClassGetItem` as a direct parent or subtype in the exact manner CPython's 
  type checker expects at runtime. Explicit 2-argument `super(Type, obj)` enforces 
  `isinstance(obj, Type)` or `issubclass(obj, Type)`, which raises 
  `TypeError: super(type, obj): obj must be an instance or subtype of type` 
  when called on dynamically synthesized leaf classes.
- **Fallback Mechanism:**
  If a parent class defines `__class_getitem__` (e.g., inheriting from `Generic` 
  or another specialized container), that parent method takes precedence. If no 
  parent defines it, or if dynamic MRO introspection raises a `TypeError`, 
  the mixin safely catches the exception and falls back to returning `cls` unchanged.

## Notes
- No `TYPE_CHECKING` import block, unlike most other mixins in this
  package — the method takes no protocol-typed `self` parameter since
  it's a `classmethod` operating on `cls`, not on an instance.
- Has zero effect on instance creation, validation, or the
  `create_instance` pipeline — it only affects what `MyClass[...]`
  returns when read by a type checker or at import time.
"""