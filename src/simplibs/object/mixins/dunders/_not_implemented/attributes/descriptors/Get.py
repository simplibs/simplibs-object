class GetDescriptorNotImplemented:
    """
    Descriptor protokol pro čtení atributů (__get__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject není descriptor - je to value object.
           Descriptory řídí přístup k atributům na třídě.
    """
    __slots__ = ()

    def __get__(self, instance, owner):
        ...


__DOCT__ = """
**Purpose:**
`__get__` is called when the descriptor is accessed through an instance or a class.
When accessed via an instance, `obj` is the instance and `objtype` is its class.
When accessed directly on the class, `obj` is `None`. This asymmetry allows descriptors
to return themselves (the descriptor object) when accessed on the class, and a computed
value when accessed on an instance.

**Signature:**
```python
def __get__(self, obj, objtype=None):
    if obj is None:
        return self   # class-level access returns the descriptor itself
    return computed_value
```

**Called automatically when:**
```python
instance.attr   # if attr's class defines __get__, it fires instead of normal lookup
MyClass.attr    # also fires, but obj=None
```

**Relationships:**
- A descriptor with only `__get__` is a *non-data descriptor* (instance dict wins).
- Add `__set__` to make it a *data descriptor* (descriptor wins over instance dict).
- `__set_name__` fires when the descriptor is first assigned to the class.
- The default `__getattribute__` is what actually invokes `__get__`.

**Example:**
```python
class Celsius:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, 0.0)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = float(value)

class Temperature:
    celsius = Celsius()

t = Temperature()
t.celsius = 100
print(t.celsius)           # 100.0
print(Temperature.celsius) # <Celsius object>
```
"""