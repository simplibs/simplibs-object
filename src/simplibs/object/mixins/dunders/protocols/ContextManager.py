class ContextManagerMixin(SimpleMixin):
    """Umožňuje použití objektu jako kontextového manažeru (with obj:)."""


    __slots__ = ()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False  # neignorujeme výjimky
