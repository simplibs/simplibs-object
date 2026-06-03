from typing import Any
from ..core.Metadata import MetadataMixin

# introspection/Documentation.py
class DocumentationMixin(MetadataMixin):
    """
    Runtime dokumentace objektu.

    Příklad:
        print(obj.help())
    """
    __slots__ = ()
    value: Any

    """
    Analýza kódu DocumentationMixin
    Kód je napsán přehledně, ale narazil jsem na jednu potenciální past při rekurzi:
    
    inner_val = getattr(self, inner.name_snake).value
    Kritický postřeh:
    Tady opět narážíme na to, zda je vnitřní prvek už "objekt s mixiny", nebo jen "atom". Pokud by někdo použil SimpleObject v režimu as_atom=True (tedy bez mixinů, jen čistý Atom), tak getattr(self, inner.name_snake) vrátí objekt Atom. Ten sice .value má, ale co když je to jen jednoduchá hodnota po dekompozici?
    
    Bezpečnější zápis:
    
    # Získáme vnitřní instanci (Atom nebo SimpleObject)
    inner_instance = getattr(self, inner.name_snake)
    
    # Získáme hodnotu bezpečně
    if hasattr(inner_instance, "value"):
        inner_val = inner_instance.value
    else:
        inner_val = inner_instance 
    Návrh na vylepšení: "Smart Help"
    Když už děláš runtime dokumentaci, co takhle ji udělat ještě užitečnější? SimpleObject ví, jestli je validní!
    
    Python
    
        def help(self) -> str:
            meta = self.meta
            # Přidáme informaci o validitě
            valid_status = "OK" if not hasattr(self, 'is_valid') else ("Validní" if self.is_valid() else "INVALIDNÍ")
            
            lines = [
                f"OBJEKT:  {self.__class__.__name__} [{valid_status}]",
                f"POPIS:   {meta.name_readable}",
                # ... zbytek kódu
            ]
    """

    def help(self) -> str:
        """Vrátí textový popis objektu a jeho struktury."""
        meta = self.meta
        lines = [
            f"OBJEKT: {self.__class__.__name__}",
            f"POPIS:  {meta.name_readable}",
            f"TYP:    {meta.value_type.__name__}",
            f"HODNOTA: {self.value}",
            f"DEFAULT: {meta.default}",
            "---"
        ]

        if meta.inners:
            lines.append("VNITŘNÍ PRVKY:")
            for inner in meta.inners:
                inner_val = getattr(self, inner.name_snake).value
                lines.append(f"  - {inner.name_snake}: {inner_val} ({inner.meta.value_type.__name__})")

        return "\n".join(lines)

