class GetattributeNotImplemented:
    """
    Primární metoda pro přístup k atributům (__getattribute__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: Přepisování __getattribute__ je nebezpečné - ovlivňuje VŠECHNY
           atributy včetně interních. Rozbilo by to celý SimpleObject systém.
    """
    __slots__ = ()

    def __getattribute__(self, name: str):
        ...


__DOCT__ = """
**Purpose:**
`__getattribute__` is called for *every single attribute access* on an object — it is the
lowest-level hook in Python's attribute system. The default implementation in `object`
handles the full descriptor/dict lookup chain. Override it only when you need to intercept
*all* attribute access, for example to implement transparent proxies or attribute logging.
**Danger:** accessing `self.anything` inside `__getattribute__` will call itself recursively.
Always use `object.__getattribute__(self, name)` or `super().__getattribute__(name)` to
safely reach the real value.

**Signature:**
```python
def __getattribute__(self, name: str):
    return super().__getattribute__(name)
```

**Called automatically when:**
```python
obj.x          # every single attribute read calls __getattribute__
obj.method()   # method lookup also goes through __getattribute__
```

**Relationships:**
- If `__getattribute__` raises `AttributeError`, Python then calls `__getattr__`.
- Contrast with `__getattr__` — which is only a fallback.
- Lives above the descriptor protocol: `__get__` is called *by* the default `__getattribute__`.

**Example:**
```python
class Logged:
    def __init__(self, x):
        self.x = x

    def __getattribute__(self, name):
        print(f"Accessing: {name}")
        return super().__getattribute__(name)   # MUST use super() to avoid recursion

obj = Logged(10)
_ = obj.x    # prints "Accessing: x"
```

"""