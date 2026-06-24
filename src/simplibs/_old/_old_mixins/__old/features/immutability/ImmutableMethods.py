# Inners
from .ImmutableBase import ImmutableBase



class ImmutableMethods(ImmutableBase):


    @staticmethod
    def __extend_instance_class__(instance_cls):

        for name in instance_cls.meta.nodes_name:
            def method(self, value, _name=name):
                # rozhodni, jestli je konstanta nebo kompozice
                if _name in self._constant_names:
                    return self.with_constant(_name, value)
                else:
                    return self.with_composite(_name, value)

            setattr(instance_cls, f"with_{name}", method)

        # 3. Navrácení upravené třídy
        return instance_cls



    def with_value(self, new_value):
        ...

