from simplibs.sentinels import UNSET
from ...mixins.base_class import SimpleMixin


class TestMixin(SimpleMixin):
    """
    Universal test mixin used for shallow and deep validation of SimpleObject instances.

    It verifies:
    - slot propagation
    - property propagation
    - method propagation
    - init_mixins execution
    - __extend_instance_class__ execution
    """

    # ------------------------------------------------------------
    # Compatibility flags (no restrictions)
    # ------------------------------------------------------------
    _constant_only = False
    _composite_only = False
    _mutable_only = False
    _immutable_only = False
    _only_types = UNSET

    # ------------------------------------------------------------
    # Slot definition
    # ------------------------------------------------------------
    __slots__ = ("_test_slot",)

    # ------------------------------------------------------------
    # Initialization hook
    # ------------------------------------------------------------
    def init_mixins(self):
        """
        Called during instance initialization.
        We set the slot to a known value so tests can verify propagation.
        """
        super().init_mixins()
        self._test_slot = "test_value"

    # ------------------------------------------------------------
    # Property exposing the slot
    # ------------------------------------------------------------
    @property
    def test_property(self):
        return self._test_slot

    @test_property.setter
    def test_property(self, value):
        self._test_slot = value

    # ------------------------------------------------------------
    # Simple method for testing method propagation
    # ------------------------------------------------------------
    def test_method(self):
        return f"[TestMixin] property={self._test_slot}"

    # ------------------------------------------------------------
    # Class extension hook
    # ------------------------------------------------------------
    @staticmethod
    def __extend_instance_class__(instance_cls):
        """
        Adds a class-level attribute and method to the instance class.
        This verifies that mixins can modify the runtime class before instantiation.
        """

        # 1) Add a class-level attribute
        setattr(instance_cls, "test_class_attribute", "class_level_ok")

        # 2) Add a class-level method
        def test_class_method(self):
            return "class_method_ok"

        setattr(instance_cls, "test_class_method", test_class_method)

        return instance_cls
