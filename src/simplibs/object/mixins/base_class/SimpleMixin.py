# Inners
from .validations import verify_mixin_definition


class SimpleMixin:

    # 1. Definice sltu
    __slots__ = ()

    # 2. Flag zda je možné mixin použít i pro konstantu
    _composite_only: bool = False

    # 3. Definice pomocné metody pro mixiny skrze kterou mají přístup do initu třídy
    def init_mixins(self) -> None:
        """Výchozí prázdná kotva pro reaktivní inicializaci mixinů."""
        # noinspection PyUnresolvedReferences
        super().init_mixins()

    # 4. Definice metody pro kontrolu zapsaných dat
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        verify_mixin_definition(cls)

