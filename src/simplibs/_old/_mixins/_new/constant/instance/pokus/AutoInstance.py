# class_name: AutoInstance
# class_parents: (InstanceBase,)
class AutoInstance(InstanceBase):
    __slots__ = ("_auto_core",)  # cls.meta.name_private

    def __init__(self, **kwargs):
        # 1. Vytáhneme hodnotu z kwargs pod jménem 'auto' (cls.meta.name_snake)
        value = kwargs.get("auto")

        # 2. Zapouzdříme ji do jádra
        self._auto_core = AutoCore(value)

        # 3. MRO řetězec pro kompozice
        super().__init__(**kwargs)

    @property
    def auto(self):  # Jméno vlastnosti je cls.meta.name_snake
        """Vrací celý objekt CORE (jádro)."""
        return self._auto_core

    @auto.setter
    def auto(self, value):
        """Zapíše hodnotu do jádra (přes jeho .value setter)."""
        self._auto_core.value = value

        # Automatický hook pro aktualizaci (ekvalizér)
        if hasattr(self, '_on_update'):
            self._on_update()