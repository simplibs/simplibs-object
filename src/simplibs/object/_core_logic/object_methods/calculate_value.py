from typing import TYPE_CHECKING, Any
#Inners
from .validations import process_calculate_value_params
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleObjectProtocol


def calculate_value(
    cls: "SimpleObjectProtocol",
    *args,
    **kwargs
) -> Any:
    """
    Dynamicky spočítá hodnotu kompozice.
    Díky ParamSpec PyCharm nahlédne do uživatelské metody '_logic'
    a začne vývojáři našeptávat JEJÍ konkrétní parametry!
    """

    # 1. Zpracování předaných parametrů
    params_dict = process_calculate_value_params(cls, *args, **kwargs)

    # 2. Výpočet hodnoty
    outcome = cls.meta.logic(cls, **params_dict)

    # 3. Navrácení výsledku
    return outcome