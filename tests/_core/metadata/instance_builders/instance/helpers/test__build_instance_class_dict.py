"""
Tests for `_core/metadata/instance_builders/instance/helpers/_build_instance_class_dict.py`.
"""
import pytest
from simplibs.object import SimpleConstant
from simplibs.object.mixins.base_class import SimpleMixin
from simplibs.object.exceptions import SimpleInitializationError
from simplibs.object._core.metadata.instance_builders.instance.helpers._build_instance_class_dict import (
    _build_instance_class_dict,
)


def _int_const(name="Widget", default=0):
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


class TestBuildInstanceClassDictBasicFields:

    def test_flags_and_mixins_tuple_are_set(self):
        class MixinA(SimpleMixin):
            __slots__ = ("_slot_a",)

        cls = _int_const()
        result = _build_instance_class_dict(cls, (MixinA,), is_atom=True, mutable=False)

        assert result["__is_constant__"] is True
        assert result["__is_mutable__"] is False
        assert MixinA in result["__mixins__"]

    def test_single_mixin_slot_is_collected(self):
        class MixinA(SimpleMixin):
            __slots__ = ("_slot_a",)

        cls = _int_const()
        result = _build_instance_class_dict(cls, (MixinA,), is_atom=True, mutable=True)

        assert result["__slots__"] == ("_slot_a",)

    def test_two_independent_mixins_slots_are_merged(self):
        class MixinA(SimpleMixin):
            __slots__ = ("_slot_a",)

        class MixinB(SimpleMixin):
            __slots__ = ("_slot_b",)

        cls = _int_const()
        result = _build_instance_class_dict(cls, (MixinA, MixinB), is_atom=True, mutable=True)

        assert set(result["__slots__"]) == {"_slot_a", "_slot_b"}


class TestBuildInstanceClassDictAttributesAndMethods:

    def test_attribute_and_method_are_copied_into_namespace(self):
        class MixinA(SimpleMixin):
            __slots__ = ()
            greeting = "hello"

            def say_hi(self):
                return "hi"

        cls = _int_const()
        result = _build_instance_class_dict(cls, (MixinA,), is_atom=True, mutable=True)

        assert result["greeting"] == "hello"
        assert result["say_hi"] is MixinA.__dict__["say_hi"]

    def test_ignored_dict_keys_are_not_copied(self):
        class MixinA(SimpleMixin):
            """Mixin docstring that must not leak into class_dict."""
            __slots__ = ()

        cls = _int_const()
        result = _build_instance_class_dict(cls, (MixinA,), is_atom=True, mutable=True)

        assert "__doc__" not in result
        assert "__module__" not in result
        assert "__dict__" not in result
        assert "__weakref__" not in result

    def test_slot_descriptors_are_not_copied_into_namespace_dict(self):
        class MixinA(SimpleMixin):
            __slots__ = ("_slot_a",)

        cls = _int_const()
        result = _build_instance_class_dict(cls, (MixinA,), is_atom=True, mutable=True)

        # Slot must appear inside the __slots__ tuple but not as a key in the namespace dict
        assert result["__slots__"] == ("_slot_a",)
        assert "_slot_a" not in result


class TestBuildInstanceClassDictOverridePrecedence:

    def test_earlier_mixin_in_tuple_wins_attribute_conflict(self):
        class MixinA(SimpleMixin):
            __slots__ = ()
            marker = "from_A"

        class MixinB(SimpleMixin):
            __slots__ = ()
            marker = "from_B"

        cls = _int_const()
        result = _build_instance_class_dict(cls, (MixinA, MixinB), is_atom=True, mutable=True)

        assert result["marker"] == "from_A"


class TestBuildInstanceClassDictInitHooksChaining:

    def test_combined_init_is_attached_when_hooks_present(self):
        class MixinA(SimpleMixin):
            __slots__ = ()

            def init_mixins(self):
                pass

        cls = _int_const()
        result = _build_instance_class_dict(cls, (MixinA,), is_atom=True, mutable=True)

        assert callable(result["init_mixins"])

    def test_no_init_mixins_key_when_no_hooks_declared(self):
        class MixinA(SimpleMixin):
            __slots__ = ()
            marker = "no_init_here"

        cls = _int_const()
        result = _build_instance_class_dict(cls, (MixinA,), is_atom=True, mutable=True)

        assert "init_mixins" not in result

    def test_hook_execution_order_is_reverse_of_user_provided_tuple(self):
        calls = []

        class MixinA(SimpleMixin):
            __slots__ = ()

            def init_mixins(self):
                calls.append("A")

        class MixinB(SimpleMixin):
            __slots__ = ()

            def init_mixins(self):
                calls.append("B")

        cls = _int_const()
        result = _build_instance_class_dict(cls, (MixinA, MixinB), is_atom=True, mutable=True)

        result["init_mixins"](object())
        assert calls == ["B", "A"]


class TestBuildInstanceClassDictSlotCollision:

    def test_two_mixins_with_same_slot_name_raise(self):
        class MixinA(SimpleMixin):
            __slots__ = ("_shared",)

        class MixinB(SimpleMixin):
            __slots__ = ("_shared",)

        cls = _int_const()
        with pytest.raises(SimpleInitializationError):
            _build_instance_class_dict(cls, (MixinA, MixinB), is_atom=True, mutable=True)

    def test_mixin_slot_colliding_with_base_class_slot_raises(self):
        class MixinWithCustomSlot(SimpleMixin):
            __slots__ = ("_custom_slot",)

        CustomBaseClass = type(
            "CustomBaseWithSlot",
            (SimpleConstant,),
            {
                "_type": int,
                "_default": 0,
                "__slots__": ("_custom_slot",),
            },
        )

        with pytest.raises(SimpleInitializationError):
            _build_instance_class_dict(
                CustomBaseClass, (MixinWithCustomSlot,), is_atom=True, mutable=True
            )


class TestBuildInstanceClassDictEmptyMixins:

    def test_no_mixins_produces_empty_slots_and_no_init_hook(self):
        cls = _int_const()
        result = _build_instance_class_dict(cls, (), is_atom=True, mutable=True)

        assert result["__slots__"] == ()
        assert "init_mixins" not in result
        assert result["__mixins__"] == ()