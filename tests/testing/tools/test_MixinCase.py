from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ..assert_simple_mixin import assert_simple_mixin
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols import SimpleClassType, SimpleMixinType


@dataclass(slots=True, kw_only=True)
class MixinCase:
    """
    Declarative reusable container for testing Simple mixins.

    Mirrors the parameter structure of `assert_simple_mixin` and allows
    bulk execution of mixin tests in a unified, predictable way.
    """

    # ------------------------------------------------------------
    # Required
    # ------------------------------------------------------------
    mixin_class: "SimpleMixinType"
    test_class: "SimpleClassType"

    # ------------------------------------------------------------
    # Optional parameter tests
    # ------------------------------------------------------------
    slots_names: tuple[str, ...] | UnsetType = UNSET
    slots_values: tuple[tuple[str, Any], ...] | tuple[str, Any] | UnsetType = UNSET
    attribute_names: tuple[str, ...] | UnsetType = UNSET
    method_names: tuple[str, ...] | UnsetType = UNSET

    # ------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------
    def run_test(
        self,
        subtests: Any,
        *,
        verbose: bool = True,
        intro: str = "",
    ) -> Any:
        """
        Execute this mixin test scenario using the main orchestrator.

        Returns:
            The created instance (with mixin applied).
        """

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
