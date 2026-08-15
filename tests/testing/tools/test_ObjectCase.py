from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ..assert_simple_object import assert_simple_object
from ..tools.InnerValue import InnerValue
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols import SimpleClassLike, SimpleMixinLike


@dataclass(slots=True, kw_only=True)
class ObjectCase:
    """
    Declarative reusable container for testing SimpleObject / SimpleConstant classes.

    Mirrors the parameter structure of `assert_simple_object` and allows
    bulk execution of object tests in a unified, predictable way.
    """

    # ------------------------------------------------------------
    # Required
    # ------------------------------------------------------------
    test_class: "SimpleClassLike"

    # ------------------------------------------------------------
    # Optional mixins
    # ------------------------------------------------------------
    mixins: tuple["SimpleMixinLike", ...] | UnsetType = UNSET

    # ------------------------------------------------------------
    # Optional parameter tests
    # ------------------------------------------------------------
    test_value_change: Any | InnerValue | UnsetType = UNSET
    test_reactivity_up: InnerValue | UnsetType = UNSET
    test_reactivity_down: Any | UnsetType = UNSET
    test_mutability: Any | InnerValue | UnsetType = UNSET
    test_immutability: Any | InnerValue | UnsetType = UNSET

    # ------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------
    def run_test(
        self,
        subtests: Any,
        *,
        verbose: bool = True,
        intro: str = "",
        deep_check: bool = True,
    ) -> Any:
        """
        Execute this object test scenario using the main orchestrator.

        Returns:
            The created instance (with mixins applied if provided).
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
