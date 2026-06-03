from typing import Callable, Optional


# patterns/Event.py
class EventMixin:
    """
    Event system — pojmenované události s callbacky.

    Příklad:
        obj.on("before_save", my_validation_func)
        obj.trigger("before_save")
    """
    __slots__ = ()

    def on(self, event_name: str, callback: Callable) -> None:
        """Zaregistruje callback na danou událost."""
        if not callable(callback):
            raise TypeError(f"Callback must be callable, got {type(callback).__name__}")

        # Lazy init events dict
        if not hasattr(self, '_events'):
            object.__setattr__(self, '_events', {})

        events = object.__getattribute__(self, '_events')
        if event_name not in events:
            events[event_name] = []
        events[event_name].append(callback)

    def trigger(self, event_name: str, *args, **kwargs) -> None:
        """Spustí všechny callbacky pro danou událost."""
        events = getattr(self, '_events', {})
        for callback in events.get(event_name, []):
            try:
                callback(self, *args, **kwargs)
            except Exception as e:
                print(f"Event error in {event_name}: {e}")

    def off(self, event_name: str, callback: Optional[Callable] = None) -> None:
        """
        Odregistruje callback(y) z události.
        Pokud callback není zadán, odstraní všechny.
        """
        if not hasattr(self, '_events'):
            return

        events = object.__getattribute__(self, '_events')
        if event_name not in events:
            return

        if callback is None:
            # Odstraň všechny callbacky pro tuto událost
            events[event_name] = []
        elif callback in events[event_name]:
            events[event_name].remove(callback)

"""
1. Konflikt s __slots__
V kódu používáš object.__setattr__(self, '_events', {}). To je sice šikovný trik, jak obejít settery, ale má to jeden háček: Pokud třída používá __slots__ a _events v nich není definováno, tento kód vyhodí AttributeError.

Protože tvůj generátor tříd SimpleObject dynamicky skládá __slots__, máš dvě možnosti:

Přidat _events do __slots__ v každé třídě, která tento mixin používá.

Přiznat si, že objekty s událostmi budou mít __dict__ (což bys asi nechtěl).

Doporučení: V rámci tvého orchestrátoru process_mixins nebo v továrně OBJECT bys měl kontrolovat, zda je přítomen EventMixin, a pokud ano, automaticky přidat _events do výsledných __slots__.

2. Lazy inicializace a bezpečnost
Použití object.__getattribute__ a __setattr__ je v tomto kontextu zbytečně "násilné". Pokud budou _events v __slots__, můžeš použít standardní getattr/setattr.

Také pozor na print() v metodě trigger. V produkční knihovně by chyba v callbacku neměla jen tak "vytéct" do konzole. Lepší by bylo buď chyby sbírat, nebo použít standardní logging.

3. Moje "refaktorovaná" verze pro tvůj systém
Python

class EventMixin:
    """
    Event system — optimalizovaný pro SimpleObject.
    """
    __slots__ = () # _events musí být v konečných slots třídy

    def _get_events_storage(self) -> dict:
        """Zajistí bezpečný přístup k úložišti událostí."""
        try:
            # Předpokládáme, že slots jsou připraveny
            ev = getattr(self, '_events')
            if ev is None: # Pokud je výchozí hodnota ve slots None
                ev = {}
                setattr(self, '_events', ev)
            return ev
        except AttributeError:
            # Fallback pokud slots chybí (pro vývoj/testy)
            if not hasattr(self, '__dict__'):
                 # Tady by měla přijít tvoje SimpleException
                 raise RuntimeError("EventMixin requires '_events' in __slots__ or a __dict__.")
            if '_events' not in self.__dict__:
                self.__dict__['_events'] = {}
            return self.__dict__['_events']

    def on(self, event_name: str, callback: Callable) -> None:
        if not callable(callback):
            raise TypeError(f"Callback must be callable")
        
        events = self._get_events_storage()
        events.setdefault(event_name, []).append(callback)

    def trigger(self, event_name: str, *args, **kwargs) -> None:
        # Tady nevoláme _get_events_storage, abychom zbytečně neinicializovali
        # pokud nikdo nic neposlouchá.
        events_dict = getattr(self, '_events', {}) or {}
        callbacks = events_dict.get(event_name, [])
        
        for callback in callbacks:
            # Voláme callback(self, *args, **kwargs)
            # self jako první argument je skvělý pro kontext
            callback(self, *args, **kwargs)
4. Architektonický detail: Kdo vyvolává události?
Aby tento mixin nebyl jen "mrtvým úložištěm", měl by někdo ty události skutečně spouštět. Napadá mě ideální propojení s _on_update:

Python

# V nějakém budoucím mixinu nebo přímo v SimpleObject:
def _on_update(self):
    if hasattr(self, 'trigger'):
        self.trigger("change", value=self.value)
    super()._on_update()
Zhodnocení:
Nápad: Výborný. Dává objektům "život".

Logika: on/off/trigger je standardní a srozumitelné rozhraní.

Slabina: Implementace úložiště _events versus __slots__. To musíš vyřešit v generátoru tříd.

Chceš se teď podívat na Observable.py? Ten by měl být postavený právě na tomto EventMixinu, že?
"""