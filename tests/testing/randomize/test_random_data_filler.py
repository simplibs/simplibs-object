from typing import TYPE_CHECKING
from simplibs.randomize import LocalRegistry, RegistryBase
from .randomize_constant import randomize_constant
from .randomize_object import randomize_object
from ....SimpleConstant import SimpleConstant
from .randomize_value import randomize_value

if TYPE_CHECKING:
    from ...._core_logic._core.protocols.instance import SimpleInstanceLike


# noinspection PyProtectedMember
def random_data_filler(
    instance: "SimpleInstanceLike",
    *,
    retries: int = 5,
    registry: RegistryBase | None = None,
    skip_unregistered: bool = False,
    skip_immutable: bool = True,
    validate: bool = True
) -> "SimpleInstanceLike":
    """Recursively fuzz-fills a Simple instance tree with random, valid values.

    For constant leaves, generates a random value matching the declared type
    (via simplibs-randomize) and attempts assignment, retrying on validation
    failure. For composite nodes, additionally attempts a direct top-down
    assignment when the node supports decomposition, and always recurses
    into inners to exercise bottom-up propagation.

    Args:
        instance: The Simple instance (constant or composite) to fill.
        retries: Maximum generation attempts per single assignment.
        registry: Optional LocalRegistry providing scoped custom randomizers,
            without touching the global RANDOMIZERS singleton.
        skip_immutable: If True, locked (immutable) nodes are left untouched.

    Returns:
        The same instance, mutated in place.
    """

    # 1. Validace
    if validate and not(
        isinstance(instance, SimpleConstant)
        and isinstance(retries, int) and retries > 0
        and (registry is None or isinstance(registry, RegistryBase))
        and isinstance(skip_unregistered, bool)
        and isinstance(skip_immutable, bool)
    ):
        validate_instance_is_simple_constant_base()
        validate_retries_is_int()
        validate_retries_is_greater_than_zero()
        validate_registry_is_randomize_registry_base()
        validate_skip_unregistered_is_bool()
        validate_skip_immutable_is_bool()

    # 2. Přeskočení immutable instancí
    instance: "SimpleInstanceLike"
    if skip_immutable and (
        not instance.__is_mutable__
        or instance._locked
    ):
        return instance

    # 3. Zpacování konstanty a dekomposebilní kompozice
    if instance.meta.is_constant or instance.meta.is_decomposeable:
        randomize_value(
            instance,
            retries=retries,
            registry=registry,
            validate=False
        )

    # 4. Změna kompozice přes její vnitřní prvky
    for inner in instance.meta.inners:

        # 4.1 Získání instance vnitřního prvku
        inner_instance = getattr(instance, inner.meta.name_private)

        # 4.2 Rekurzivní volání pro vyřízení vnitnřího prvku
        random_data_filler(
            inner_instance,
            retries=retries,
            registry=registry,
            skip_immutable=skip_immutable
        )

    # 4. Navrácení instance
    return instance


"""
**Použití:**
```python
from simplibs.testing.utils.fuzz import random_data_filler

person = Person()
random_data_filler(person)  # fuzzuje celý strom, global RANDOMIZERS

# nebo se scoped custom generátorem, bez zásahu do globálu
from simplibs.randomize.registry.classes import LocalRegistry

with LocalRegistry() as reg:
    reg.add(MyDomainEnum, lambda: random.choice(list(MyDomainEnum)))
    random_data_filler(person, registry=reg)
```

"""