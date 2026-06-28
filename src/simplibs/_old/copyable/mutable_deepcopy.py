import copy as _copy
# Outers
from ......_metadata.instance_builders.instance import create_instance


def mutable_deepcopy(self, memo):
    new = create_instance(
        cls=self.__class__.meta.owner_class,
        mixins=self.__class__.__mixins__,
        as_atom=self.__class__.__is_constant__,
        mutable=True,
        validate=False
    )
    new.value = _copy.deepcopy(self.value, memo)
    return new
