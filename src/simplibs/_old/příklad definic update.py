def _on_update(self):
    # 1. Přepočítám vlastní hodnotu pomocí _logic
    # Vstupy bere z vnitřních instancí, které už v sobě mají aktuální data
    self._value = self._logic(*(attr.value for attr in self._inners))

    # 2. Informuji rodiče (pokud existuje), že jsem se změnil
    if hasattr(self, '_parent') and self._parent:
        self._parent._on_update()