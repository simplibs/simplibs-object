class SetDescriptorNotImplemented:
    """
    Descriptor protokol pro zápis atributů (__set__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject není descriptor - je to value object.
           Descriptory řídí nastavení atributů na třídě.
    """
    __slots__ = ()

    def __set__(self, instance, value):
        ...


__DOCT__ = """
**Purpose:**
`__set__` makes a descriptor a *data descriptor*, giving it priority over the instance
`__dict__`. Without `__set__`, Python would store a value in the instance dict and the
descriptor's `__get__` would be shadowed. With `__set__`, every assignment goes through
the descriptor, enabling validation, type coercion, and computed storage.

**Signature:**
```python
def __set__(self, obj, value) -> None:
    # validate/transform and store
    obj.__dict__[self.name] = value
```

**Called automatically when:**
```python
instance.attr = value   # if descriptor defines __set__, it intercepts the assignment
```

**Relationships:**
- Together with `__get__`, forms a complete data descriptor.
- Add `__delete__` for a full descriptor (get + set + delete).
- Without `__set__`, the descriptor is a non-data descriptor — instance dict can shadow it.

"""