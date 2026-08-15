from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .asserts.mixins import (
    assert_mixin_inheritance,
    assert_mixin_instance_creation,
    assert_instance_hasattr,
    assert_mixins_slots_values
)
# Annotations
if TYPE_CHECKING:
    from .._core.protocols import SimpleClassType, SimpleMixinType


def assert_simple_mixin(
    subtests,
    mixin_class: "SimpleMixinType",
    *,
    test_class: "SimpleClassType",
    slots_names: tuple[str, ...] | UnsetType = UNSET,
    slots_values: tuple[tuple[str, Any], ...] | tuple[str, Any] | UnsetType = UNSET,
    attribute_names: tuple[str, ...] | UnsetType = UNSET,
    method_names: tuple[str, ...] | UnsetType = UNSET,
    verbose: bool = True,
    intro: str = "",
):

    # ------------------------------------------------------------
    # SHALLOW TESTS — základní test
    # ------------------------------------------------------------

    # 1. Test dědičnosti mixinu ze SimpleMixin
    assert_mixin_inheritance(
        subtests,
        mixin_class,
        verbose=verbose,
        intro=intro
    )

    # 2. Test inicializace mixinu na uživatelem dodané třídě
    instance = assert_mixin_instance_creation(
        subtests,
        test_class,
        mixin_class,
        verbose=verbose,
        intro=intro
    )

    # ------------------------------------------------------------
    # PARAMETER TESTS — volitelné testy podle uživatele
    # ------------------------------------------------------------

    # 3. Test přítomnosti slotů
    if slots_names is not UNSET:
        slots_names: tuple[str, ...]
        assert_instance_hasattr(
            subtests,
            instance,
            names=slots_names,
            kind="slot",
            verbose=verbose,
            intro=intro
        )

    # 4. Test hodnot slotů
    if slots_values is not UNSET:
        assert_mixins_slots_values(
            subtests,
            instance,
            slots_values=slots_values,
            verbose=verbose,
            intro=intro
        )

    # 5. Test přítomnosti atributů
    if attribute_names is not UNSET:
        attribute_names: tuple[str, ...]
        assert_instance_hasattr(
            subtests,
            instance,
            names=attribute_names,
            kind="attribute",
            verbose=verbose,
            intro=intro
        )

    # 6. Test přítomnosti metod
    if method_names is not UNSET:
        method_names: tuple[str, ...]
        assert_instance_hasattr(
            subtests,
            instance,
            names=method_names,
            kind="method",
            verbose=verbose,
            intro=intro
        )

    # 7. Vrátíme instanci pro případné další testy uživatele
    return instance
