from typing import Any, Callable, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .create_constant_class import create_constant_class
from .create_object_class import create_object_class
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols import SimpleClassType, SimpleMixinLike, SimpleClassLike


# noinspection PyTypeChecker
def create_simple_object(
    class_name: str,
    default: Any | UnsetType = UNSET,
    inners: tuple["SimpleClassType", ...] | UnsetType = UNSET,
    value_type: type | UnsetType = UNSET,
    validate: Callable | UnsetType = UNSET,
    logic: Callable | UnsetType = UNSET,
    decompose: Callable | UnsetType = UNSET,
    return_instance: bool = False,
    mixins: tuple["SimpleMixinLike", ...] = (),
    as_atom: bool = False,
    mutable: bool = True,
) -> Any:
    """Universal facade for dynamically creating SimpleConstant or SimpleObject blueprints/instances.

    Routes execution based on the presence of ``inners``:
    - If ``inners`` is UNSET: Constructs a leaf ``SimpleConstant`` class definition.
    - If ``inners`` is supplied: Constructs a composite ``SimpleObject`` class definition.

    Args:
        class_name: Target name of the generated class.
        default: Static default value (required for leaf constants).
        inners: Tuple of inner component classes (required for composite objects).
        value_type: Explicit value type override.
        validate: Optional validation callable or lambda rule.
        logic: Functional calculation rule deriving value from inner components.
        decompose: Optional top-down value decomposition callable or lambda rule.
        return_instance: If True, returns an instantiated object instead of the class blueprint.
        mixins: Mixin instances to bind during class instantiation (if return_instance=True).
        as_atom: Instantiates the object in atomic mode (if return_instance=True).
        mutable: Instantiates the object as mutable/immutable (if return_instance=True).

    Returns:
        Newly constructed Simple class blueprint, or its initialized instance if return_instance=True.
    """

    # 1. Route to SimpleConstant creation for leaf nodes
    if inners is UNSET:
        _class: "SimpleClassLike" = create_constant_class(
            class_name=class_name,
            default=default,
            value_type=value_type,
            validate=validate,
        )

    # 2. Route to SimpleObject creation for composite nodes
    else:
        _class = create_object_class(
            class_name=class_name,
            inners=inners,
            logic=logic,
            value_type=value_type,
            validate=validate,
            decompose=decompose,
        )

    # 3. Return class blueprint or instantiated object
    return (
        _class
        if not return_instance
        else _class(
            mixins=mixins,
            as_atom=as_atom,
            mutable=mutable
        )
    )


_DESIGN_NOTES = """
# create_simple_object (Orchestrator Facade)

## Purpose
Serves as the primary universal entry point for programmatic, statement-less creation 
of both leaf constants (`SimpleConstant`) and composite objects (`SimpleObject`).

## Architecture & Routing Logic
- **Leaf Mode (`inners` is UNSET):** Delegates class creation directly to `create_constant_class`. 
  Boundary checks (ensuring non-None default, absence of logic/decompose) are delegated to the constant creator.
- **Composite Mode (`inners` is provided):** Delegates class creation directly to `create_object_class`. 
  Boundary checks (ensuring valid logic and child parameters) are delegated to the composite creator.
- **Instantiation Dispatch:** If `return_instance=True`, immediately instantiates the dynamically 
  created class with the specified `mixins`, `as_atom`, and `mutable` settings.

## Framework Usage
- Public API helper for functional definition of dynamic domain tree components.
"""