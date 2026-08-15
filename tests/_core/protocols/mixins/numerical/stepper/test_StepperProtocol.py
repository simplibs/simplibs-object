from typing import Protocol, runtime_checkable, Any, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ....instance import SimpleInstanceLike
    from .internal_types import StepValue, LimitAction


@runtime_checkable
class StepperProtocol(
    Protocol
):
    """
    Protocol for the Stepper service class.

    Guarantees an encapsulated interface for incrementing, decrementing, and enforcing
    limit restrictions on numerical values bound to an object instance.
    """

    # --- TECHNICAL ATTRIBUTES (Initialized in __init__) ---
    _instance: "SimpleInstanceLike"
    _value_type: type
    _step: Any
    _up_limit: Any
    _down_limit: Any
    _up_limit_action: "LimitAction"
    _down_limit_action: "LimitAction"

    # --- PROPERTIES (Getters & Setters) ---

    @property
    def step(self) -> Any:
        """Step size by which the value shifts (matches the type of the instance value)."""
        ...

    @step.setter
    def step(self, value: Any) -> None:
        ...

    @property
    def up_limit(self) -> Any:
        """Upper limit beyond which the value cannot rise (or UNSET)."""
        ...

    @up_limit.setter
    def up_limit(self, value: Any) -> None:
        ...

    @property
    def down_limit(self) -> Any:
        """Lower limit below which the value cannot fall (or UNSET)."""
        ...

    @down_limit.setter
    def down_limit(self, value: Any) -> None:
        ...

    @property
    def up_limit_action(self) -> "LimitAction":
        """Callback/Action executed upon exceeding the upper limit (or UNSET)."""
        ...

    @up_limit_action.setter
    def up_limit_action(self, value: "LimitAction") -> None:
        ...

    @property
    def down_limit_action(self) -> "LimitAction":
        """Callback/Action executed upon dropping below the lower limit (or UNSET)."""
        ...

    @down_limit_action.setter
    def down_limit_action(self, value: "LimitAction") -> None:
        ...

    # --- CONTROL AND NAVIGATION METHODS ---

    def step_up(self, value: "StepValue" = ..., *, validate: bool = True, raise_exception: bool = False) -> Any:
        """
        Shifts the bound instance's value upward by the defined step (or specified value).
        Validates configured limits and triggers corresponding actions if threshold reached.
        """
        ...

    def step_down(self, value: "StepValue" = ..., *, validate: bool = True, raise_exception: bool = False) -> Any:
        """
        Shifts the bound instance's value downward by the defined step (or specified value).
        Validates configured limits and triggers corresponding actions if threshold reached.
        """
        ...

    def set_value(self, value: Any, *, validate: bool = True, raise_exception: bool = False) -> Any:
        """
        Safely writes a new value to the instance with full validation of all limits and actions.
        """
        ...