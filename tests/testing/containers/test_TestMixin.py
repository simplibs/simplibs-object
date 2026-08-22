"""
Tests for `testing/containers/TestMixin.py`.
"""
from simplibs.object.mixins.base_class import SimpleMixin
from simplibs.object.testing.containers.TestMixin import TestMixin


class TestTestMixinStructure:

    def test_inherits_from_simple_mixin(self):
        assert issubclass(TestMixin, SimpleMixin)

    def test_compatibility_flags_are_unrestricted(self):
        assert TestMixin._constant_only is False
        assert TestMixin._composite_only is False
        assert TestMixin._mutable_only is False
        assert TestMixin._immutable_only is False

    def test_declares_test_slot(self):
        assert "_test_slot" in TestMixin.__slots__


class TestTestMixinInstanceIntegration:

    def test_slot_is_initialized_on_instance_creation(self, IntConst):
        instance = IntConst(mixins=(TestMixin,))
        assert instance._test_slot == "test_value"

    def test_property_reads_slot_value(self, IntConst):
        instance = IntConst(mixins=(TestMixin,))
        assert instance.test_property == "test_value"

    def test_property_setter_updates_slot_value(self, IntConst):
        instance = IntConst(mixins=(TestMixin,))
        instance.test_property = "changed"
        assert instance._test_slot == "changed"

    def test_method_reflects_current_property_state(self, IntConst):
        instance = IntConst(mixins=(TestMixin,))
        assert instance.test_method() == "[TestMixin] property=test_value"

        instance.test_property = "updated"
        assert instance.test_method() == "[TestMixin] property=updated"


class TestTestMixinExtendInstanceClass:

    def test_class_level_attribute_is_injected(self, IntConst):
        instance = IntConst(mixins=(TestMixin,))
        assert getattr(instance.__class__, "test_class_attribute", None) == "class_level_ok"

    def test_class_level_method_is_injected(self, IntConst):
        instance = IntConst(mixins=(TestMixin,))
        assert instance.test_class_method() == "class_method_ok"

    def test_extend_instance_class_returns_the_same_class_object(self):
        class FakeInstanceClass:
            pass

        result = TestMixin.__extend_instance_class__(FakeInstanceClass)
        assert result is FakeInstanceClass
        assert result.test_class_attribute == "class_level_ok"