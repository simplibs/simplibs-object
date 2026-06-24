class InitSubclassNotImplemented:
    """
    Hook volaný při vytvoření podtřídy (__init_subclass__).

    V SimpleObject: NEIMPLEMENTOVÁNO (řízeno metaclass)
    Důvod: SimpleObjectMeta řídí tvorbu podtříd.
           Přidání __init_subclass__ by kolidovalo s metaclass logikou.
    """
    __slots__ = ()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        ...



__DOCT__ = """
**Purpose:**
`__init_subclass__` is called on the *parent* class whenever a new subclass of it is
created. This allows a base class to automatically register subclasses, enforce contracts,
or inject behaviour into child classes without a metaclass. It receives the new subclass as
`cls` and any keyword arguments passed in the class definition line.

**Signature:**
```python
@classmethod
def __init_subclass__(cls, /, **kwargs) -> None:
    super().__init_subclass__(**kwargs)
    # cls is the newly defined subclass
```

**Called automatically when:**
```python
class Child(Parent, some_kwarg=True):   # __init_subclass__ fires on Parent
    pass
```

**Relationships:**
- Related to `__set_name__` (also fires at class-definition time).
- Related to `__class_getitem__` (class-level hook for subscript syntax).
- Alternative to metaclasses for simple subclass-time customisation.

**Example:**
```python
class PluginBase:
    _registry = {}

    def __init_subclass__(cls, plugin_name: str = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name:
            PluginBase._registry[plugin_name] = cls

class AudioPlugin(PluginBase, plugin_name="audio"):
    pass

class VideoPlugin(PluginBase, plugin_name="video"):
    pass

print(PluginBase._registry)
# {'audio': <class 'AudioPlugin'>, 'video': <class 'VideoPlugin'>}
```
"""