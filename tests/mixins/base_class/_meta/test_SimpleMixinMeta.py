"""
Tests for `SimpleMixinMeta` metaclass.
"""
from types import SimpleNamespace
import pytest
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.object.mixins.base_class._meta.SimpleMixinMeta import SimpleMixinMeta


class TestSimpleMixinMetaValidationTrigger:

    def test_root_meta_definition_without_bases_skips_validation(self):
        # Empty bases simulate the root base class definition
        root_cls = SimpleMixinMeta("RootClass", (), {"__slots__": ()})
        assert isinstance(root_cls, SimpleMixinMeta)

    def test_subclass_with_invalid_slots_fails_at_class_creation(self):
        root_cls = SimpleMixinMeta("RootClass", (), {"__slots__": ()})

        with pytest.raises(SimpleRuntimeError):
            # Creating a subclass with missing slots fails immediately
            SimpleMixinMeta("InvalidDerived", (root_cls,), {})

    def test_valid_subclass_creates_successfully(self):
        root_cls = SimpleMixinMeta("RootClass", (), {"__slots__": ()})
        derived = SimpleMixinMeta("ValidDerived", (root_cls,), {"__slots__": ("slot_a",)})
        assert issubclass(derived, root_cls)


class TestSimpleMixinMetaInstanceCheck:

    def test_standard_isinstance_returns_true_for_direct_instance(self):
        class Root(metaclass=SimpleMixinMeta):
            __slots__ = ()

        class ConcreteMixin(Root):
            __slots__ = ()

        instance = ConcreteMixin()
        assert isinstance(instance, ConcreteMixin)
        assert isinstance(instance, Root)

    def test_isinstance_matches_from_flat_mixins_registry(self):
        class TargetMixin(metaclass=SimpleMixinMeta):
            __slots__ = ()

        # Instance from runtime compiler that does not have TargetMixin in MRO,
        # but registers it in its flat __mixins__ registry tuple
        dynamic_instance = SimpleNamespace(__mixins__=(TargetMixin,))

        assert isinstance(dynamic_instance, TargetMixin)

    def test_isinstance_matches_subclass_in_flat_mixins_registry(self):
        class BaseMixin(metaclass=SimpleMixinMeta):
            __slots__ = ()

        class ChildMixin(BaseMixin):
            __slots__ = ()

        dynamic_instance = SimpleNamespace(__mixins__=(ChildMixin,))

        assert isinstance(dynamic_instance, ChildMixin)
        assert isinstance(dynamic_instance, BaseMixin)

    def test_isinstance_returns_false_when_not_registered(self):
        class TargetMixin(metaclass=SimpleMixinMeta):
            __slots__ = ()

        class OtherMixin(metaclass=SimpleMixinMeta):
            __slots__ = ()

        dynamic_instance = SimpleNamespace(__mixins__=(OtherMixin,))

        assert not isinstance(dynamic_instance, TargetMixin)

    def test_isinstance_handles_objects_without_mixins_attribute(self):
        class TargetMixin(metaclass=SimpleMixinMeta):
            __slots__ = ()

        obj = object()
        assert not isinstance(obj, TargetMixin)