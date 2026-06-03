def __init__(self, barva="červená", vykon=100):
    # 1. Atomy
    self._barva = Barva.meta.atom_class(barva)
    self._vykon = Vykon.meta.atom_class(vykon)

    # 2. Kompozice (bere data z už vytvořených atomů)
    self._karoserie = Karoserie.meta.composite_class(barva=self._barva.value)

    # 3. Finální logika
    self._value = self._logic(self._karoserie.value, self._vykon.value)
    self._on_update()


    """
    Super a díky moc :-)

A tedy to co mi z toho plyne že máme před sebou celkem tři kroky:
1) funkci která vytvoří soty - tedy projde slovníky constants_map a composites_map a ze tříd vytahý parametr meta.name_private a ty tedy umístí do slotu a nebo vytvoří kompletní slot který se pak přidá jen do definice dict vytvářené třídy.

2 funkci pro vatvočření initu - ta se tedy bude skládat ze dvou podfunkcí - jedna pro vytvoření parametrů initu - zde tedy budeme vycházet ze slovníku constants_map a brát jejich meta.name_snake a meta.value_type - a tedy možná by i stálo za to, když už to budeme definovat dinamicky, tak aby zde byl i meta.default jako defaultní hodnota - a tím páde init by obsahoval ve svém volání vše co je třeba a neb´muselo se kontrolovat zda byla přžedaná hodnota a nebo ne a má být použit default - ale tuto myšlenku mi tedy taky zhodnotť.

a pak druhá pomocná funkce, by zase vytvořila logiku, kdy by pro všechny konstanty z constants_map vytvořila zápis hodnota do slotu tedy meta.name_private a přebírala by hodnoty z initu dle meta.name_snake a tím že by init obsahoval i defaultní hodntoy nic více by zde nebylo potřeba dělat - a tedy namísto aby tam tyto hodnoty přepsala tak by si z každé této konstanty vytváhla její meta._atom_class a předala ji obdržený parametr, tak aby se vše zvalidovalo a zároveň slot odkazoval na celou instanční třídu a ne jen na hodnotu.
A tedy pak by musela obhospodařit i kompozice, kde bude potřeba vymyslet mechanizmus jak je spracovat, tak aby se šlo od té poslední směrem nahoru tak aby vždy každá měla k dispozici všechny data - tedy počítám, že ta nejspodnější kompozice bude mít v sobě jen konstanty, které díky parametrům už známe - a tedy skrze ně se dopočítá její instance a vloží do slotu, a tak se bude pokračovat skrze všechny ostatní kompozitní třídy a až bude dopočtena i ta poslední, tak příjde na řadu aktuální třída a její hodnota value, která se tedy dopočítá z vypočítaného.

A poslední funkce pro vytváření dinamického obsahu pak bude zaměřena na property, ale to bych zatím nechal na pozděnji at se nám to nemíchá - a tedy zatím se koncentoroval na toto, protože to samo o sobě je už velké sousto - a tedy to co bych chtěl od tebe je návrh jak by mohli vypadat funkce které by připravovali tyto obsahy - a klidně si to rozděl jako funkc ena definici slotů, funkce na definici parametrů pro init, funkce na definici spracování konstant, a funkce na definici zpracování kompozit - a tedy tyto dvě funkce budou pro init. 

a tedy dodatečné nastavování skrze property necháme na příště, ve finále když s enám povvede vyřešit tyto 4 funkce, tak property pak už bude snadná záležitostk de budeme jen kopírovat dané postupy.

A le nejprve se tedy zaměřme na toto -jedna funkc  pro vytvoření slotů a druhá pro definici logiky a parametrů initu :-)
    """