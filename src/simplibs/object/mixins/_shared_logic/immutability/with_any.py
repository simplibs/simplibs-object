from typing import Any
from .with_composite import with_composite
from .with_constants import with_constants
from .helpers.with_any import (
    get_top_composite_paths,
    split_constants_paths,
    process_single_change,
    split_changes
)
from .helpers.common import (
    create_new_instance,
    create_snapshot_dict
)


def with_any(
    self,
    changes: tuple[str, Any] | tuple[tuple[str, Any], ...] | None = None
):
    """
    !!! POŽADAVEK NA INTEGRACI !!!
    Tato funkce je navržena pro core pipeline frameworku. Objekt předaný v argumentu
    'instance' MUSÍ dědit z následujících mixinů (nebo implementovat jejich protokoly):
      1. Snapshot (poskytuje metodu _restore_snapshot)
      2. NodesDicts (poskytuje metadata a přístup k uzlům)
    Bez těchto předků pipeline vyhodí AttributeError.
    """

    # 1. Vyřízení pokud není zadaná žádná změna
    if not changes:
        instance = create_new_instance(self, self._build_snapshot())
        return instance if not self.__is_mutable__ else instance.value

    # 2. Základní validace typu
    if not isinstance(changes, tuple):
        raise ...

    # 3. Vyřízení pokud je zadaná jen jedna položka
    if not isinstance(changes[0], tuple):
        changes: tuple[str, Any]
        instance = process_single_change(self, changes)
        return instance if not self.__is_mutable__ else instance.value

    # 4. Roztřídění položek
    changes: tuple[tuple[str, Any], ...]
    constants, composite = split_changes(self, changes)

    # 5. Vyřízení pokud všechny položky jsou konstanty
    if not composite:
        instance = with_constants(self, changes)
        return instance if not self.__is_mutable__ else instance.value

    # 6. Vytvoření slovníku z předaných hodnot (tuple s tuplemi)
    changes_dict = {key: value for key, value in changes}

    # 7. Získání nejnižších kompozic
    top_composite, child_composite = get_top_composite_paths(composite, self._nodes_path_dict)

    # 8. Vytvoření základní instance
    instance = create_new_instance(self, self._build_snapshot())

    # 9. Aplikace root kompozic
    for name in top_composite:
        instance = with_composite(instance, name, changes_dict[name])

    # 10. Snapshot po root kompozicích
    # noinspection PyProtectedMember
    instance_snapshot_dict = create_snapshot_dict(instance._nodes_tuple)

    # 11. Validace child kompozic
    if child_composite:
        for name, value in composite:
            if instance_snapshot_dict[name] != value:
                raise ...

    # 12. Zpracování konstant
    if constants:

        # 12.1 Rozdělení na unique prvky
        contained, unique = split_constants_paths(
            constants,
            top_composite,
            self._nodes_path_dict
        )

        # 12.2 Validace contained konstant
        for name, _ in contained:
            if instance_snapshot_dict[name] != changes_dict[name]:
                raise ...

        # 12.3 Aplikace unique konstant
        new_changes = [(name, changes_dict[name]) for name, _ in unique]
        instance = with_constants(instance, tuple(new_changes))

    # 13. Návrat instance nebo hodnoty (podpora pro implementaci v metodě __call__)
    return instance if not self.__is_mutable__ else instance.value
