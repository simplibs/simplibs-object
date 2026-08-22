from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols import SimpleClassType, SimpleMixinType


@dataclass(slots=True, kw_only=True)
class MixinCase:
    """Declarative reusable container configuration for testing Simple mixins.

    Mirrors the parameter structure of ``assert_simple_mixin``, enabling declarative specification,
    reuse, and batch execution of mixin test scenarios across bulk testing setups.

    Attributes:
        mixin_class: Target mixin blueprint class under test.
        test_class: Target base object class used to bind and instantiate the mixin.
        slots_names: Optional tuple of expected slot string identifiers to check for presence.
        slots_values: Optional tuple of single or multiple ``(slot_name, expected_value)`` pairs.
        attribute_names: Optional tuple of expected attribute identifiers to check for presence.
        method_names: Optional tuple of expected method identifiers to check for presence.
    """

    # ------------------------------------------------------------
    # Required Configuration
    # ------------------------------------------------------------
    mixin_class: "SimpleMixinType"
    test_class: "SimpleClassType"

    # ------------------------------------------------------------
    # Optional Parameter Test Cases
    # ------------------------------------------------------------
    slots_names: tuple[str, ...] | UnsetType = UNSET
    slots_values: tuple[tuple[str, Any], ...] | tuple[str, Any] | UnsetType = UNSET
    attribute_names: tuple[str, ...] | UnsetType = UNSET
    method_names: tuple[str, ...] | UnsetType = UNSET

    # ------------------------------------------------------------
    # Execution Methods
    # ------------------------------------------------------------
    def run_test(
        self,
        subtests: Any,
        *,
        verbose: bool = True,
        intro: str = "",
    ) -> Any:
        """Executes this mixin test scenario via the master orchestrator function.

        Args:
            subtests: The native pytest subtests fixture manager instance.
            verbose: Enables isolated pytest subtests reporting across child assertions.
            intro: Optional prefix string added to generated subtest identity names.

        Returns:
            The created instance with the target mixin applied.
        """
        from ..assert_simple_mixin import assert_simple_mixin
        return assert_simple_mixin(
            subtests,
            self.mixin_class,
            test_class=self.test_class,
            slots_names=self.slots_names,
            slots_values=self.slots_values,
            attribute_names=self.attribute_names,
            method_names=self.method_names,
            verbose=verbose,
            intro=intro,
        )


_DESIGN_NOTES = """
# MixinCase (Declarative Mixin Test Specification Container)

## Purpose
Acts as a declarative dataclass container wrapping all configurable parameters required to test 
a `SimpleMixin` subclass. It separates mixin test definitions from execution, allowing mixin scenarios 
to be constructed as data structures and run in batch suites.

## Architectural Lifecycle
1. **Definition:** Users instantiate `MixinCase(mixin_class=MyMixin, test_class=MyObject, ...)` as data objects.
2. **Batch Dispatch:** Passed to `bulk_test`, which detects `isinstance(item, MixinCase)` and delegates execution.
3. **Delegation:** Calls `self.run_test(...)`, unpacking stored parameters into `assert_simple_mixin(...)`.

## Framework Usage Locations
1. **`bulk_test.py`:** Evaluated in the main dispatch loop (`isinstance(item, MixinCase)`) to trigger `item.run_test(...)`.
2. **External Test Suites:** Used directly by developers to declare lists of mixin test scenarios for bulk processing.
"""