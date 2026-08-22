from typing import TYPE_CHECKING
# Inners
from .validations import raise_invalide_extend_instance_class_definition
# Annotations
if TYPE_CHECKING:
    from .....protocols.alias_typings import MixinsTuple
    from .....protocols.instance import SimpleInstanceLike


def _extend_instance_class(
    mixins: "MixinsTuple",
    instance_class: "SimpleInstanceLike",
) -> None:
    """Applies in-place class modifications defined by mixin __extend_instance_class__ hooks."""

    # 1. Traverse flattened mixins
    for mixin in mixins:

        # 2. Inspect raw dictionary for metaprogramming extension hook
        if "__extend_instance_class__" in mixin.__dict__:

            # 3. Validate that the hook is properly decorated as staticmethod or classmethod
            raw_attr = mixin.__dict__["__extend_instance_class__"]
            if not isinstance(raw_attr, (staticmethod, classmethod)):
                raise_invalide_extend_instance_class_definition(instance_class, mixin)

            # 4. Execute in-place class modification hook
            mixin.__extend_instance_class__(instance_class)


_DESIGN_NOTES = """
# _extend_instance_class

## Purpose
Applies metaprogramming extensions directly to the newly compiled `instance_class` in-place[cite: 24].
Serves as an extension gateway for complex mixins (e.g., `InnersProperty`, `Equalizer`, 
`ImmutableWithInners`) that need to dynamically bind descriptor attributes, setters, or 
specialized protocols directly onto the compiled class object.

## Pipeline & Logic
1. **Direct Dictionary Inspection**
   Checks `mixin.__dict__` directly for `__extend_instance_class__` to avoid descriptor binding 
   or descriptor evaluation during inspection.

2. **Decorator Validation**
   Ensures `__extend_instance_class__` is defined as either `@staticmethod` or `@classmethod`. 
   Raw instance methods or un-decorated attributes trigger `raise_invalide_extend_instance_class_definition`.

3. **In-Place Modification (`None` return)**
   Invokes `mixin.__extend_instance_class__(instance_class)`. The hook modifies `instance_class` 
   directly (e.g., using `setattr`). Returns `None` following Python's standard in-place 
   mutation convention.

## Architectural Notes
- **In-Place Mutator Pattern**: Aligns with Python built-ins like `list.sort()` by returning `None`,
  reflecting that `instance_class` is mutated in-place in memory.
- **Post-Compilation Hook**: Executes after `type()` has built the class, giving mixins complete 
  access to the finalized target class object.
"""