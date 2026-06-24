class NewInstanceMixin(SimpleMixin):
    """
    Sdílený základ pro mixiny které potřebují vytvořit novou instanci se změněnou hodnotou.
    """
    __slots__ = ()

    def _new_with_value(self, new_value: Any) -> Any:
        new = self.__class__()
        new.value = new_value
        return new

# Předělat mixiny aby nekopírovali metodu a měli tohoto předka:
class NumericArithmeticMixin(NewInstanceMixin): ...
class NumericUnaryMixin(NewInstanceMixin): ...
class BitwiseMixin(NewInstanceMixin): ...