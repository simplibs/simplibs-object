from typing import Any


class FormatMixin:
    """
    Mixin umožňující formátovat výstupní hodnotu podle masky nebo pravidel.

    Metody:
        - format(pattern: str | None) -> str
        - __format__(format_spec: str) -> str (pro f-stringy)

    Pokud není pattern zadán, zkusí použít masku z metadat (pokud existuje).
    """

    # Očekává
    value: Any
    meta: Any

    def format(self, pattern: str = None) -> str:
        """
        Zformátuje hodnotu. Pokud není pattern zadán, zkusí ho najít v metadatech.
        Příklad: "+420 {}" pro telefonní číslo.
        """
        # Hledáme masku v metadatech (pokud ji tam v budoucnu přidáme)
        mask = pattern or getattr(self.meta, 'mask', None)

        if mask and isinstance(self.value, (str, int, float)):
            # Rozhodnout se za potřebuji zde try except blok a nebo je zbytečný?
            # try:
            #     return mask.format(self.value)
            # except Exception:
            #     # Pokud formátování selže, vrátíme prostě str(self.value)
            #     return str(self.value)
            return mask.format(self.value)

        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        """Podpora pro f-stringy: f"{obj:maska}" """
        return self.format(format_spec)


__DOCT__ = """
**Purpose:**
Defines how `format(obj, spec)` renders the object — the `spec` part of `f"{obj:spec}"`.
For example, `f"{number:.2f}"` calls `number.__format__(".2f")`. This lets your class
support the full Python format mini-language or a custom one. If `__format__` is not
defined, Python falls back to `str(obj)` (i.e., `__str__`).

**Signature:**
```python
def __format__(self, format_spec: str) -> str:
    if format_spec == "":
        return str(self)
    # delegate to a built-in type for numeric formatting:
    return format(self.value, format_spec)
```

**Called automatically when:**
```python
format(obj, ".2f")   # direct call
f"{obj:.2f}"         # f-string with format spec
"{:.2f}".format(obj) # str.format()
```

**Relationships:**
- Falls back to `__str__` when spec is empty.
- `__str__` and `__repr__` are simpler alternatives for non-formatted output.

**Example:**
```python
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount, self.currency = amount, currency

    def __format__(self, spec):
        if spec == "long":
            return f"{self.amount:.2f} {self.currency}"
        return format(self.amount, spec or ".2f")

m = Money(1234.5)
print(f"{m}")        # 1234.50
print(f"{m:long}")   # 1234.50 USD
print(f"{m:,.2f}")   # 1,234.50
```
"""