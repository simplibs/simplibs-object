from typing import TYPE_CHECKING
from simplibs.randomize import randomize, RandomizeError
from simplibs.randomize.registry.classes import LocalRegistry

if TYPE_CHECKING:
    from ....._core.protocols.instance import SimpleInstanceLike


def randomize_value(
    instance: "SimpleInstanceLike",
    *,
    retries: int,
    registry: LocalRegistry | None,
    skip_unregistered: bool = False,
    validate: bool = True
) -> "SimpleInstanceLike":
    """Generates and assigns a random valid value to a single constant leaf."""

    # 1. Validace
    if validate and not (
        isinstance(instance, SimpleConstant)
        and isinstance(retries, int) and retries > 0
        and (registry is None or isinstance(registry, RegistryBase))
        and isinstance(skip_unregistered, bool)
    ):
        validate_instance_is_simple_constant_base()
        validate_retries_is_int()
        validate_retries_is_greater_than_zero()
        validate_registry_is_randomize_registry_base()
        validate_skip_unregistered_is_bool()

    # 2. Načtení randomizéru
    value_randomizer = registry.randomize if registry else randomize

    # 3. Randomizace dle počtu pokusů
    for _ in range(retries):

        # 3.1 Získání nové hodnoty
        try:
            value_type = instance.meta.value_type
            new_value = value_randomizer(value_type)
        except RandomizeError:
            if skip_unregistered:
                return instance
            raise

        # 3.2 Ověření, že není totožná s aktuální
        if new_value == instance.value:
            continue

        # 3.3 Přiřazení hodnoty (setter/validace)
        # noinspection PyBroadException
        try:
            instance.value = new_value
            return instance

        # 3.4 Zpracování výjimky validace na setteru (další pokus)
        except Exception:
            continue

    # 4. Výjimka, když se vyčerpají pokusy
    raise_random_data_filler_exhausted(instance, retries)