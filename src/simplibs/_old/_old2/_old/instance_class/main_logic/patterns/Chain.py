from typing import Any

from ..core.Metadata import MetadataMixin
from typing import Self

# patterns/Chain.py
class ChainMixin(MetadataMixin):
    """
    Fluent Interface — řetězení metod.

    Příklad:
        obj.set_value(10).set_attr('enabled', True).validate()
    """
    __slots__ = ()
    value: Any

    def set_value(self, new_value: Any) -> Self:
        """Nastaví hodnotu a vrátí self pro řetězení."""
        self.value = new_value
        return self

    def set_attr(self, name: str, value: Any) -> Self:
        """
        Nastaví vnitřní atribut (inner) a vrátí self.

        Validuje, že atribut existuje a je součástí inners.
        """
        # Validace existence
        if not hasattr(self, 'meta') or not self.meta.inners:
            raise AttributeError(f"{self.__class__.__name__} has no inners")

        valid_attrs = {inner.name_snake for inner in self.meta.inners}
        if name not in valid_attrs:
            raise AttributeError(
                f"'{name}' is not a valid inner attribute. "
                f"Valid attributes: {', '.join(valid_attrs)}"
            )

        # Původně bylo:
        # setattr(self, name, value)

        # Získáme vnitřní prvek (což je Atom nebo SimpleObject)
        inner_element = getattr(self, name)

        # Nastavíme hodnotu DO něj (tím se spustí jeho vlastní validace)
        inner_element.value = value

        # EXPLICITNĚ vyvoláme update na sobě (rodiči), protože jsme změnili svou část
        if hasattr(self, '_on_update'):
            self._on_update()

        return self