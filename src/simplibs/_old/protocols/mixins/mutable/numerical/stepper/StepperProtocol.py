from typing import Protocol, runtime_checkable, Any
# Outers
from .....types import SimpleInstanceType


@runtime_checkable
class StepperProtocol(Protocol):
    """
    Protokol pro servisní třídu Stepper.

    Garantuje zapouzdřené rozhraní pro inkrementaci, dekrementaci a hlídání
    limitů číselných hodnot nad navázanou instancí objektu.
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v __init__) ---
    _instance: SimpleInstanceType
    _value_type: type
    _step: Any
    _up_limit: Any
    _down_limit: Any
    _up_limit_action: Any
    _down_limit_action: Any

    # --- PROPERTIES (Getters & Setters) ---

    @property
    def step(self) -> Any:
        """Krok, o který se hodnota posouvá (shodný s typem hodnoty instance)."""
        ...

    @step.setter
    def step(self, value: Any) -> None:
        ...

    @property
    def up_limit(self) -> Any:
        """Horní limit, za který hodnota nesmí stoupnout (nebo UNSET)."""
        ...

    @up_limit.setter
    def up_limit(self, value: Any) -> None:
        ...

    @property
    def down_limit(self) -> Any:
        """Spodní limit, pod který hodnota nesmí klesnout (nebo UNSET)."""
        ...

    @down_limit.setter
    def down_limit(self, value: Any) -> None:
        ...

    @property
    def up_limit_action(self) -> Any:
        """Callback/Akce spuštěná při překročení horního limitu (nebo UNSET)."""
        ...

    @up_limit_action.setter
    def up_limit_action(self, value: Any) -> None:
        ...

    @property
    def down_limit_action(self) -> Any:
        """Callback/Akce spuštěná při překročení spodního limitu (nebo UNSET)."""
        ...

    @down_limit_action.setter
    def down_limit_action(self, value: Any) -> None:
        ...

    # --- KONTROLNÍ A NAVIGAČNÍ METODY ---

    def step_up(self, value: Any = ..., *, validate: bool = True, raise_exception: bool = False) -> Any:
        """
        Posune hodnotu navázané instance směrem nahoru o definovaný krok (nebo zadanou hodnotu).
        Kontroluje nastavené limity a spouští případné akce.
        """
        ...

    def step_down(self, value: Any = ..., *, validate: bool = True, raise_exception: bool = False) -> Any:
        """
        Posune hodnotu navázané instance směrem dolů o definovaný krok (nebo zadanou hodnotu).
        Kontroluje nastavené limity a spouští případné akce.
        """
        ...

    def set_value(self, value: Any, *, validate: bool = True, raise_exception: bool = False) -> Any:
        """
        Bezpečně zapíše novou hodnotu do instance s plnou kontrolou všech limitů a akcí.
        """
        ...