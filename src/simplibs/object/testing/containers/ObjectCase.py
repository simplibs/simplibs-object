from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .InnerValue import InnerValue
# Outers
from ..assert_simple_object import assert_simple_object
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols import SimpleClassLike, SimpleMixinLike


@dataclass(slots=True, kw_only=True)
class ObjectCase:
    """Declarative reusable container configuration for testing SimpleObject / SimpleConstant classes.

    Mirrors the parameter signature of ``assert_simple_object``, enabling declarative specification,
    reuse, and batch execution of object test suites across bulk testing setups.

    Attributes:
        test_class: Target object blueprint class under test.
        mixins: Optional tuple of mixin classes to inject into the test class instance.
        test_value_change: Candidate value or ``InnerValue`` payload used to test state changes.
        test_reactivity_up: ``InnerValue`` payload used to verify upward state recalculation.
        test_reactivity_down: Raw composite value used to verify downward decomposition cascades.
        test_mutability: Raw value used to test in-place state mutation preserving object identity.
        test_immutability: Raw value used to test state changes returning new object instances.
    """

    # ------------------------------------------------------------
    # Required Configuration
    # ------------------------------------------------------------
    test_class: "SimpleClassLike"

    # ------------------------------------------------------------
    # Optional Mixins
    # ------------------------------------------------------------
    mixins: tuple["SimpleMixinLike", ...] | UnsetType = UNSET

    # ------------------------------------------------------------
    # Optional Parameter Test Cases
    # ------------------------------------------------------------
    test_value_change: Any | InnerValue | UnsetType = UNSET
    test_reactivity_up: InnerValue | UnsetType = UNSET
    test_reactivity_down: Any | UnsetType = UNSET
    test_mutability: Any | InnerValue | UnsetType = UNSET
    test_immutability: Any | InnerValue | UnsetType = UNSET

    # ------------------------------------------------------------
    # Execution Methods
    # ------------------------------------------------------------
    def run_test(
        self,
        subtests: Any,
        *,
        verbose: bool = True,
        intro: str = "",
        deep_check: bool = True,
    ) -> Any:
        """Executes this object test scenario via the master orchestrator function.

        Args:
            subtests: The native pytest subtests fixture manager instance.
            verbose: Enables isolated pytest subtests reporting across child assertions.
            intro: Optional prefix string added to generated subtest identity names.
            deep_check: Enables deep validation (synthetic mixins & internal methods).

        Returns:
            The created instance with optional mixins applied.
        """
        return assert_simple_object(
            subtests,
            self.test_class,
            mixins=self.mixins,
            test_value_change=self.test_value_change,
            test_reactivity_up=self.test_reactivity_up,
            test_reactivity_down=self.test_reactivity_down,
            test_mutability=self.test_mutability,
            test_immutability=self.test_immutability,
            verbose=verbose,
            intro=intro,
            deep_check=deep_check,
        )


_DESIGN_NOTES = """
# ObjectCase (Declarative Object Test Specification Container)

## Purpose
Acts as a declarative dataclass container wrapping all configurable parameters required to test 
a `SimpleObject` or `SimpleConstant` class. It separates test scenario definitions from test execution, 
enabling reusable test case definitions across test suites.

## Architectural Lifecycle
1. **Definition:** Users instantiate `ObjectCase(test_class=MyObject, test_value_change=42, ...)` as data objects.
2. **Batch Dispatch:** Passed to `bulk_test`, which detects `isinstance(item, ObjectCase)` and delegates execution.
3. **Delegation:** Calls `self.run_test(...)`, unpacking stored parameters into `assert_simple_object(...)`.

## Framework Usage Locations
1. **`bulk_test.py`:** Evaluated in the main dispatch loop (`isinstance(item, ObjectCase)`) to trigger `item.run_test(...)`.
2. **External Test Suites:** Used directly by developers to declare lists of test scenarios for bulk processing.
"""