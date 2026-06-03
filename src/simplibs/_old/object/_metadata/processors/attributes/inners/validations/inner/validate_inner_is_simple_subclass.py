# Outers
from .......exceptions import SimpleObjectMetadataError
from ......._types import SimpleClassType
from ..utils import exception_info_for_inners


def validate_inner_is_simple_subclass(
    inner: type,
    inners: tuple,
    owner_class: SimpleClassType
) -> None:
    """
    Validuje, že vnitřní prvek je potomkem požadovaných základních tříd.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID INNERS DEFINITION: Prvek z _inners má neplatnou hierarchii
    ═════════════════════════════════════════════════════════════════
    Expected:  Vnitřní prvek musí dědit ze SimpleObject nebo SimpleConstant.
    Got:       repr(inner) (type)
    Problem:   Prvek není potomkem SimpleObject nebo SimpleConstant třídy.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Vnitřní prvky atributu _inners mohou být pouze potomci třídy SimpleObject a SimpleConstant.
         • Opravte uvedený prvek, tak aby byl validním prvkem.
         • Zajistěte, aby všechny třídy v '_inners' dědily z podporovaných základních tříd.
         • Zkontrolujte, zda jste importovali správnou třídu.
         • Acceptable definitions:
         • class {class_name}(class_parrent):
         •     _inners: tuple = (PrvekA, PrvekB)
         •     ...
    ═════════════════════════════════════════════════════════════════
    """

    # Vnitřní import předcházející cilkulární chybě
    from .......SimpleConstant import SimpleConstant

    # 1. Podmínka výjimky
    if not issubclass(inner, SimpleConstant):

        # 2. Vypočet proměných
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = exception_info_for_inners(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleObjectMetadataError(
            error_name=error_name,
            value_label="Prvek z _inners má neplatnou hierarchii",
            expected="Vnitřní prvek musí dědit ze SimpleObject nebo SimpleConstant.",
            value=inner,
            problem="Prvek není potomkem SimpleObject nebo SimpleConstant třídy.",
            context=context,
            how_to_fix=(
                "Vnitřní prvky atributu _inners mohou být pouze potomci třídy SimpleObject a SimpleConstant.",
                "Opravte uvedený prvek, tak aby byl validním prvkem.",
                "Zajistěte, aby všechny třídy v '_inners' dědily z podporovaných základních tříd.",
                "Zkontrolujte, zda jste importovali správnou třídu.",
            ) + acceptable_definitions,
            exception=TypeError
        )

_DESIGN_NOTES = """
# validate_inner_is_simple_object_subclass

## Účel
Tato validace je pilířem integrity celého systému. Ověřuje, že vnořený prvek 
implementuje standardní rozhraní SimpleObject. To je nezbytné, protože 
následné procesory v pipeline budou přistupovat k atributům jako `.meta`, 
které jsou dostupné pouze u tříd vzniklých pod touto metatřídou.

## Vztah k ostatním validacím
Tato funkce je úzce specializovaná:
1. Předpokládá, že prvek již prošel validací `validate_inner_is_class`.
2. Zaměřuje se výhradně na **vztah dědičnosti**.
3. **Důležitá poznámka**: Tato funkce propustí i samotnou základní třídu 
   `SimpleObject` (protože je podtřídou sebe sama). Vyloučení samotné základní 
   třídy je však delegováno na následující krok `validate_inner_is_not_simple_object_class`. 
   Toto rozdělení udržuje každou funkci atomickou a snadno pochopitelnou.

## Strategie Importu
V rámci zachování "čistého zenu" a prevence kruhových importů (Circular Imports) 
neprovádí tato funkce vlastní import `SimpleObject`. Místo toho očekává 
referenci na základní třídu jako parametr `simple_object_base`. Tento parametr 
je poskytnut řídící metodou `_process_composition_setup`, která provádí 
tzv. Lazy Import.
"""