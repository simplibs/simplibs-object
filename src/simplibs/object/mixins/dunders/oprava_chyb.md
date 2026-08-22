
---

### 2. `Lifecycle` / `PickleReduce` – Názvy dynamických tříd při picklování

* **Zasažené testy:**
* `test_Lifecycle.py::TestLifecycleCombinedAPI::test_provides_both_copy_and_pickle_api`
* `test_PickleReduce.py::TestPickleReduceRoundTrip::test_full_pickle_unpickle_round_trip_mutable`


* **Kód a chyba:**
* `_pickle.PicklingError: Can't pickle <OuterBlueprint ...>: attribute lookup OuterInstance on simplibs.object._core.metadata.SimpleMeta failed`


* **Příčina:**
* Standardní pickle mechanismus se pokouší lokalizovat dynamicky vytvořenou instanční třídu (`OuterInstance`) přes globální modul (`__module__` a `__qualname__`). V `__reduce__` vracíte třídu instance jako callable objekt (`cls`), ale tato třída byla vygenerována za běhu a nelze ji z modulu importovat.


* **Proč opravit:**
* Objekty vytvořené frameworkem musí být serializovatelné pomocí `pickle` (pro multiprocessing, caching, Celery apod.).


* **Jak opravit:**
* V `__reduce__` nevracet přímo dynamickou třídu `self.__class__`, ale tovární funkci (např. funkci `_reconstruct_instance` nebo původní blueprint class) a argumenty potřebné k její obnově:
```python
def __reduce__(self):
    # Vracet helper funkci, která umí instanci zrekonstruovat
    return (_rebuild_instance_helper, (self._blueprint, self._build_snapshot()))

