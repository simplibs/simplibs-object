from typing import Any, TYPE_CHECKING
# Inners
from .ImmutableMethods import ImmutableMethods
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.immutable import ImmutableMethodsWithInnersProtocol
    from ...._core.protocols.instance import SimpleInstanceLike


class ImmutableWithInners(ImmutableMethods):
    """
    Adds, on top of the base class's basic methods, dedicated methods for
    every inner.

    Guarantees the presence of dynamically generated immutable methods
    (setters) for each inner element (e.g. `obj.with_uzel(value)`).
    Every one of these methods produces a new, transformed instance (Self).
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _immutable_only = True
    _composite_only = True

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Hook for modifying the instance class
    # ----------------------------------------

    @staticmethod
    def __extend_instance_class__(
        instance_cls: "SimpleInstanceLike"
    ) -> "SimpleInstanceLike":
        """
        Internal method for attaching elements to the class, before the
        initialization process.
        """

        # 1. Iterate over nodes
        for name in instance_cls.meta.node_names_set:

            # 2. Method definition
            # (All use the composite method, since it forwards constants to with_constant)
            def method(self: "ImmutableMethodsWithInnersProtocol", value: Any, _name: str=name):
                return self.with_composite(_name, value)

            # 3. Set the inner element's attributes
            method_name = f"with_{name}"
            method.__name__ = method_name
            method.__doc__ = (
                f"Immutable setter for the value `{name}`.\n"
                f"Returns a new immutable instance with `{name}` changed."
            )

            # 4. Create the method attribute
            setattr(instance_cls, method_name, method)

        # 5. Return the modified class
        return instance_cls


_DESIGN_NOTES = """
# ImmutableWithInners

## Purpose
Generates a dedicated `with_<name>(value)` method for every inner of a
composite, so instead of writing `obj.with_composite("uzel", value)`
generically, callers get a specific, autocomplete-friendly
`obj.with_uzel(value)` for each field the blueprint actually defines.

> For newcomers: this is code generation at class-creation time, not at
> instance-creation time — the methods are attached once, when the
> instance class itself is built, and every instance of that class shares
> them.

## Compatibility
- `_immutable_only = True` — inherited requirement, since every generated
  method returns a new instance rather than mutating.
- `_composite_only = True` — per-inner setters only make sense where
  inners exist; an atom has nothing to generate methods for.

## Logic
`__extend_instance_class__` runs once per instance class, before
initialization:
1. Iterates `instance_cls.meta.node_names_set` — every inner's name.
2. For each name, defines a small closure `method(self, value, _name=name)`
   that forwards to `self.with_composite(_name, value)`. The default
   argument `_name=name` is what pins each generated method to its own
   name — without it, every closure would share the loop variable and
   all end up pointing at the last name iterated.
3. Names the method `with_<name>`, gives it a generated docstring, and
   attaches it to the class via `setattr`.

The comment "all use the composite method, since it forwards constants to
with_constant" explains why there's no special-casing between constant
inners and composite inners here — `with_composite` already knows how to
route a constant change down to `with_constant` internally.

## Notes
- This is one of the (apparently few) mixins that actually uses the
  `__extend_instance_class__` hook, alongside property-generating mixins
  like `InnersProperty` and `Equalizer` — most mixins only use
  `init_mixins`.
- The generated methods are true instance-class attributes, not computed
  per-instance — inspectable via `dir()` or `help()` on the class itself.
"""
