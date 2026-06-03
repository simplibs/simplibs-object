from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from ...._metadata.SimpleObjectMetadata import SimpleObjectMetadata


class CreateValue:

    meta: 'SimpleObjectMetadata'
    _logic: Any


    @classmethod
    def create_value(cls, **kwargs) -> Any:
        """
        Vytvoří výslednou hodnotu pomocí metody _logic.
        Chybějící parametry doplní z výchozích hodnot vnitřních prvků (inners).
        """
        # 1. Vytvoření slovníku pro hodnoty
        final_args = {}

        # Projdeme parametry, které _logic očekává
        for param_name, info in cls.meta.param_map.items():

            # Hodnota byla předána v kwargs
            if param_name in kwargs:
                final_args[param_name] = kwargs[param_name]

            # Hodnota chybí, vezmeme výchozí hodnotu z metadat daného inner prvku
            else:
                # info["class"] je odkaz na třídu vnitřního prvku
                inner_class = info["class"]
                final_args[param_name] = inner_class.meta.default


        return cls._logic(**final_args)

    @classmethod
    @logic_decorator(cls.meta.inners, cls.meta.value_type)
    def create_value(cls, **kwargs) -> Any:
        """
        Vytvoří výslednou hodnotu pomocí metody _logic.
        """
        return cls._logic(**kwargs)

    @classmethod
    def create_value(cls, **kwargs) -> Any:
        """
        Vytvoří výslednou hodnotu pomocí metody _logic.
        """
        return cls._logic(**kwargs)

    create_value.__signature__ = inspect.Signature(
        parameters=inner.meta.atom_param_signature for inner in cls.metta.inners,
        return_annotation=cls.metta.value_type,
        __validate_parameters__=False
    )