"""
Tests for `_core/metadata/instance_builders/instance/create_instance.py`.
"""
import pytest
from simplibs.object import SimpleBase, SimpleConstant, SimpleObject
from simplibs.object.exceptions import SimpleInitializationError


class TestCreateInstanceHappyPath:

    def test_instantiating_constant_returns_working_instance(self, IntConst):
        instance = IntConst()
        assert instance.value == IntConst.meta.default

    def test_instantiated_object_is_locked_false_by_default(self, IntConst):
        instance = IntConst()
        assert instance._locked is False


class TestCreateInstanceBaseClassGuard:

    def test_instantiating_simple_base_raises(self):
        with pytest.raises(SimpleInitializationError):
            SimpleBase()

    def test_instantiating_simple_constant_raises(self):
        with pytest.raises(SimpleInitializationError):
            SimpleConstant()

    def test_instantiating_simple_object_raises(self):
        with pytest.raises(SimpleInitializationError):
            SimpleObject()


class TestCreateInstanceParamValidation:

    def test_as_atom_must_be_bool(self, IntConst):
        with pytest.raises(SimpleInitializationError):
            IntConst(as_atom="not-a-bool")

    def test_mutable_must_be_bool(self, IntConst):
        with pytest.raises(SimpleInitializationError):
            IntConst(mutable="not-a-bool")


class TestCreateInstanceImmutability:

    def test_immutable_instance_is_locked_or_readonly(self, IntConst):
        instance = IntConst(mutable=False)
        with pytest.raises(AttributeError):
            instance.value = 5


class TestCreateInstanceStructuralModeResolution:

    def test_constant_is_always_atom_regardless_of_as_atom_flag(self, IntConst):
        instance = IntConst(as_atom=False)
        assert instance.value == IntConst.meta.default


class TestCreateInstanceMixinsSlotsBugRegression:

    def test_two_independently_slotted_mixins_via_public_api(self, IntConst):
        from simplibs.object.mixins.base_class import SimpleMixin

        class MixinA(SimpleMixin):
            __slots__ = ("_slot_a",)

            def init_mixins(self):
                self._slot_a = "a"

        class MixinB(SimpleMixin):
            __slots__ = ("_slot_b",)

            def init_mixins(self):
                self._slot_b = "b"

        instance = IntConst(mixins=(MixinA, MixinB))
        assert instance._slot_a == "a"
        assert instance._slot_b == "b"
        assert instance.value == IntConst.meta.default