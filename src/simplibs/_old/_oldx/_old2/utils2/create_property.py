def create_property(value, value_tyoe, normalize_method):


    # 3. Definice geteru
    def getter(self) -> Any:
        return self._value

    # 4. Definice setteru
    def setter(self, new_value: Any) -> None:
        old_value = self._value
        new_normalized = self.normalize(new_value, process_none=True)

        if old_value != new_normalized:
            self._value = new_normalized
            self._on_update()

    return property(getter, setter)