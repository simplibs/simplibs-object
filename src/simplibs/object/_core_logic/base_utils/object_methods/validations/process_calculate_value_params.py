from typing import Any, TYPE_CHECKING
# Anotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleObjectProtocol


def process_calculate_value_params(
    cls: "SimpleObjectProtocol",
    *args,
    **kwargs
) -> dict[str, Any]:

    # 1. Načtení mapy innerů
    inners_map = cls.meta.inners_map

    # 2. Rychlý „guard clause“ na počet pozičních parametrů
    if len(args) > len(inners_map):
        raise ValueError(f"Třída {cls.__name__} očekává maximálně {len(inners_map)} pozičních parametrů, ale bylo zadáno {len(args)}.")

    # 3. Příprava dat
    clean_kwargs = {}
    args_iter = iter(args)

    # 4. Cyklus procházející mapu innerů
    for param_name, inner_cls in inners_map.items():

        # 4.1 Zpracování args
        try:
            value = next(args_iter)
            if param_name in kwargs:
                raise ValueError(f"Parametr '{param_name}' byl zadán jako poziční i pojmenovaný argument zároveň.")

        # 4.2 Zpracování kwargs
        except StopIteration:
            value = kwargs.pop(param_name, None)

        # 4.3 Natažení nezadaných parametrů
        if value is None:
            value = inner_cls.meta.default

        # 4.4 Validace předaných hodnot
        else:
            inner_cls.validate(value)

        # 4.5 Přidání zvalidované hodnoty do slovníku
        clean_kwargs[param_name] = value

    # 5. Kontrola zda v kwarks něco nezbylo
    if kwargs:
        unknown_params = ", ".join(f"'{k}'" for k in kwargs)
        raise ValueError(f"Třída {cls.__name__} neobsahuje parametry: {unknown_params}.")

    # 6. Navrácení slovníku
    return clean_kwargs
