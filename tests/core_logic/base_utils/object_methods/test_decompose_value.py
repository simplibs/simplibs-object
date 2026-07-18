from typing import TYPE_CHECKING, Any
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleObjectProtocol


def decompose_value(
    cls: "SimpleObjectProtocol",
    value: Any
) -> Any:
    """Rozloží hlavní hodnotu na vnitřní komponenty."""

    # 1. Validace předané hodnoty
    cls.validate(value)

    # 2. Rozložení předané hodnoty
    # noinspection PyUnresolvedReferences
    outcome = cls.meta.decompose(cls, value)

    # 3. Navrácení výsledku
    return outcome