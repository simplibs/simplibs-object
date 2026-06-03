def generate_init_constants_logic(meta: "SimpleObjectMetadata"):
    """Generuje kód pro inicializaci instancí konstant."""
    lines = []
    for name_snake, const_meta in meta.constants_map.items():
        # Příklad: self._cena = Cena.meta.atom_class(cena)
        # Používáme atom_class, aby proběhla normalizace a validace
        line = f"self.{const_meta.name_private} = {const_meta.class_name}.meta.atom_class({name_snake})"
        lines.append(line)
    return lines