from typing import Union
from simplibs.sentinels import UNSET
# Inners
from .validations import verify_mixin_definition


class SimpleMixin:

    # 1. Deklarativní omezení
    _constant_only = False
    _composite_only = False
    _mutable_only = False
    _immutable_only = False
    _only_types: type | Union = UNSET

    # 2. Definice sltu
    __slots__ = ()

    # 3. Definice pomocné metody pro mixiny skrze kterou mají přístup do initu třídy
    def init_mixins(self) -> None:
        """Výchozí prázdná kotva pro reaktivní inicializaci mixinů."""
        # noinspection PyUnresolvedReferences
        super().init_mixins()

    # 4. Definice metody pro kontrolu zapsaných dat
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        verify_mixin_definition(cls)

