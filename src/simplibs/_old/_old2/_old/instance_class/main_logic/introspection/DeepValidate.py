from typing import Dict, List

from ..core.Validate import ValidateMixin
from ..core.Metadata import MetadataMixin

class DeepValidateMixin(ValidateMixin, MetadataMixin):
    """
    Hloubková validace včetně všech inners (rekurzivně).

    Příklad:
        errors = obj.validate_all()
        if errors:
            print("Chyby:", errors)
    """
    __slots__ = ()

    """
    Podněty k vylepšení (Logika rekurze)
    Mám jeden technický postřeh k této části:

    inner_instance = getattr(self, inner.name_snake)
    
    Problém:
    Tento řádek předpokládá, že inner_instance je už hotový objekt (včetně mixinů). Ale my víme, že v tvé architektuře inner v metadatech je třída (SimpleBase), zatímco inner_instance v instanci je Atom/Core (to, co vrací getattr(self, inner.name_snake)).
    
    Aby rekurze fungovala (tedy aby inner_instance měl metodu validate_all), musí být ten vnitřní prvek sám o sobě instancí SimpleObject, která tento mixin obsahuje.
    
    Doporučení pro robustnost:
    Pokud by náhodou inner_instance byl jen "hloupý" Atom (který nemá mixiny), rekurze by selhala. V tvém aktuálním návrhu se to ale pravděpodobně nestane, protože SimpleObject skládá vše dohromady.
    
    Jedna drobná oprava v try-except:
    V části else (pokud inner nemá validate_all) voláš:
    
    inner.validate(inner_instance.value)
    
    Zde pozor – inner je třída. Metoda validate na třídě (z tvého Validate mixinu v SimpleBase) vyžaduje jako první parametr value. To máš správně. Ale pokud inner_instance je tvůj Atom, pak má atribut .value. Pokud je to ale primitivní typ (protože dekompozice vrátila int/str), pak .value hodí chybu.
    
    Bezpečnější varianta:
    
    # Místo inner_instance.value použijeme raději jen inner_instance, 
    # protože u primitivních typů je to hodnota samotná, u Atomů je to objekt.
    val_to_check = inner_instance.value if hasattr(inner_instance, 'value') else inner_instance
    inner.validate(val_to_check)
    """

    def validate_all(self) -> Dict[str, List[str]]:
        """
        Provede validaci sebe sama i všech inners.
        Vrací slovník {cesta: [chyby]}.
        """
        errors = {}


        # 1. Validace sebe sama
        try:
            self.validate(self.value)
        except Exception as e:
            errors[self.meta.name_snake] = [str(e)]

        # 2. Rekurzivní validace inners
        if self.meta.inners:
            for inner in self.meta.inners:
                inner_instance = getattr(self, inner.name_snake)

                if hasattr(inner_instance, 'validate_all'):
                    # Sloučení chyb z podstromu
                    for path, inner_errors in inner_instance.validate_all().items():
                        full_path = f"{self.meta.name_snake}.{path}"
                        errors[full_path] = inner_errors
                else:
                    # Základní validace pokud inner nemá validate_all
                    try:
                        inner.validate(inner_instance.value)
                    except Exception as e:
                        errors[f"{self.meta.name_snake}.{inner.name_snake}"] = [str(e)]

        return errors

    @property
    def is_valid_deep(self) -> bool:
        """Rychlá kontrola — True pokud je vše v pořádku."""
        return len(self.validate_all()) == 0