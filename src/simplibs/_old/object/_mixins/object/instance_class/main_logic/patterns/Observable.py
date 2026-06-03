from typing import Any, List, Callable


# patterns/Observable.py
class ObservableMixin:
    """
    Observer pattern — sledování změn objektu.

    Příklad:
        obj.add_observer(lambda o: print(f"Changed to {o.value}"))
        obj.value = 42  # → "Changed to 42"
    """
    __slots__ = ()

    @property
    def _observers(self) -> List[Callable]:
        """Lazy inicializace seznamu observerů."""
        if not hasattr(self, '_observers_storage'):
            object.__setattr__(self, '_observers_storage', [])
        return self._observers_storage

    def add_observer(self, callback: Callable[[Any], None]) -> None:
        """Přidá funkci která bude zavolána při každé změně."""
        if not callable(callback):
            raise TypeError(f"Observer must be callable, got {type(callback).__name__}")

        if callback not in self._observers:
            self._observers.append(callback)

    def remove_observer(self, callback: Callable[[Any], None]) -> None:
        """Odstraní registrovaný callback."""
        if hasattr(self, '_observers_storage') and callback in self._observers:
            self._observers.remove(callback)

    def _notify_observers(self) -> None:
        """Interní metoda — spustí všechny zaregistrované callbacky."""
        for callback in getattr(self, '_observers_storage', []):
            try:
                callback(self)
            except Exception as e:
                # Nechceme aby pád jednoho observeru zastavil zbytek
                print(f"Observer error in {callback}: {e}")

    def _on_update(self) -> None:
        """Hook volaný po změně hodnoty."""
        super()._on_update()
        self._notify_observers()


"""
Tady už se dostáváme k reálné magii "reaktivního" objektu. ObservableMixin je v podstatě specializovaná, zjednodušená verze událostí zaměřená čistě na životní cyklus dat.

Mám k němu tři hlavní postřehy, které navazují na naši předchozí debatu:

1. _on_update a MRO (Method Resolution Order)
Tady jsi udělal přesně to, co jsme u ChainMixin předvídali:

Python

def _on_update(self) -> None:
    super()._on_update()
    self._notify_observers()
Tohle je naprosto správně. Díky super()._on_update() zajistíš, že pokud existuje celý řetězec mixinů (např. jeden loguje, druhý ukládá, třetí je tento), všechny se provedou v pořadí, v jakém byly "namíchány".

2. Problém s __slots__ (Opět a znovu)
Stejně jako u EventMixin, i tady narážíme na object.__setattr__(self, '_observers_storage', []).

Pokud tvůj finální SimpleObject nebude mít ve svých __slots__ definován název _observers_storage, tento kód selže.

U ObservableMixin je riziko ještě o něco vyšší, protože je velmi pravděpodobné, že ho uživatelé budou chtít používat masivně.

Doporučení: Protože EventMixin a ObservableMixin řeší v podstatě totéž (notifikace), zvaž, zda je nesjednotit pod jeden systém úložiště, nebo zajistit, aby tvůj orchestrátor process_mixins automaticky "přibalil" potřebné sloty.

3. "Lazy" inicializace v property
Tvůj přístup přes @property s názvem _observers je elegantní:

Python

@property
def _observers(self) -> List[Callable]:
    if not hasattr(self, '_observers_storage'):
        object.__setattr__(self, '_observers_storage', [])
    return self._observers_storage
Pozor na jednu věc: Pokud uživatel zavolá hasattr(obj, '_observers'), vrátí to True, což je v pořádku. Ale pokud tvůj kód (např. v _notify_observers) používá getattr(self, '_observers_storage', []), tak obcházíš tu tvou lazy inicializaci v property a vracíš prázdný seznam, i když property by ho právě teď vytvořila. V tomto konkrétním případě to nevadí (v obou případech se nic nestane), ale je dobré držet se jednoho přístupu.

Jak to vylepšit pro "Simple" standard?
Pokud bys chtěl být opravdu precizní, navrhoval bych malou úpravu v _notify_observers, aby se callbackům předávala i stará hodnota (pokud ji budeme v budoucnu v HistoryMixin držet). Ale pro teď stačí předávat self.

Můj tip pro robustnost:

Python

def _notify_observers(self) -> None:
    # Použijeme raději property, abychom využili tu lazy inicializaci, 
    # pokud by někdo náhodou volal notify dříve než add.
    observers = getattr(self, '_observers_storage', None)
    if not observers:
        return

    for callback in observers:
        try:
            # Předáváme celou instanci, uživatel si z ní vytáhne .value nebo .meta
            callback(self)
        except Exception as e:
            # Tady bychom v budoucnu mohli mít SimpleException nebo logger
            pass 
Zhodnocení:
ObservableMixin je skvělý doplněk. Je to přesně ta "kostička lega", která dělá rozdíl mezi statickým datovým kontejnerem a živým objektem, který může pohánět UI (např. v Tkinteru, PySide nebo i webovém frontendu).

Zbývá nám z této sekce něco, nebo už "mutujeme" směrem k Mutation.py a Randomize.py? Randomize.py zní jako osvěžující kousek po vší té vážné logice!
"""