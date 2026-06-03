class AbstractmethodsNotImplemented:
    """
    Set abstraktních metod třídy (__abstractmethods__).

    V SimpleObject: NEIMPLEMENTOVÁNO (ABC systém)
    Důvod: SimpleObject nepoužívá ABC (Abstract Base Classes).
           Používá SimpleObjectMeta pro validaci metadat.
    """
    __slots__ = ()


__DOCT__ = """
**Purpose:**
`__abstractmethods__` is a frozenset attribute automatically maintained by `ABCMeta`
(the metaclass for abstract base classes). It contains the names of all abstract methods
that have not yet been implemented in a concrete subclass. If `__abstractmethods__` is
non-empty, instantiating the class raises `TypeError`. You never set this manually —
it is managed by `@abstractmethod` decorators and `ABCMeta`.

**You do not implement this** — use `abc.ABCMeta` and `@abc.abstractmethod`:
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str: ...

class Dog(Animal):
    def speak(self): return "Woof"

Animal()    # TypeError: Can't instantiate abstract class
Dog()       # OK — speak is implemented
```

**Relationships:**
- Maintained by `ABCMeta` metaclass automatically.
- Works with `__subclasshook__` for virtual subclass registration.
"""

