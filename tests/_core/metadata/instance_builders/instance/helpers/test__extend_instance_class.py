"""
Tests for `_core/metadata/instance_builders/instance/helpers/_extend_instance_class.py`.
"""
import pytest
from simplibs.object.mixins.base_class import SimpleMixin
from simplibs.object._core.metadata.instance_builders.instance.helpers._extend_instance_class import (
    _extend_instance_class,
)


class TestExtendInstanceClassStaticmethodHook:

    def test_staticmethod_hook_is_invoked_with_instance_class(self):
        calls = []

        class MixinA(SimpleMixin):
            __slots__ = ()

            @staticmethod
            def __extend_instance_class__(instance_class):
                calls.append(instance_class)

        class FakeInstanceClass:
            pass

        _extend_instance_class((MixinA,), FakeInstanceClass)
        assert calls == [FakeInstanceClass]

    def test_hook_can_mutate_target_class_in_place(self):
        class MixinA(SimpleMixin):
            __slots__ = ()

            @staticmethod
            def __extend_instance_class__(instance_class):
                instance_class.injected_attribute = "injected"

        class FakeInstanceClass:
            pass

        _extend_instance_class((MixinA,), FakeInstanceClass)
        assert FakeInstanceClass.injected_attribute == "injected"


class TestExtendInstanceClassClassmethodHook:

    def test_classmethod_hook_is_invoked(self):
        calls = []

        class MixinA(SimpleMixin):
            __slots__ = ()

            @classmethod
            def __extend_instance_class__(cls, instance_class):
                calls.append((cls, instance_class))

        class FakeInstanceClass:
            pass

        _extend_instance_class((MixinA,), FakeInstanceClass)
        assert calls == [(MixinA, FakeInstanceClass)]


class TestExtendInstanceClassNoHook:

    def test_mixin_without_hook_is_silently_skipped(self):
        class MixinNoHook(SimpleMixin):
            __slots__ = ()

        class FakeInstanceClass:
            pass

        _extend_instance_class((MixinNoHook,), FakeInstanceClass)


class TestExtendInstanceClassInvalidHookDecoration:

    def test_plain_instance_method_hook_raises(self):
        class MixinBadHook(SimpleMixin):
            __slots__ = ()

            def __extend_instance_class__(self, instance_class):
                pass

        class FakeInstanceClass:
            pass

        with pytest.raises(Exception):
            _extend_instance_class((MixinBadHook,), FakeInstanceClass)

    def test_plain_attribute_hook_raises(self):
        class MixinBadHook(SimpleMixin):
            __slots__ = ()
            __extend_instance_class__ = "not-a-method"

        class FakeInstanceClass:
            pass

        with pytest.raises(Exception):
            _extend_instance_class((MixinBadHook,), FakeInstanceClass)


class TestExtendInstanceClassMultipleMixins:

    def test_all_hooks_are_invoked_in_given_order(self):
        calls = []

        class MixinA(SimpleMixin):
            __slots__ = ()

            @staticmethod
            def __extend_instance_class__(instance_class):
                calls.append("A")

        class MixinB(SimpleMixin):
            __slots__ = ()

            @staticmethod
            def __extend_instance_class__(instance_class):
                calls.append("B")

        class FakeInstanceClass:
            pass

        _extend_instance_class((MixinA, MixinB), FakeInstanceClass)
        assert calls == ["A", "B"]

    def test_only_mixins_with_own_dict_hook_are_triggered(self):
        """
        Hook is checked directly via mixin.__dict__, not via inherited getattr.
        A subclass that does not explicitly redeclare the hook will not run it.
        """
        calls = []

        class ParentMixin(SimpleMixin):
            __slots__ = ()

            @staticmethod
            def __extend_instance_class__(instance_class):
                calls.append("parent")

        class ChildMixin(ParentMixin):
            __slots__ = ()

        class FakeInstanceClass:
            pass

        _extend_instance_class((ChildMixin,), FakeInstanceClass)
        assert calls == []