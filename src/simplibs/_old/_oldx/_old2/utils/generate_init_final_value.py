def generate_init_final_value(meta: "SimpleObjectMetadata"):
    """Generuje finální výpočet hodnoty kompozice."""
    # Získáme jména všech inners pro volání _logic
    inner_values = [f"self.{m.name_private}.value" for m in meta.inners.values()]
    args_str = ", ".join(inner_values)

    return [
        f"# Výpočet vlastní hodnoty skrze _logic",
        f"self._value = self._logic({args_str})",
        f"self._on_update()"
    ]