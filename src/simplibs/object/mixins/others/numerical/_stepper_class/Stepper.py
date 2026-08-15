from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .processors import (
    validate_instance,
    process_value,
    process_up_limit_value,
    process_down_limit_value,
    process_limit_action,
)
from .methods import step_up, step_down, set_value
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.numerical.stepper import StepperProtocol
    from ....._core.protocols.mixins.numerical.stepper.internal_types import StepValue, LimitAction
    from ....._core.protocols.instance import SimpleInstanceLike


class Stepper:
    """
    Service class for controlled numeric value manipulation.

    Provides an encapsulated interface for incrementing, decrementing, and
    enforcing numeric limits on the value of a bound instance.
    """

    __slots__ = (
        "_instance",
        "_step",
        "_up_limit",
        "_down_limit",
        "_up_limit_action",
        "_down_limit_action",
        "_value_type"
    )

    def __init__(
        self: "StepperProtocol",
        instance: "SimpleInstanceLike"
    ) -> None:

        # 1. Validate instance
        validate_instance(instance)

        # 2. Bind instance
        self._instance: "SimpleInstanceLike" = instance

        # 3. Determine numeric type
        self._value_type: type = type(instance.value)

        # 4. Default step value
        self._step: Any = self._value_type(1)

        # 5. Default limits and actions
        self._up_limit: Any = UNSET
        self._down_limit: Any = UNSET
        self._up_limit_action: "LimitAction" = UNSET
        self._down_limit_action: "LimitAction" = UNSET

    # ----------------------------------------
    # Property - getters
    # ----------------------------------------
    @property
    def step(self: "StepperProtocol") -> Any:
        """Step value used for increment/decrement operations."""
        return self._step

    @property
    def up_limit(self: "StepperProtocol") -> Any:
        """Upper limit for the value (or UNSET)."""
        return self._up_limit

    @property
    def down_limit(self: "StepperProtocol") -> Any:
        """Lower limit for the value (or UNSET)."""
        return self._down_limit

    @property
    def up_limit_action(self: "StepperProtocol") -> "LimitAction":
        """Callback executed when the upper limit is exceeded (or UNSET)."""
        return self._up_limit_action

    @property
    def down_limit_action(self: "StepperProtocol") -> "LimitAction":
        """Callback executed when the lower limit is exceeded (or UNSET)."""
        return self._down_limit_action

    # ----------------------------------------
    # Property - setters
    # ----------------------------------------
    @step.setter
    def step(self: "StepperProtocol", value: Any) -> None:
        """Step value used for increment/decrement operations."""
        self._step = process_value(self, value)

    @up_limit.setter
    def up_limit(self: "StepperProtocol", value) -> None:
        """Upper limit for the value (or UNSET)."""
        self._up_limit = process_up_limit_value(self, value)

    @down_limit.setter
    def down_limit(self: "StepperProtocol", value: Any) -> None:
        """Lower limit for the value (or UNSET)."""
        self._down_limit = process_down_limit_value(self, value)

    @up_limit_action.setter
    def up_limit_action(self: "StepperProtocol", value: "LimitAction") -> None:
        """Callback executed when the upper limit is exceeded (or UNSET)."""
        self._up_limit_action = process_limit_action(self, value)

    @down_limit_action.setter
    def down_limit_action(self: "StepperProtocol", value: "LimitAction") -> None:
        """Callback executed when the lower limit is exceeded (or UNSET)."""
        self._down_limit_action = process_limit_action(self, value)

    # ----------------------------------------
    # Methods
    # ----------------------------------------
    def step_up(
        self: "StepperProtocol",
        value: "StepValue" = UNSET,
        *,
        validate: bool = True,
        raise_exception: bool = False
    ) -> Any:
        """Increase the instance value by a step or custom amount."""
        return step_up(self, value, validate=validate, raise_exception=raise_exception)

    def step_down(
        self: "StepperProtocol",
        value: "StepValue" = UNSET,
        *,
        validate: bool = True,
        raise_exception: bool = False
    ) -> Any:
        """Decrease the instance value by a step or custom amount."""
        return step_down(self, value, validate=validate, raise_exception=raise_exception)

    def set_value(
        self: "StepperProtocol",
        value: Any,
        *,
        validate: bool = True,
        raise_exception: bool = False
    ) -> Any:
        """Safely assign a new value with full limit enforcement."""
        return set_value(self, value, validate=validate, raise_exception=raise_exception)

    # ----------------------------------------
    # Dunders
    # ----------------------------------------
    def __repr__(self: "StepperProtocol") -> str:
        """String representation of the Stepper."""
        return f"<Stepper value={self._instance.value!r} step={self._step}>"


_DESIGN_NOTES = """
# Stepper Class

## Purpose
The Stepper is the core controller for safe numeric manipulation inside the
Simple object system. It provides a fully encapsulated interface for:

- incrementing values,
- decrementing values,
- assigning values directly,
- enforcing upper and lower limits,
- executing limit actions,
- normalizing and validating numeric inputs.

It is automatically attached to numerical mixins (`Volume`, `Equalizer`) and
never instantiated directly by the user.

---

## Architectural Role
The Stepper acts as a dedicated numeric engine.  
It integrates with:

- configuration processors (`process_value`, `process_limit_action`, …),
- runtime processors (`verify_up_limit`, `verify_down_limit`),
- stepping methods (`step_up`, `step_down`, `set_value`),
- instance-level validation (`instance.validate`).

It guarantees deterministic, safe, and predictable numeric transitions.

---

## Components

### 1. Initialization
- Validates the bound instance.
- Determines the numeric type.
- Sets default step value.
- Initializes limits and limit actions.

### 2. Properties
- `step` — step size for stepping operations.
- `up_limit` — maximum allowed value.
- `down_limit` — minimum allowed value.
- `up_limit_action` — callback triggered when exceeding upper limit.
- `down_limit_action` — callback triggered when exceeding lower limit.

### 3. Methods
- `step_up(value=UNSET, validate=True, raise_exception=False)`  
  Increases the value by the configured step or a custom amount.  
  Enforces upper limit and triggers actions.

- `step_down(value=UNSET, validate=True, raise_exception=False)`  
  Decreases the value by the configured step or a custom amount.  
  Enforces lower limit and triggers actions.

- `set_value(value, validate=True, raise_exception=False)`  
  Assigns a new value directly.  
  Enforces both limits depending on direction of change.

### 4. Dunders
- `__repr__` — simple debug-friendly representation.

---

## Notes
- Stepper is internal and not part of the public API.
- All heavy logic is delegated to processors and validation helpers.
- The class itself remains minimal, predictable, and easy to reason about.
- Guarantees deterministic behavior across all numeric transitions.
"""