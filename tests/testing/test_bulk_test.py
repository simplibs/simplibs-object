from typing import Any
from simplibs.sentinels import UNSET
from simplibs.exception.testing import maybe_subtest

# Case třídy
from .ObjectCase import ObjectCase
from .MixinCase import MixinCase

# Orchestrátory
from ..assert_simple_object import assert_simple_object
from ..assert_simple_mixin import assert_simple_mixin

# Typy
from ..._core.protocols import SimpleClassLike, SimpleMixinLike

from ....SimpleConstant import SimpleConstant
from ....mixins.base_class import SimpleMixin


def bulk_test(
    subtests: Any,
    items: list[Any],
    *,
    verbose: bool = True,
    deep_check: bool = True,
) -> None:
    """
    Unified bulk test runner for SimpleObject and SimpleMixin tests.

    Supports:
        - ObjectCase
        - MixinCase
        - raw object class
        - raw (object_class, mixins)
        - raw (mixin_class, test_class)

    Args:
        subtests: pytest subtests fixture
        items: list of test definitions
        verbose: enable verbose subtests
        deep_check: deep validation for object tests
    """

    for item in items:

        # ------------------------------------------------------------
        # 1) ObjectCase
        # ------------------------------------------------------------
        if isinstance(item, ObjectCase):
            intro = f"object_{item.test_class.__name__}::"
            item.run_test(
                subtests,
                verbose=verbose,
                intro=intro,
                deep_check=deep_check,
            )
            continue

        # ------------------------------------------------------------
        # 2) MixinCase
        # ------------------------------------------------------------
        if isinstance(item, MixinCase):
            intro = f"mixin_{item.mixin_class.__name__}::"
            item.run_test(
                subtests,
                verbose=verbose,
                intro=intro,
            )
            continue

        # ------------------------------------------------------------
        # 3) Raw object class (no mixins)
        # ------------------------------------------------------------
        if isinstance(item, type) and issubclass(item, SimpleConstant):
            cls = item
            intro = f"object_{cls.__name__}::"
            assert_simple_object(
                subtests,
                cls,
                mixins=UNSET,
                verbose=verbose,
                intro=intro,
                deep_check=deep_check,
            )
            continue

        # ------------------------------------------------------------
        # 4) Raw object class with mixins
        # ------------------------------------------------------------
        if isinstance(item, tuple) and len(item) == 2:

            cls, mixins = item
            if (
                isinstance(cls, type)
                and issubclass(cls, SimpleConstant)
                and isinstance(mixins, tuple)
                and all(issubclass(mixin, SimpleMixin) for mixin in mixins)
            ):
                intro = f"object_{cls.__name__}::"
                assert_simple_object(
                    subtests,
                    cls,
                    mixins=mixins,
                    verbose=verbose,
                    intro=intro,
                    deep_check=deep_check,
                )
                continue

        # ------------------------------------------------------------
        # 5) Raw mixin test (mixin_class, test_class)
        # ------------------------------------------------------------

            mixin_class, test_class = item
            if (
                isinstance(mixin_class, type)
                and issubclass(mixin_class, SimpleMixin)
                and isinstance(test_class, type)
                and issubclass(test_class, SimpleConstant)
            ):
                intro = f"mixin_{mixin_class.__name__}::"
                assert_simple_mixin(
                    subtests,
                    mixin_class,
                    test_class=test_class,
                    verbose=verbose,
                    intro=intro,
                )
                continue

        # ------------------------------------------------------------
        # 6) Unknown item
        # ------------------------------------------------------------
        with maybe_subtest(subtests, name="unknown_item", verbose=verbose):
            raise AssertionError(f"Unsupported bulk test item: {item!r}")
