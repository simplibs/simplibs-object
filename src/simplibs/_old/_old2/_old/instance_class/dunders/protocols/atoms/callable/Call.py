from typing import Any


class CallMixin:
    """
    Mixin umožňující volat objekt jako funkci pro dočasnou transformaci hodnoty.
    """

    value: Any

    # def __call__(self, **kwargs: Any) -> Any:
    #     """
    #     Zavolání instance s parametry vytvoří dočasný klon,
    #     který okamžitě vrátí svou hodnotu.
    #     """
    #     if not kwargs:
    #         # Volání bez parametrů vrací aktuální hlavní hodnotu
    #         return self.value
    #
    #     # Vytvoříme dočasnou instanci s novými parametry
    #     temp_instance = self.with_(**kwargs)
    #
    #     # Vrátíme hodnotu této dočasné instance
    #     return temp_instance.value
    #
    #
    # def __call__(self, **kwargs: Any) -> Any:
    #     """
    #     Zkratka pro get_calculated_value.
    #     Umožňuje zápis: vysledek = obj(dan=0.21)
    #     """
    #     if not kwargs:
    #         return self.value
    #
    #     return self.get_calculated_value(**kwargs)

    def __call__(self, return_instance=False, **kwargs: Any) -> Any:
        """
        Zkratka pro get_calculated_value.
        Umožňuje zápis: vysledek = obj(dan=0.21)
        """
        if return_instance:
            if not kwargs:
                return self.copy_self()
            return self.create_modified_instance(**kwargs)

        if not kwargs:
            return self.value
        return self.get_calculated_value(**kwargs)

__DOCT__ = """
**Purpose:**
`__call__` is invoked when an instance is used with `()`. This transforms any object
into a callable. Useful for: stateful functions (where the object carries configuration),
decorator classes, event handlers, and anywhere you want function-like syntax with the
benefits of OOP (inheritance, state, multiple methods).

**Signature:**
```python
def __call__(self, *args, **kwargs):
    # process arguments
    return result
```

**Called automatically when:**
```python
obj(arg1, arg2)      # calls obj.__call__(arg1, arg2)
callable(obj)        # returns True if __call__ is defined
```

**Relationships:**
- `callable(obj)` returns `True` iff `type(obj)` has `__call__`.
- Related to `__init__` — classes themselves are callable because their metaclass defines `__call__`.
- Enables the *functor* pattern from functional programming.

**Example:**
```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor

double = Multiplier(2)
triple = Multiplier(3)

print(double(5))     # 10
print(triple(5))     # 15
print(list(map(double, [1, 2, 3])))  # [2, 4, 6] — usable as a function
```
"""