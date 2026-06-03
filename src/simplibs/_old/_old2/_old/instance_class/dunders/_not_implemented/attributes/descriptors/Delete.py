class DeleteDescriptorNotImplemented:
    """
    Descriptor protokol pro mazání atributů (__delete__).

    V SimpleObject: NEIMPLEMENTOVÁNO
    Důvod: SimpleObject není descriptor - je to value object.
           Descriptory se používají pro atributy na třídě, ne instance.
    """
    __slots__ = ()

    def __delete__(self, instance):
        ...


__DOCT__ = """
**Purpose:**
`__delete__` (the descriptor variant) is called when `del instance.attr` is issued and
the class has a data descriptor for that name. It allows the descriptor to control what
happens when the attribute is deleted — you might clear the stored value, raise an error,
or trigger a cascade.

**Signature:**
```python
def __delete__(self, obj) -> None:
    obj.__dict__.pop(self.name, None)
```

**Called automatically when:**
```python
del instance.attr   # if attr's descriptor defines __delete__
```

**Relationships:**
- Completes the descriptor triad: `__get__`, `__set__`, `__delete__`.
- Distinguished from `__delattr__` — `__delattr__` is on the *object*; `__delete__` is on the *descriptor*.

"""