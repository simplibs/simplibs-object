"""
Tests for `_core/metadata/instance_builders/instance/helpers/create_instance_class.py`.
"""
import pytest
from simplibs.object.mixins.base_class import SimpleMixin
from simplibs.object._core.metadata.instance_builders.instance.helpers.create_instance_class import (
    create_instance_class,
)


class TestCreateInstanceClassSlotsBugRegression:

    def test_two_independently_slotted_mixins_no_longer_conflict(self, IntConst):
        class MixinA(SimpleMixin):
            __slots__ = ("_slot_a",)

        class MixinB(SimpleMixin):
            __slots__ = ("_slot_b",)

        base_class = IntConst.meta.atom_class_mutable
        result = create_instance_class(
            IntConst, (MixinA, MixinB), base_class, is_atom=True, mutable=True
        )
        assert isinstance(result, type)

    def test_resulting_class_has_single_base_in_bases(self, IntConst):
        class MixinA(SimpleMixin):
            __slots__ = ("_slot_a",)

        base_class = IntConst.meta.atom_class_mutable
        result = create_instance_class(
            IntConst, (MixinA,), base_class, is_atom=True, mutable=True
        )
        assert result.__bases__ == (base_class,)

    def test_instance_of_compiled_class_has_both_mixin_slots_accessible(self, IntConst):
        class MixinA(SimpleMixin):
            __slots__ = ("_slot_a",)

            def init_mixins(self):
                self._slot_a = "a"

        class MixinB(SimpleMixin):
            __slots__ = ("_slot_b",)

            def init_mixins(self):
                self._slot_b = "b"

        base_class = IntConst.meta.atom_class_mutable
        result = create_instance_class(
            IntConst, (MixinA, MixinB), base_class, is_atom=True, mutable=True
        )

        instance = object.__new__(result)
        if hasattr(instance, "init_mixins"):
            instance.init_mixins()

        assert instance._slot_a == "a"
        assert instance._slot_b == "b"


class TestCreateInstanceClassNaming:

    def test_class_name_follows_convention(self, IntConst):
        base_class = IntConst.meta.atom_class_mutable
        result = create_instance_class(IntConst, (), base_class, is_atom=True, mutable=True)
        assert result.__name__ == f"{IntConst.meta.class_name}Instance"

    def test_qualname_matches_name(self, IntConst):
        base_class = IntConst.meta.atom_class_mutable
        result = create_instance_class(IntConst, (), base_class, is_atom=True, mutable=True)
        assert result.__qualname__ == result.__name__


class TestCreateInstanceClassExtensionHooks:

    def test_extend_instance_class_hook_is_applied(self, IntConst):
        class MixinA(SimpleMixin):
            __slots__ = ()

            @staticmethod
            def __extend_instance_class__(instance_class):
                instance_class.injected = "yes"

        base_class = IntConst.meta.atom_class_mutable
        result = create_instance_class(
            IntConst, (MixinA,), base_class, is_atom=True, mutable=True
        )
        assert getattr(result, "injected", None) == "yes"


class TestCreateInstanceClassNoMixins:

    def test_works_with_empty_mixins_tuple(self, IntConst):
        base_class = IntConst.meta.atom_class_mutable
        result = create_instance_class(IntConst, (), base_class, is_atom=True, mutable=True)

        assert isinstance(result, type)
        assert result.__bases__ == (base_class,)