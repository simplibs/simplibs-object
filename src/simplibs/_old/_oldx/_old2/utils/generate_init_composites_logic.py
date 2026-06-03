def generate_init_composites_logic(meta: "SimpleObjectMetadata"):
    """Generuje kód pro inicializaci vnitřních kompozic."""
    lines = []
    for comp_meta in meta.composites_map.values():
        # Tady je ten trik: Kompozice si vytáhne potřebné hodnoty z už existujících slotů
        # Musíme zjistit, jaké parametry ta vnitřní kompozice vyžaduje
        required_consts = comp_meta.constants_map.keys()
        args = ", ".join([f"{name}=self._{name}.value" for name in required_consts])

        # Příklad: self._karoserie = Karoserie.meta.composite_class(barva=self._barva.value)
        line = f"self.{comp_meta.name_private} = {comp_meta.class_name}.meta.composite_class({args})"
        lines.append(line)
    return lines