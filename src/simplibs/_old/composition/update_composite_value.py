# Metoda na kompozici pro aktualizaci zdola
def _recalculate_composite_value(self) -> None:
    # 1. Sběr aktuálních hodnot z inners instancí
    # (Tento krok se vygeneruje dynamicky pro každou třídu)
    current_params = {
        inner_meta.name_snake: getattr(self, inner_meta.name_private).value
        for inner_meta in self.meta.inners
    }

    # 2. Výpočet nové vlastní hodnoty
    new_value = self.calculate_value(**current_params)

    # 3. Pokud došlo ke změně, uložíme ji a pošleme update výše
    if self._value != new_value:
        self._value = new_value

        # Pokud máme rodiče (jsme sami vnořeni v jiné kompozici),
        # dáme mu vědět, ať se také aktualizuje
        if self._owner is not None:
            self._owner.recalculate_composite_value()