from typing import Any
from simplibs.sentinels import UNSET
from simplibs.exception.testing import maybe_subtest
# Inners
from .containers import ObjectCase, MixinCase
from .assert_simple_object import assert_simple_object
from .assert_simple_mixin import assert_simple_mixin
# Outers
from ..SimpleConstant import SimpleConstant
from ..mixins.base_class import SimpleMixin


# noinspection PyTypeChecker
def bulk_test(
    subtests: Any,
    items: list[Any] | tuple[Any, ...],
    *,
    verbose: bool = True,
    deep_check: bool = True,
) -> None:
    """Unified bulk test runner orchestrating batch execution of object and mixin test cases.

    Iterates over a sequence of test definitions, automatically dispatching each item based on its type:
        - ``ObjectCase``: Executes structured object testing via ``item.run_test``.
        - ``MixinCase``: Executes structured mixin testing via ``item.run_test``.
        - Raw ``SimpleConstant`` class: Invokes ``assert_simple_object`` without mixins.
        - Tuple ``(test_class, mixins)``: Invokes ``assert_simple_object`` with attached mixins.
        - Tuple ``(mixin_class, test_class)``: Invokes ``assert_simple_mixin`` for mixin verification.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        items: Sequence of test case objects, raw class types, or tuple configurations to test.
        verbose: Enables isolated pytest subtests reporting across child assertions.
        deep_check: Enables deep validation (synthetic mixins & internal methods) for object tests.

    Raises:
        AssertionError: If an item in ``items`` does not match any recognized test definition schema.
    """
    for item in items:

        # ------------------------------------------------------------
        # 1. ObjectCase Instance
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
        # 2. MixinCase Instance
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
        # 3. Raw Object Class (SimpleConstant / SimpleObject, no mixins)
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
        # 4. Raw Object Class with Mixins / Mixin with Base Class
        # ------------------------------------------------------------
        if isinstance(item, tuple) and len(item) == 2:

            # 4a. Object Class + Mixin Tuple: (test_class, (mixin_1, mixin_2, ...))
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

            # 4b. Mixin Class + Target Class Tuple: (mixin_class, test_class)
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
        # 5. Unsupported / Unrecognized Test Item Schema
        # ------------------------------------------------------------
        with maybe_subtest(subtests, name="unknown_item", verbose=verbose):
            raise AssertionError(f"Unsupported bulk test item provided to bulk_test: {item!r}")


_DESIGN_NOTES = """
# bulk_test (Batch Test Suite Orchestration Engine)

## Purpose
Acts as a polymorphic batch execution entry point for suite-level testing. It accepts heterogeneous collections 
of test configurations—ranging from fully declarative `ObjectCase` / `MixinCase` instances to quick raw class types 
and tuples—and automatically routes them to the appropriate test orchestrator.

## Dispatch Resolution Pipeline
1. **`ObjectCase` Container:** Directly calls `item.run_test(subtests, ...)`.
2. **`MixinCase` Container:** Directly calls `item.run_test(subtests, ...)`.
3. **Raw Blueprint Class (`type` deriving from `SimpleConstant`):** Automatically wraps and dispatches to `assert_simple_object`.
4. **Tuple Pair Resolution:**
   - **Object + Mixins (`(SimpleConstant, tuple[SimpleMixin, ...])`):** Dispatches to `assert_simple_object(cls, mixins=mixins)`.
   - **Mixin + Base Target (`(SimpleMixin, SimpleConstant)`):** Dispatches to `assert_simple_mixin(mixin_class, test_class=test_class)`.
5. **Fallback / Invalid Item Intercept:** Raises an `AssertionError` wrapped in a subtest context when an invalid 
   item schema is encountered.

## Pipeline Lifecycle Role
Provides a lightweight, zero-boilerplate batch testing runner for test suites, allowing entire packages of objects 
and mixins to be validated in a single pytest test function call.
"""