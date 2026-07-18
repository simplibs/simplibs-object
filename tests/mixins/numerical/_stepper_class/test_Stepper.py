from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .validations import (
    validate_instance,
    process_value,
    process_up_limit_value,
    process_down_limit_value,
    process_limit_action,
)
from .methods import step_up, step_down, set_value
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.numerical.stepper import StepperProtocol
    from ....protocols.mixins.numerical.stepper.internal_types import StepValue, LimitAction
    from ....protocols.instance import SimpleInstanceLike


class Stepper:
    """
    Servisní třída Stepper pro změnu numerické hodnoty.

    Garantuje zapouzdřené rozhraní pro inkrementaci, dekrementaci a hlídání
    limitů číselných hodnot nad navázanou instancí objektu.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = (
        "_instance",
        "_step",
        "_up_limit",
        "_down_limit",
        "_up_limit_action",
        "_down_limit_action",
        "_value_type"
    )

    # ----------------------------------------
    # Inicializace třídy
    # ----------------------------------------

    def __init__(
        self: "StepperProtocol",
        instance: "SimpleInstanceLike"
    ) -> None:

        # 1. Validace instance
        validate_instance(instance)

        # 2. Přiřazení instance
        self._instance: "SimpleInstanceLike" = instance

        # 3. Výpočet typu
        self._value_type: type = type(instance.value)

        # 4. Definice hodnoty pro step
        self._step: Any = self._value_type(1)

        # 5. Definice limitérů
        self._up_limit: Any = UNSET
        self._down_limit: Any = UNSET
        self._up_limit_action: "LimitAction" = UNSET
        self._down_limit_action: "LimitAction" = UNSET

    # ----------------------------------------
    # Property - getters
    # ----------------------------------------
    @property
    def step(
        self: "StepperProtocol"
    ) -> Any:
        """Krok, o který se hodnota posouvá (shodný s typem hodnoty instance)."""
        return self._step

    @property
    def up_limit(
        self: "StepperProtocol"
    ) -> Any:
        """Horní limit, za který hodnota nesmí stoupnout (nebo UNSET)."""
        return self._up_limit

    @property
    def down_limit(
        self: "StepperProtocol"
    ):
        """Spodní limit, pod který hodnota nesmí klesnout (nebo UNSET)."""
        return self._down_limit

    @property
    def up_limit_action(
        self: "StepperProtocol"
    ) -> "LimitAction":
        """Callback/Akce spuštěná při překročení horního limitu (nebo UNSET)."""
        return self._up_limit_action

    @property
    def down_limit_action(
        self: "StepperProtocol"
    ) -> "LimitAction":
        """Callback/Akce spuštěná při překročení spodního limitu (nebo UNSET)."""
        return self._down_limit_action

    # ----------------------------------------
    # Property - setters
    # ----------------------------------------
    @step.setter
    def step(
        self: "StepperProtocol",
        value: Any
    ) -> None:
        """Krok, o který se hodnota posouvá (shodný s typem hodnoty instance)."""
        self._step = process_value(self, value)

    @up_limit.setter
    def up_limit(
        self: "StepperProtocol",
        value
    ):
        """Horní limit, za který hodnota nesmí stoupnout (nebo UNSET)."""
        self._up_limit = process_up_limit_value(self, value)

    @down_limit.setter
    def down_limit(
        self: "StepperProtocol",
        value: Any
    ) -> None:
        """Spodní limit, pod který hodnota nesmí klesnout (nebo UNSET)."""
        self._down_limit = process_down_limit_value(self, value)

    @up_limit_action.setter
    def up_limit_action(
        self: "StepperProtocol",
        value: "LimitAction"
    ) -> None:
        """Callback/Akce spuštěná při překročení horního limitu (nebo UNSET)."""
        self._up_limit_action = process_limit_action(self, value)

    @down_limit_action.setter
    def down_limit_action(
        self: "StepperProtocol",
        value: "LimitAction"
    ) -> None:
        """Callback/Akce spuštěná při překročení spodního limitu (nebo UNSET)."""
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
        """
        Posune hodnotu navázané instance směrem nahoru o definovaný krok (nebo zadanou hodnotu).
        Kontroluje nastavené limity a spouští případné akce.
        """
        return step_up(self, value, validate=validate, raise_exception=raise_exception)

    def step_down(
        self: "StepperProtocol",
        value: "StepValue" = UNSET,
        *,
        validate: bool = True,
        raise_exception: bool = False
    ) -> Any:
        """
        Posune hodnotu navázané instance směrem dolů o definovaný krok (nebo zadanou hodnotu).
        Kontroluje nastavené limity a spouští případné akce.
        """
        return step_down(self, value, validate=validate, raise_exception=raise_exception)

    def set_value(
        self: "StepperProtocol",
        value: Any,
        *,
        validate: bool = True,
        raise_exception: bool = False
    ) -> Any:
        """
        Bezpečně zapíše novou hodnotu do instance s plnou kontrolou všech limitů a akcí.
        """
        return set_value(self, value, validate=validate, raise_exception=raise_exception)

    # ----------------------------------------
    # Dunders
    # ----------------------------------------

    def __repr__(
        self: "StepperProtocol"
    ) -> str:
        """Textová reprezentace objektu"""
        return f"<Stepper value={self._instance.value!r} step={self._step}>"
