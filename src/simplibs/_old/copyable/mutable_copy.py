# Outers
from ......_metadata.instance_builders.instance import create_instance


def mutable_copy(self):
    new = create_instance(
        cls=self.__class__.meta.owner_class,
        mixins=self.__class__.__mixins__,
        as_atom=self.__class__.__is_constant__,
        mutable=True,
        validate=False
    )
    new.value = self.value
    return new

