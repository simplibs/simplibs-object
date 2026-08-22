from typing import TYPE_CHECKING
from simplibs.randomize import RegistryBase
# Inners
from .randomize_value import randomize_value
from ._validations import (
    validate_instance_is_simple_constant_base,
    validate_retries_is_int,
    validate_retries_is_greater_than_zero,
    validate_registry_is_randomize_registry_base,
    validate_skip_unregistered_is_bool,
    validate_skip_immutable_is_bool,
)
# Outers
from ...SimpleConstant import SimpleConstant
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.instance import SimpleInstanceLike


# noinspection PyProtectedMember
def random_data_filler(
    instance: "SimpleInstanceLike",
    *,
    retries: int = 5,
    registry: RegistryBase | None = None,
    skip_unregistered: bool = False,
    skip_immutable: bool = True,
    validate: bool = True,
) -> "SimpleInstanceLike":
    """Recursively fuzz-fills a Simple instance tree with random, valid values.

    For constant leaves, generates a random value matching the declared type hint (via ``simplibs-randomize``)
    and attempts assignment, retrying on validation failure. For composite nodes, additionally attempts
    a direct top-down assignment when the node supports decomposition, and recursively traverses inner
    children to exercise bottom-up propagation.

    Args:
        instance: The target ``SimpleConstant`` or composite object tree root to fill.
        retries: Maximum generation and assignment attempts per leaf node.
        registry: Optional custom ``RegistryBase`` instance providing scoped randomizers.
        skip_unregistered: If ``True``, ignores unregistered types rather than raising an error.
        skip_immutable: If ``True``, locked or immutable instances are bypassed without mutation.
        validate: Enables argument type and boundary validation when ``True``.

    Returns:
        The mutated root instance modified in-place.
    """

    # ------------------------------------------------------------
    # 1. Parameter Validation Gate
    # ------------------------------------------------------------
    if validate and not (
        isinstance(instance, SimpleConstant)
        and isinstance(retries, int) and retries > 0
        and (registry is None or isinstance(registry, RegistryBase))
        and isinstance(skip_unregistered, bool)
        and isinstance(skip_immutable, bool)
    ):
        validate_instance_is_simple_constant_base(instance)
        validate_retries_is_int(retries)
        validate_retries_is_greater_than_zero(retries)
        validate_registry_is_randomize_registry_base(registry)
        validate_skip_unregistered_is_bool(skip_unregistered)
        validate_skip_immutable_is_bool(skip_immutable)

    # ------------------------------------------------------------
    # 2. Immutable Instance Bypass Check
    # ------------------------------------------------------------
    instance: "SimpleInstanceLike"
    is_immutable = not getattr(instance, "__is_mutable__", True)
    is_locked = getattr(instance, "_locked", False)

    if skip_immutable and (is_immutable or is_locked):
        return instance

    # ------------------------------------------------------------
    # 3. Leaf Constant & Decomposable Composite Direct Randomization
    # ------------------------------------------------------------
    if instance.meta.is_constant or instance.meta.is_decomposeable:
        randomize_value(
            instance,
            retries=retries,
            registry=registry,
            skip_unregistered=skip_unregistered,
            validate=False,
        )

    # ------------------------------------------------------------
    # 4. Recursive Composite Children Traversal
    # ------------------------------------------------------------
    if hasattr(instance.meta, "inners"):
        for inner in instance.meta.inners:

            # 4.1 Extract private inner instance reference
            inner_instance = getattr(instance, inner.meta.name_private)

            # 4.2 Recurse down to child node
            random_data_filler(
                inner_instance,
                retries=retries,
                registry=registry,
                skip_unregistered=skip_unregistered,
                skip_immutable=skip_immutable,
                validate=False,
            )

    # ------------------------------------------------------------
    # 5. Return Mutated Root Instance
    # ------------------------------------------------------------
    return instance


_DESIGN_NOTES = """
# random_data_filler (Tree-Level Fuzzing Engine)

## Purpose
Acts as the top-level tree-traversal entry point for fuzzing `SimpleObject` and `SimpleConstant` instances. 
It recursively walks through object hierarchies, populating leaf values and composite structures with 
schema-compliant random data.

## Execution Workflow
1. **Validation Gate:** Validates initial arguments when `validate=True`. Child recursive calls set `validate=False` 
   for performance optimization.
2. **Immutability Protection:** Bypasses nodes when `skip_immutable=True` if the node is marked immutable (`__is_mutable__ == False`) 
   or locked (`_locked == True`).
3. **Top-Down Assignment:** For constant nodes or decomposable composites, invokes `randomize_value(...)`.
4. **Bottom-Up Propagation:** Iterates through `instance.meta.inners`, fetching private attributes (`inner.meta.name_private`), 
   and recurses down child nodes to trigger upward reactivity updates across the tree.

## Usage Scenarios
- Automated state fuzzing in unit and integration test suites.
- Filling complex domain models with mock data using scoped `LocalRegistry` instances.
"""