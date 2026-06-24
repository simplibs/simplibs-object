import copy as _copy
# Outers
from ....._metadata.instance_builders.instance import create_instance
from .....protocols import SimpleInstanceType


class LifecycleMutableMixin:
    """
    Mutable lifecycle:
    - mělká kopie přes create_instance(validate=False)
    - hluboká kopie přes create_instance(validate=False)
    """

    __slots__ = ()

    # ---------------------------------------------------------
    # 1) Mělká kopie (mutable)
    # ---------------------------------------------------------
    def __copy__(self):
        new = create_instance(
            cls=self.__class__.meta.owner_class,
            mixins=self.__class__.__mixins__,
            as_atom=self.__class__.__is_constant__,
            mutable=True,
            validate=False
        )
        new.value = self.value
        return new

    # ---------------------------------------------------------
    # 2) Hluboká kopie (mutable)
    # ---------------------------------------------------------
    def __deepcopy__(self, memo):
        new = create_instance(
            cls=self.__class__.meta.owner_class,
            mixins=self.__class__.__mixins__,
            as_atom=self.__class__.__is_constant__,
            mutable=True,
            validate=False
        )
        new.value = _copy.deepcopy(self.value, memo)
        return new
